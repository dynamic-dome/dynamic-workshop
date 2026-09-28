import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "resources" / "demos" / "assets" / "hooks" / "secure-diff-gate.py"
INSTALLER = ROOT / "tools" / "install_workshop_plugin.ps1"
DOCTOR = ROOT / "tools" / "workshop_doctor.ps1"
POWERSHELL = shutil.which("powershell.exe") or shutil.which("powershell")


def _run_hook(path: str) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"tool_input": {"file_path": path}})
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )


def _git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def _run_installer(install_root: Path, repo_url: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            POWERSHELL,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(INSTALLER),
            "-InstallRoot",
            str(install_root),
            "-RepoUrl",
            str(repo_url),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def _create_source_repo(path: Path) -> None:
    path.mkdir()
    _git("init", "-b", "main", cwd=path)
    _git("config", "user.email", "workshop-tests@example.invalid", cwd=path)
    _git("config", "user.name", "Workshop Tests", cwd=path)
    plugin = path / ".claude-plugin"
    plugin.mkdir()
    (plugin / "plugin.json").write_text(
        json.dumps(
            {"name": "dynamic-workshop", "version": "0.0.0", "description": "test"}
        ),
        encoding="utf-8",
    )
    (path / "state.txt").write_text("one\n", encoding="utf-8")
    _git("add", ".", cwd=path)
    _git("commit", "-m", "initial", cwd=path)


def test_secure_diff_gate_blocks_env_with_contract_exit_2():
    result = _run_hook("config/.env")

    assert result.returncode == 2
    assert "BLOCKED" in result.stderr


def test_secure_diff_gate_blocks_pem_with_contract_exit_2():
    result = _run_hook("certificates/panel.pem")

    assert result.returncode == 2
    assert "BLOCKED" in result.stderr


def test_secure_diff_gate_allows_normal_write():
    result = _run_hook("src/access_control.py")

    assert result.returncode == 0
    assert result.stderr == ""


@pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")
def test_installer_updates_clean_checkout_fast_forward_only(tmp_path: Path):
    source = tmp_path / "source"
    install_root = tmp_path / "install"
    _create_source_repo(source)

    first = _run_installer(install_root, source)
    assert first.returncode == 0, first.stdout + first.stderr

    (source / "state.txt").write_text("two\n", encoding="utf-8")
    _git("add", "state.txt", cwd=source)
    _git("commit", "-m", "update", cwd=source)
    expected_head = _git("rev-parse", "HEAD", cwd=source)

    second = _run_installer(install_root, source)
    checkout = install_root / "dynamic-workshop"

    assert second.returncode == 0, second.stdout + second.stderr
    assert _git("rev-parse", "HEAD", cwd=checkout) == expected_head
    # This static guard complements the behavioral update check: a plain pull
    # could also update but would violate the approved no-merge contract.
    assert "--ff-only" in INSTALLER.read_text(encoding="utf-8")


@pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")
def test_installer_rejects_existing_checkout_with_wrong_origin_without_changes(
    tmp_path: Path,
):
    requested_source = tmp_path / "requested-source"
    wrong_source = tmp_path / "wrong-source"
    install_root = tmp_path / "install"
    _create_source_repo(requested_source)
    _create_source_repo(wrong_source)
    assert _run_installer(install_root, wrong_source).returncode == 0

    checkout = install_root / "dynamic-workshop"
    head_before = _git("rev-parse", "HEAD", cwd=checkout)
    status_before = _git("status", "--porcelain", "--untracked-files=all", cwd=checkout)

    result = _run_installer(install_root, requested_source)

    assert result.returncode != 0
    assert "origin" in (result.stdout + result.stderr).lower()
    assert _git("rev-parse", "HEAD", cwd=checkout) == head_before
    assert _git("status", "--porcelain", "--untracked-files=all", cwd=checkout) == status_before


@pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")
def test_installer_rejects_existing_checkout_with_wrong_plugin_name_without_changes(
    tmp_path: Path,
):
    source = tmp_path / "source"
    install_root = tmp_path / "install"
    _create_source_repo(source)
    assert _run_installer(install_root, source).returncode == 0

    checkout = install_root / "dynamic-workshop"
    manifest = checkout / ".claude-plugin" / "plugin.json"
    manifest.write_text(
        json.dumps({"name": "another-plugin", "version": "0.0.0"}),
        encoding="utf-8",
    )
    _git("add", ".claude-plugin/plugin.json", cwd=checkout)
    _git("commit", "-m", "change plugin identity", cwd=checkout)
    head_before = _git("rev-parse", "HEAD", cwd=checkout)
    status_before = _git("status", "--porcelain", "--untracked-files=all", cwd=checkout)

    result = _run_installer(install_root, source)

    assert result.returncode != 0
    assert "dynamic-workshop" in (result.stdout + result.stderr)
    assert _git("rev-parse", "HEAD", cwd=checkout) == head_before
    assert _git("status", "--porcelain", "--untracked-files=all", cwd=checkout) == status_before


@pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")
def test_installer_rejects_dirty_checkout(tmp_path: Path):
    source = tmp_path / "source"
    install_root = tmp_path / "install"
    _create_source_repo(source)
    assert _run_installer(install_root, source).returncode == 0

    checkout = install_root / "dynamic-workshop"
    (checkout / "state.txt").write_text("local change\n", encoding="utf-8")
    result = _run_installer(install_root, source)

    assert result.returncode != 0
    assert "dirty" in (result.stdout + result.stderr).lower()
    assert (checkout / "state.txt").read_text(encoding="utf-8") == "local change\n"


@pytest.mark.skipif(POWERSHELL is None, reason="Windows PowerShell is required")
def test_installer_rejects_existing_non_git_destination(tmp_path: Path):
    source = tmp_path / "source"
    install_root = tmp_path / "install"
    _create_source_repo(source)
    destination = install_root / "dynamic-workshop"
    destination.mkdir(parents=True)
    (destination / "keep.txt").write_text("keep\n", encoding="utf-8")

    result = _run_installer(install_root, source)

    assert result.returncode != 0
    assert "git" in (result.stdout + result.stderr).lower()
    assert (destination / "keep.txt").read_text(encoding="utf-8") == "keep\n"


def test_doctor_requires_git_checkout_and_valid_plugin_manifest():
    source = DOCTOR.read_text(encoding="utf-8")

    assert "rev-parse" in source
    assert "plugin.json" in source
    assert "ConvertFrom-Json" in source
    assert "dynamic-workshop" in source

# Claude Code changelog

> Release notes for Claude Code, including new features, improvements, and bug fixes by version.

This page is generated from the [CHANGELOG.md on GitHub](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). Longer releases are grouped by type of change, with long lists of improvements and bug fixes collapsed.

Run `claude --version` to check your installed version.

**2.1.310**

October 23, 2026

**Added**

* Added the Monitor tool and plugin monitors on Bedrock, Vertex, and Foundry, and when telemetry or nonessential traffic is disabled; long foreground sleeps are now blocked there too
* \[Cloud sessions] Added Claude Code cloud sessions and Remote Control permissions to Enterprise custom roles, so Owners can control access to each by role

**Changed**

* Changed the error for an MCP tool call that times out in a non-interactive session while the server's elicitation is unanswered: it now tells Claude that no answer came and not to repeat the call
* \[Cloud sessions] Changed turning on Cloud sessions or Remote Control in admin settings to ask for confirmation and list the custom roles that have that permission

**6 improvements**

* Improved auto mode's prompt before the first read outside the working directories: it now says when blocking those reads makes shell commands ask for permission
* Improved memory use of non-interactive sessions (`-p`, Agent SDK) during compaction when the transcript file is very large

**14 bug fixes**

* Fixed requests failing behind some gateways and compatible servers that reject the `effort-2025-11-24` beta value or mid-conversation system messages; Claude Code now retries without them
* Fixed background cleanup deleting some recent files, such as pasted images, when `cleanupPeriodDays` is set to a very large value
* Windows: Fixed PreToolUse and PermissionRequest hooks letting a tool call through when Git Bash is missing and the hook's command is only quoted strings, such as a quoted path
* \[VSCode] Fixed pressing Enter on the plan review card's "Send feedback and keep planning" button approving the plan instead of sending your comments back

**2.1.309**

October 22, 2026

**Added**

* \[VSCode] Added a log warning that says what to do when dictation or the extension's own requests fail certificate verification, such as behind a TLS-inspecting proxy

**Changed**

* Updated the bundled dataviz skill to accept APCA as a text-contrast measure (keeping WCAG 2 ratios where AA conformance is required), add an `apca(text, background)` function to its palette validator scripts, and say whether a label inside a colored chart fill should be white or near-black
* Updated the /claude-api skill: service account keys and Workload Identity Federation tokens can now manage OpenTelemetry destinations

**8 improvements**

* Improved the speed of many git commands Claude Code runs for itself on Windows; on every platform, errors from those commands now show in English even when git is set to another language
* Improved the error when a hooks module is nested too deep to load: it now names the file instead of showing a bare stack-overflow message

**62 bug fixes**

* Fixed sandboxed Bash commands on macOS and Linux running the shell's startup files outside the sandbox before each command
* Fixed macOS sandbox `denyWrite` glob patterns not applying at a path's real location when the pattern's folder is reached through a symlink
* Windows: Fixed PowerShell permission checks auto-approving some `Set-Location` or `cd` commands that target the current directory and carry extra arguments; these now prompt for approval
* \[VSCode] Fixed the Claude panel staying blank after the editor cached an incomplete copy of its files; it now recovers by itself, or says what went wrong and how to fix it

**2.1.308**

October 22, 2026

* Bug fixes and reliability improvements

**2.1.293**

October 7, 2026

**Added**

* Added Claude Haiku 5.5 (`claude-haiku-5-5`), now the default Haiku model on the Anthropic API — 1M context, $0.10/$0.50 per Mtok ($0.50/$2.50 for prompts over 100K)
* Added `agentType` to the `subagentStatusLine` payload, so scripts can tell custom subagent types apart

**Changed**

* Reverted the auto mode denial message change from 2.1.281 that told Claude a denial covers the outcome, not only the exact command
* Reverted the 2.1.290 fix for cloud sessions staying asleep after a container restart lost a pending `/loop` wakeup or scheduled task; Claude is no longer told, and the session stays asleep

**7 improvements**

* Improved startup for Team and Enterprise organizations: policy and managed settings are fetched earlier, and a stalled request is retried after 3 seconds
* Improved Claude in Chrome: fewer page actions are refused when the browser is slow to report its tabs

**38 bug fixes**

* Fixed Claude sometimes treating its own last actions before a context compaction as done after it, and retracting or redoing finished work
* Fixed a memory leak where an HTTP MCP connection kept every request it had sent until it closed
* Windows: Fixed stopping a status line, hook, or shell command sometimes terminating an unrelated process that had been given the same process ID

**2.1.292**

October 6, 2026

**Added**

* Added `--marketplace <source>` to `claude plugin install`: adds the marketplace if needed, under the same policy checks as `claude plugin marketplace add`, then installs the plugin from it
* Added an `effort` parameter to the Agent tool, so Claude runs a sub-agent at the effort level you ask for

**Changed**

* Changed local (stdio) MCP server connections to negotiate protocol version 2026-07-28 by default on every install, including Bedrock, Vertex and Foundry; `MCP_PROTOCOL_NEGOTIATION=legacy` opts out
* Changed `claude plugin test`: a failed `expect` inside a hook the test registered, or a stub answer the engine refuses, now fails the test instead of passing silently

**13 improvements**

* Improved startup of `claude -p` and SDK sessions: the first turn no longer waits for HTTP and SSE MCP servers to answer `resources/list`
* Improved rendering speed of long bulleted or numbered replies: they stream, resize and re-open in the transcript (ctrl+o) much faster

**64 bug fixes**

* Fixed subagent definitions with `permissionMode: auto` entering auto mode when auto mode is unavailable (disabled by settings, circuit breaker, or a model that doesn't support it)
* Fixed sandboxed commands being able to read the staged file copies of `/ultrareview` uploads under `~/.claude/seed-admin`

**2.1.291**

October 6, 2026

* Fixed a regression in 2.1.290 where cloud sessions could drop answers to permission prompts
* Fixed a regression in 2.1.288 where the last messages of a session could be lost when quitting

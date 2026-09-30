# safety-check.ps1 - PreToolUse hook (matcher "Bash|PowerShell"): block destructive shell commands.
# tested asset: resources/demos/assets/hooks/safety-check.ps1
#
# Contract (official hooks reference):
#   - Claude Code sends the event as JSON on stdin; the shell command is in tool_input.command
#     (the Bash and the PowerShell tool use the same field).
#   - exit 2 = BLOCK: the command does not run, and stderr is shown to Claude as the reason.
#   - exit 0 = no objection: the normal permission flow decides.
#   - Any OTHER exit code (1, ...) does NOT block: the command runs anyway.
#   - On Windows, shell commands usually run through the PowerShell tool. A hook with
#     matcher "Bash" alone never fires there, so register it as "Bash|PowerShell".
#   - The patterns are examples, not complete protection: combine hooks with permission
#     rules and a sandbox.

$raw = [Console]::In.ReadToEnd()

# Fail closed: if the input cannot be read, block instead of silently allowing everything.
try { $data = $raw | ConvertFrom-Json -ErrorAction Stop }
catch {
  [Console]::Error.WriteLine("SAFETY HOOK: could not read the hook input - blocking to stay safe.")
  exit 2
}
$command = [string]$data.tool_input.command

# Dangerous patterns (same set as the bash version); the last four are PowerShell and cmd
$dangerous = @(
  'rm\s+-rf',
  'git push.*--force',
  'git push.*-f(\s|$)',
  'DROP TABLE',
  'truncate.*--yes',
  'mkfs\.',
  'dd\s+if=.*of=/dev/',
  '> /dev/sd',
  '(^|[^\w-])(Remove-Item|rm|ri|del|erase|rmdir|rd)\s.*-Recurse',
  '(^|[^\w-])(rd|rmdir)\s+/s',
  'Format-Volume',
  'Clear-Disk'
)

foreach ($pattern in $dangerous) {
  # -match is case-insensitive by default (like grep -i)
  if ($command -match $pattern) {
    [Console]::Error.WriteLine("SAFETY HOOK: potentially destructive command blocked.")
    [Console]::Error.WriteLine("Command: $command")
    [Console]::Error.WriteLine("Pattern matched: $pattern")
    [Console]::Error.WriteLine("If this was intended, run it yourself outside Claude Code.")
    exit 2
  }
}

# All checks passed - no objection
exit 0

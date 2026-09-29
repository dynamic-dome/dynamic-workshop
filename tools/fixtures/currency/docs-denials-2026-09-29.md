<!-- Auszug aus der offiziellen Doku, abgerufen 2026-09-29: hooks.md:754, cli-reference.md:86, env-vars.md:174 -->
There is no `$CLAUDE_MODEL` environment variable. The hook can read `$ANTHROPIC_MODEL` if you set it in your shell, but that value doesn't change when you switch models with `/model` during a session.
| `--enable-auto-mode` | Removed in v2.1.111. Auto mode is now in the `Shift+Tab` cycle by default; use `--permission-mode auto` to start in it | `claude --permission-mode auto` |
| `ANTHROPIC_MODEL` | Name of the model setting to use (see [Model Configuration](/docs/en/model-config#environment-variables)) |

---
name: workshop
description: "Claude Code Workshop — interactive teaching plugin with guide and learn modes. Use /workshop for overview, /workshop guide [module] for moderator mode, /workshop learn [module] for self-paced learning."
user_invocable: true
arguments:
  - name: mode
    description: "Mode: 'guide' (moderator), 'learn' (self-paced), or omit for overview"
    required: false
  - name: module
    description: "Module ID like '1.1', '2.3', 'block-1', or omit for full overview"
    required: false
---

# Workshop Command

Load the `workshop` skill with the provided arguments.

If no arguments: show the full module overview.
If mode is `guide`: activate moderator co-pilot mode for the specified module.
If mode is `learn`: activate interactive tutor mode for the specified module.
If only a module ID is given without mode: default to `learn`.

Valid module IDs:
- Block 1 (Foundations): 1.1, 1.2, 1.3, 1.4, 1.5 (or "block-1" for all)
- Block 2 (Ecosystem): 2.1, 2.2, 2.3, 2.4, 2.5 (or "block-2" for all)
- Block 3 (Advanced): 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 (or "block-3" for all)

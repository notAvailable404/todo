# TODO-PY `v0.4.7`

A minimalist, terminal-based task manager written in Python. No bloat, no complex databases—just a single script and a CSV file.

```text
 .      ::::::::::: ::::::::  :::::::::   ::::::::      .
    ,      :+:    :+:    :+: :+:    :+: :+:    :+:   *
          +:+    +:+    +:+ +:+    +:+ +:+    +:+        .
     *   +#+    +#+    +:+ +#+    +#+ +#+    +#+   +
  +     +#+    +#+    +#+ +#+    +#+ +#+    +#+  * 
     + #+#    #+#    #+# #+#    #+# #+#    #+#     
 *    ###     ########  #########   ########    +    *
```

## Features

* **Persistent Storage:** Automatically saves tasks to a `.csv` file in your home directory (`~/.config/todo-py/` or equivalent).
* **Automatic Backups:** If the CSV file gets corrupted, the script automatically creates a backup before wiping the slate.
* **Cross-Platform:** Includes ANSI initialization for Windows and standard escape sequences for Unix-based systems.
* **No Dependencies:** Uses only the Python Standard Library.

---

## Installation & Usage

1. **Prerequisites:** Ensure you have **Python 3.10+** installed (required for the `match` statement).
2. **Download:** Grab `todo.py`.
3. **Run:**
```bash
python todo.py
```

### Command Reference

| Command | Action | Example |
| --- | --- | --- |
| `+ {text}` | **Add** a new task | `+ Buy more coffee` |
| `x {num}` | **Toggle** task as done/undone | `x 1` |
| `- {num}` | **Delete** a task | `- 2` |
| `c` | **Clear** the screen | `c` |
| `h` | Show **Help** menu | `h` |
| `q` | **Quit** | `q` |

---

## Disclaimer & License

**This software is provided as-is, you are liable for your own use of this software, it will not be updated or maintained, update it as you yourself see fit, it is released under the CC0 license.**

This project is dedicated to the public domain under the Creative Commons Zero (CC0) license. You can copy, modify, and distribute the code, even for commercial purposes, all without asking permission.

---

### A Note on Maintenance

> This project is considered **feature-complete** (or more accurately, **finished with**). The author will not be checking issues, merging pull requests, or fixing bugs. If it breaks, you own both halves.

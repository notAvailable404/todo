import os
import csv
import shutil
import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

if os.name == 'nt':
    os.system('') # Force ANSI initialization, hopefully whoever uses this shitty cold doesn't use a REALLY old version of python, or a REALLY old version of windows!
    def clear_screen(): os.system('cls')
else:
    def clear_screen(): print("\033[H\033[J", end="", flush=True)

# CONFIG
APP_VERSION = "v0.4.5"
LOGO = """
 .      ::::::::::: ::::::::  :::::::::   ::::::::      .
    ,      :+:    :+:    :+: :+:    :+: :+:    :+:   *
          +:+    +:+    +:+ +:+    +:+ +:+    +:+        .
     *   +#+    +#+    +:+ +#+    +#+ +#+    +#+   +
  +     +#+    +#+    +#+ +#+    +#+ +#+    +#+  * 
     + #+#    #+#    #+# #+#    #+# #+#    #+#     
 *    ###     ########  #########   ########    +    *"""

@dataclass
class Task:
    text: str
    done: bool = False

def handle_add(tasks: list, text: str, save_file: Path):
    if text: 
        tasks.append(Task(text))
        save_tasks(tasks, save_file)

def get_save_path() -> Path:
    # Consolidated path logic without needing extra dependencies like `platformdirs`
    # Standard XDG/Windows paths using only Pathlib
    base = Path.home() / ".config" if (Path.home() / ".config").exists() else Path.home()
    app_dir = base / "todo-py"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / "tasks.csv"

def handle_modify(tasks: list, op: str, val: str, save_file: Path):
    if not val.isdigit(): return
    idx = int(val) - 1
    if 0 <= idx < len(tasks):
        if op == '-': tasks.pop(idx)
        else: tasks[idx].done = not tasks[idx].done
        save_tasks(tasks, save_file)

def backup_corrupt_file(path: Path, base_name="error_file"):
    if not path.exists(): return None
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_path = path.parent / f"{base_name}_{ts}.csv"
    counter = 1
    while backup_path.exists():
        backup_path = path.parent / f"{base_name}_{ts}_{counter}.csv"
        counter += 1
    try:
        path.replace(backup_path)
        return backup_path
    except OSError:
        try:
            shutil.copy2(path, backup_path)
            path.unlink()
            return backup_path
        except Exception: return None

def load_tasks(save_path: Path):
    if not save_path.exists() or save_path.stat().st_size == 0:
        return [Task("Add your first task with '+'"), Task("Type 'h' for help")]

    tasks = []
    try:
        with save_path.open(mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append(Task(row.get("text", ""), row.get("done") == "True"))
        return tasks 
    except Exception as e:
        # Simple, effective backup
        backup = save_path.with_suffix(".csv.bak")
        save_path.replace(backup)
        print(f"[!] Error loaded. Corrupt file moved to {backup.name}")
        return []

def save_tasks(tasks: list, save_path: Path):
    try:
        with save_path.open(mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "done"])
            writer.writeheader()
            for task in tasks:
                writer.writerow(asdict(task))
    except IOError as e:
        print(f"[!] Save failed: {e}")

def display_help(error_msg=None):
    clear_screen()
    cols, _ = shutil.get_terminal_size()

    print(f"TODO-PY HELP MENU ({APP_VERSION})\n" + "=" * cols)
    print("\nCOMMANDS:")
    print("  + {text} : Add task\n  x {num}  : Toggle done on task {num}\n  - {num}  : Delete task {num}\n  c        : Clear the screen\n  h        : Shows this help menu\n  q        : Quit application\n")
    if error_msg:
        print("-" * (len(error_msg) + 12))
        print(f"\n[!] ERROR:\n{error_msg}")

    input("\n[ Press Enter to return ]\n")

def display_tui(tasks):
    clear_screen()
    print(f"{APP_VERSION}\n{LOGO}")
    if not tasks:
        print("\n (No tasks found)")
    else:
        print("") # Top padding
        max_len = max(len(t.text) for t in tasks) if tasks else 0
        for i, task in enumerate(tasks, 1):
            status = "[X]" if task.done else "[ ]"
            print(f"{status} {task.text.ljust(max_len)}  ({i})")
    
    footer = "[+]task | [-]num | [x]num | [c]lear | [h]elp | [q]uit"
    print("\n" + "=" * len(footer))
    print(footer)    
    return input("[-] > ").strip()

def main():
    save_file = get_save_path()
    tasks = load_tasks(save_file)

    while True:
        user_input = display_tui(tasks)
        if not user_input: continue

        parts = user_input.split(maxsplit=1)
        action = parts[0].lower()
        val = parts[1] if len(parts) > 1 else ""

        # Quick command parsing
        if action.startswith('+') and len(action) > 1:
            val = action[1:] + (f" {val}" if val else "")
            action = '+'
        elif (action.startswith('-') or action.startswith('x')) and len(action) > 1 and action[1:].isdigit():
            val = action[1:]
            action = action[0]

        # Clean, decoupled match statement
        match action:
            case 'q':
                print("Goodbye!")
                break
            case 'c': pass
            case '+': handle_add(tasks, val, save_file)
            case '-' | 'x': handle_modify(tasks, action, val, save_file)
            case 'h': display_help()
            case _: display_help(f"'{action}' is not a valid command.")

if __name__ == "__main__":
    main()


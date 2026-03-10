import os
import csv
import shutil
import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

# Force ANSI for Windows users on older terminals
if os.name == 'nt':
    os.system('') 
    def clear_screen(): os.system('cls')
else:
    def clear_screen(): print("\033[H\033[J", end="", flush=True)

# CONFIG
APP_VERSION = "v0.4.9"
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
    # Strip leading/trailing whitespace and redundant quotes
    clean_text = text.strip().strip('"').strip("'")
    if clean_text: 
        tasks.append(Task(clean_text))
        save_tasks(tasks, save_file)

def get_save_path() -> Path:
    # Logic for XDG/Linux paths without extra dependencies
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

def load_tasks(save_path: Path):
    if not save_path.exists() or save_path.stat().st_size == 0:
        return [Task("Add your first task with '+'"), Task("Type 'h' for help")]

    tasks = []
    try:
        with save_path.open(mode="r", newline="", encoding="utf-8") as f:
            # quotechar and quoting handle the CSV structure
            reader = csv.DictReader(f, quotechar='"')
            for row in reader:
                # Convert '1' back to True, '0' to False
                tasks.append(Task(row.get("text", ""), row.get("done") == "1"))
        return tasks 
    except Exception as e:
        backup = save_path.with_suffix(".csv.bak")
        save_path.replace(backup)
        print(f"[!] Error loading tasks. Corrupt file moved to {backup.name}")
        return []

def save_tasks(tasks: list, save_path: Path):
    try:
        with save_path.open(mode="w", newline="", encoding="utf-8") as f:
            # QUOTE_NONNUMERIC puts quotes around strings but leaves our 0/1 as-is
            writer = csv.DictWriter(f, fieldnames=["text", "done"], quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for task in tasks:
                writer.writerow({
                    "text": task.text,
                    "done": 1 if task.done else 0  # Save as integer for disk efficiency
                })
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
            
            # This capitalizes the first letter but preserves the rest of the string
            # If you prefer full .capitalize(), just use: task.text.capitalize()
            display_text = task.text[:1].upper() + task.text[1:]
            
            print(f"{status} {display_text.ljust(max_len)}  ({i})")
    
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

        if action.startswith('+') and len(action) > 1:
            val = action[1:] + (f" {val}" if val else "")
            action = '+'
        elif (action.startswith('-') or action.startswith('x')) and len(action) > 1 and action[1:].isdigit():
            val = action[1:]
            action = action[0]

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

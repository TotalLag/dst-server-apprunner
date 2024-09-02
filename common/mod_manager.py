"""
Module: mod_manager.py
Description: Manages adding, removing, and listing mods for the server setup. 
Uses Steam Workshop to fetch mod details and manages the dedicated server mod setup file.
"""

import time
import sys
from queue import Queue

MOD_FILE_PATH = "/home/steam/dst-dedicated/mods/dedicated_server_mods_setup.lua"
MOD_SETTINGS_PATH = "/home/steam/dst-dedicated/mods/modsettings.lua"


def read_file(file_path):
    """
    Reads the specified file and returns its lines.

    Args:
        file_path (str): Path to the file to read.

    Returns:
        list: List of lines in the file.
    """
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except IOError as e:
        print(f"Error reading {file_path}: {e}")
        return []


def write_file(file_path, lines):
    """
    Writes the given lines to the specified file.

    Args:
        file_path (str): Path to the file to write.
        lines (list): List of lines to write to the file.
    """
    try:
        with open(file_path, "w") as file:
            file.writelines(lines)
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")


def read_mod_file():
    """Reads the dedicated server mods setup file."""
    return read_file(MOD_FILE_PATH)


def write_mod_file(lines):
    """Writes to the dedicated server mods setup file."""
    write_file(MOD_FILE_PATH, lines)


def read_mod_settings():
    """
    Reads the mod settings file and extracts mods as a dictionary.

    Returns:
        tuple: A dictionary of mods and a list of lines in the file.
    """
    lines = read_file(MOD_SETTINGS_PATH)
    mods = {}
    in_table = False

    for line in lines:
        line = line.strip()
        if line.startswith("return {"):
            in_table = True
            continue
        if in_table and line.startswith('["workshop-'):
            mod_id = line.split('"]')[0].split('["workshop-')[1]
            mods[mod_id] = line

    return mods, lines


def write_mod_settings(mod_lines):
    """Writes the mod settings to the mod settings file."""
    write_file(MOD_SETTINGS_PATH, mod_lines)


def get_installed_mods():
    """
    Retrieves the list of installed mods from the mods setup file.

    Returns:
        list: List of tuples with mod ID and comment.
    """
    lines = read_mod_file()
    mods = []

    for line in lines:
        if line.strip().startswith("ServerModSetup"):
            parts = line.split('"')
            if len(parts) > 1:
                mod_id = parts[1]
                comment = line.split("--")[-1].strip() if "--" in line else ""
                mods.append((mod_id, comment))

    return mods


def insert_mod(mod_id, title, summary):
    """
    Inserts or updates a mod in both the mods setup file and mod settings file.

    Args:
        mod_id (str): The ID of the mod.
        title (str): The title of the mod.
        summary (str): A summary of the mod's description.
    """
    # Update dedicated_server_mods_setup.lua
    lines = read_mod_file()
    new_line = f'ServerModSetup("{mod_id}") -- {title}: {summary}\n'
    inserted = False

    for i in range(len(lines) - 1, -1, -1):
        if "ServerModSetup" in lines[i] and not lines[i].strip().startswith("--"):
            lines.insert(i + 1, new_line)
            inserted = True
            break

    if not inserted:
        lines.append(new_line)

    write_mod_file(lines)
    print(f"Mod {mod_id} added or updated in {MOD_FILE_PATH}.")

    # Update modsettings.lua
    mod_settings, all_lines = read_mod_settings()
    mod_key = f'["workshop-{mod_id}"]'
    new_setting_line = f"  {mod_key} = {{ enabled = true }}, -- {title}\n"
    all_lines = [line for line in all_lines if not line.strip().startswith(mod_key)]

    for i in range(len(all_lines) - 1, -1, -1):
        if all_lines[i].strip() == "}":
            all_lines.insert(i, new_setting_line)
            break

    write_mod_settings(all_lines)
    print(f"Mod {mod_id} added or updated in {MOD_SETTINGS_PATH}.")


def add_mods(mod_ids, delay=0.75):
    """
    Adds the specified mods by their IDs, fetching information and updating files.

    Args:
        mod_ids (list): List of mod IDs to add.
        delay (float): Delay in seconds between processing mods.
    """
    try:
        from fetch_mod_info import fetch_mod_description, summarize_description
    except ImportError:
        print(
            "Error: Unable to import fetch_mod_info. Make sure it's in the same directory."
        )
        return

    mod_queue = Queue()
    for mod_id in mod_ids:
        mod_queue.put(mod_id)

    while not mod_queue.empty():
        mod_id = mod_queue.get()
        installed_mods = get_installed_mods()

        if any(mod[0] == mod_id for mod in installed_mods):
            print(f"Mod {mod_id} already exists. Updating information...")
            remove_mods([mod_id])

        try:
            title, description = fetch_mod_description(mod_id)
            summary = summarize_description(description)
            insert_mod(mod_id, title, summary)
            print(
                f"Mod {mod_id} added/updated successfully with title: {title} and summary: {summary}"
            )
        except Exception as e:
            print(f"Error adding/updating mod {mod_id}: {e}")

        time.sleep(delay)


def remove_mods(mod_ids):
    """
    Removes the specified mods by their IDs from both the mods setup file and mod settings file.

    Args:
        mod_ids (list): List of mod IDs to remove.
    """
    lines = read_mod_file()
    modified_lines = []
    modified = False

    for line in lines:
        if not any(f'ServerModSetup("{mod_id}")' in line for mod_id in mod_ids):
            modified_lines.append(line)
        else:
            modified = True
            mod_id = [mid for mid in mod_ids if f'ServerModSetup("{mid}")' in line][0]
            print(f"Mod {mod_id} removed from {MOD_FILE_PATH}.")

    if modified:
        write_mod_file(modified_lines)

    mod_settings, all_lines = read_mod_settings()
    for mod_id in mod_ids:
        mod_key = f'["workshop-{mod_id}"]'
        if mod_key in mod_settings:
            all_lines = [
                line for line in all_lines if not line.strip().startswith(mod_key)
            ]
            print(f"Mod {mod_id} removed from {MOD_SETTINGS_PATH}.")

    write_mod_settings(all_lines)


def list_installed_mods():
    """Lists all installed mods."""
    mods = get_installed_mods()
    if mods:
        print("Installed mods:")
        for mod in mods:
            print(f"- [{mod[0]}]: {mod[1].strip(' -')}")
    else:
        print("No mods installed.")


def main():
    """Main function to handle command-line arguments for mod management."""
    if len(sys.argv) < 2:
        print("Usage: python mod_manager.py <action> [mod_id1] [mod_id2] ...")
        print("Actions: add, remove, list")
        sys.exit(1)

    action = sys.argv[1]
    if action in ["add", "remove"] and len(sys.argv) > 2:
        mod_ids = sys.argv[2:]
        if action == "add":
            add_mods(mod_ids)
        elif action == "remove":
            remove_mods(mod_ids)
    elif action == "list":
        list_installed_mods()
    else:
        print("Invalid action or missing mod_id")
        sys.exit(1)


if __name__ == "__main__":
    main()

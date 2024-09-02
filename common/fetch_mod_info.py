"""
Module: fetch_mod_info.py
Description: Fetches mod information (title and description) from the Steam Workshop and provides a summary.
"""

import re
import time
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "Error: Required libraries 'requests' and 'beautifulsoup4' are not installed."
    )
    print("Please install them using: pip install requests beautifulsoup4")
    sys.exit(1)


def fetch_mod_description(mod_id, retries=3):
    """
    Fetches the title and description of a mod from the Steam Workshop.

    Args:
        mod_id (str): The ID of the mod to fetch.
        retries (int): Number of times to retry fetching in case of failure.

    Returns:
        tuple: A tuple containing the mod's title and description.
    """
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("div", class_="workshopItemTitle")
            title = (
                title_element.text.strip() if title_element else "No title available."
            )

            description_element = soup.find("div", class_="workshopItemDescription")
            description = (
                description_element.text.strip()
                if description_element
                else "No description available."
            )

            return title, description
        except requests.RequestException as e:
            print(f"Error fetching mod {mod_id}, attempt {attempt + 1}/{retries}: {e}")
            time.sleep(2)

    return "Error fetching mod information.", "Error fetching mod information."


def summarize_description(description, max_length=100):
    """
    Summarizes the description to a shorter form.

    Args:
        description (str): The full description of the mod.
        max_length (int): The maximum length of the summary.

    Returns:
        str: A summarized version of the description.
    """
    lines = description.splitlines()
    filtered_lines = [
        line
        for line in lines
        if not re.match(r"^\s*v\d+(\.\d+)*", line.strip().lower())
    ]

    for line in filtered_lines:
        if line.strip():
            summary = line.strip()
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            return summary

    return "No relevant description available."


def main():
    """
    Main function to fetch mod information based on command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Usage: python fetch_mod_info.py <mod_id1> <mod_id2> ...")
        sys.exit(1)

    mod_ids = sys.argv[1:]
    for mod_id in mod_ids:
        title, description = fetch_mod_description(mod_id)
        summary = summarize_description(description)
        print(f"Title: {title}\nSummary: {summary}\n")
        time.sleep(2)


if __name__ == "__main__":
    main()

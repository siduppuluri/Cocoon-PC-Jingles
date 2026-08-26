import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "database" / "games.json"
INDEX = ROOT / "index.json"


def main():
    with DATABASE.open("r", encoding="utf-8") as file:
        database = json.load(file)

    entries = []

    for game in database["games"]:
        if game.get("review_status") != "approved":
            continue

        entries.append(
            {
                "game": game["game"],
                "file": game["clip"]["file"],
            }
        )

    index = {
        "name": "Cocoon PC Jingles",
        "entries": entries,
    }

    with INDEX.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2, ensure_ascii=False)
        file.write("\n")

    print(f"Generated {INDEX}")
    print(f"{len(entries)} jingle(s) included")


if __name__ == "__main__":
    main()
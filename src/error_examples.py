import csv
import json
from pathlib import Path

RESULTS_FILE = Path("results/per_item.csv")
DATA_FILE = Path("data/items.jsonl")

def load_items():

    items = {}

    with DATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            item = json.loads(line)

            if item["split"] == "test":
                items[item["id"]] = item

    return items

def load_results():

    with RESULTS_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(csv.DictReader(file))

def main():

    items = load_items()
    results = load_results()

    models = []

    for row in results:
        if row["model"] not in models:
            models.append(row["model"])

    print("=" * 100)
    print("WRONG-ANSWER EXAMPLES")
    print("=" * 100)

    for model in models:

        errors = [
            row
            for row in results
            if row["model"] == model
            and row["status"] != "correct"
        ]

        print()
        print("-" * 100)
        print(f"MODEL: {model}")
        print("-" * 100)

        if not errors:
            print("No errors.")
            continue

        for row in errors[:3]:

            item = items[row["item_id"]]

            print()
            print(f"Item: {row['item_id']}")
            print(f"Expected: {row['expected']}")
            print(f"Output: {row['output']}")
            print(f"Status: {row['status']}")
            print(f"Clause: {item['clause']}")

    print()
    print("=" * 100)

if __name__ == "__main__":
    main()
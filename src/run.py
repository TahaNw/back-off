import csv
import json
import time
from pathlib import Path
import requests
from prompt import build_prompt
from score import score

# configuration
MODELS = [
    "qwen2.5:7b",
    "qwen2.5:3b",
    "phi3.5:latest",
]
OLLAMA_URL = "http://localhost:11434/api/generate"
TEMPERATURE = 0
NUM_PREDICT = 20
EVAL_SPLIT = "test"
DATA_FILE = Path("data/items.jsonl")
RESULTS_FILE = Path("results/per_item.csv")

# Load dataset
def load_items():

    items = []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            item = json.loads(line)

            if item["split"] == EVAL_SPLIT:
                items.append(item)

    return items

# Call Ollama
def call_model(model: str, prompt: str):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": NUM_PREDICT,
        },
    }

    start = time.perf_counter()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        latency_ms = (time.perf_counter() - start) * 1000

        output_text = data.get("response", "").strip()

        generated_tokens = data.get("eval_count", 0)
        eval_duration_ns = data.get("eval_duration", 0)

        eval_duration_seconds = eval_duration_ns / 1_000_000_000

        if eval_duration_seconds > 0:
            tokens_per_second = (
                generated_tokens / eval_duration_seconds
            )
        else:
            tokens_per_second = 0.0

        return (
            output_text,
            latency_ms,
            generated_tokens,
            tokens_per_second,
            "",
        )

    except Exception as exc:
        latency_ms = (time.perf_counter() - start) * 1000

        return (
            "",
            latency_ms,
            0,
            0.0,
            str(exc),
        )

# Save results
def save_results(rows):

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "model",
        "item_id",
        "split",
        "expected",
        "output",
        "correct",
        "status",
        "latency_ms",
        "generated_tokens",
        "tokens_per_second",
    ]

    with RESULTS_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

# Main
def main():

    items = load_items()

    print(f"Loaded {len(items)} {EVAL_SPLIT} items.")
    print()

    all_results = []

    for model in MODELS:

        print("=" * 70)
        print(f"MODEL: {model}")
        print("=" * 70)

        for index, item in enumerate(items, start=1):

            prompt = build_prompt(item["clause"])

            print(
                f"[{index}/{len(items)}] "
                f"{model} | item {item['id']}",
                end=" ... ",
                flush=True,
            )

            (
                output,
                latency_ms,
                generated_tokens,
                tokens_per_second,
                error,
            ) = call_model(
                model,
                prompt,
            )

            if error:

                correct = False
                status = "timeout_or_error"

                output = ""

                print(
                    f"ERROR "
                    f"({latency_ms:.0f} ms)"
                )

            else:

                correct, status = score(
                    output,
                    item["label"],
                )

                print(
                    f"{status} "
                    f"({latency_ms:.0f} ms)"
                )

            all_results.append(
                {
                    "model": model,
                    "item_id": item["id"],
                    "split": item["split"],
                    "expected": item["label"],
                    "output": output,
                    "correct": correct,
                    "status": status,
                    "latency_ms": round(
                        latency_ms,
                        3,
                    ),
                    "generated_tokens": generated_tokens,
                    "tokens_per_second": round(
                        tokens_per_second,
                        3,
                    ),
                }
            )

    save_results(all_results)

    print()
    print("=" * 70)
    print("Evaluation complete.")
    print(f"Results saved to: {RESULTS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
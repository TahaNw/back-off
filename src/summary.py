import csv
import statistics
from pathlib import Path

RESULTS_FILE = Path("results/per_item.csv")
SUMMARY_FILE = Path("results/summary.csv")

def percentile(values, percentile):

    values = sorted(values)

    if not values:
        return 0.0

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * percentile / 100

    lower = int(position)
    upper = lower + 1

    if upper >= len(values):
        return values[lower]

    fraction = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower]) * fraction
    )


def load_results():

    with RESULTS_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        return list(csv.DictReader(file))


def build_summary(rows):

    models = []

    for row in rows:
        if row["model"] not in models:
            models.append(row["model"])

    summaries = []

    for model in models:

        model_rows = [
            row for row in rows
            if row["model"] == model
        ]

        total = len(model_rows)

        correct = sum(
            row["correct"].lower() == "true"
            for row in model_rows
        )

        wrong = sum(
            row["status"] == "wrong"
            for row in model_rows
        )

        parse_errors = sum(
            row["status"] == "parse_error"
            for row in model_rows
        )

        errors = sum(
            row["status"] == "timeout_or_error"
            for row in model_rows
        )

        latencies = [
            float(row["latency_ms"])
            for row in model_rows
        ]

        token_speeds = [
            float(row["tokens_per_second"])
            for row in model_rows
            if float(row["tokens_per_second"]) > 0
        ]

        accuracy = correct / total

        summaries.append(
            {
                "model": model,
                "total_items": total,
                "correct": correct,
                "wrong": wrong,
                "parse_errors": parse_errors,
                "timeout_or_error": errors,
                "accuracy": round(accuracy, 4),
                "p50_latency_ms": round(
                    percentile(latencies, 50),
                    3,
                ),
                "p95_latency_ms": round(
                    percentile(latencies, 95),
                    3,
                ),
                "average_tokens_per_second": round(
                    statistics.mean(token_speeds),
                    3,
                ),
            }
        )

    return summaries


def save_summary(summaries):

    SUMMARY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "model",
        "total_items",
        "correct",
        "wrong",
        "parse_errors",
        "timeout_or_error",
        "accuracy",
        "p50_latency_ms",
        "p95_latency_ms",
        "average_tokens_per_second",
    ]

    with SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(summaries)

def main():

    rows = load_results()

    summaries = build_summary(rows)

    save_summary(summaries)

    print()
    print("=" * 90)
    print("BENCHMARK SUMMARY")
    print("=" * 90)

    for summary in summaries:

        print(
            f"{summary['model']}: "
            f"accuracy={summary['accuracy']:.2%}, "
            f"p50={summary['p50_latency_ms']:.0f} ms, "
            f"p95={summary['p95_latency_ms']:.0f} ms, "
            f"tokens/sec={summary['average_tokens_per_second']:.2f}"
        )

    print()
    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
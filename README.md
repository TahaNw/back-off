# CS496 AI Engineering — Project 0: The Bake-Off

## Project Overview

This project evaluates three locally hosted LLMs on a legal clause classification task.

The task is to classify each legal clause into exactly one predefined category. The same prompt, dataset, generation settings, parser, and evaluation procedure are used for all three models.

## Task

### Legal Clause Classification

Given a contract clause, the model must classify it into exactly one of these categories:

- CONFIDENTIALITY
- TERMINATION
- PAYMENT
- LIABILITY
- INDEMNIFICATION
- INTELLECTUAL_PROPERTY
- GOVERNING_LAW
- DATA_PROTECTION
- WARRANTY
- NON_COMPETE

### Example

**Input:**

> The customer shall pay all invoices within thirty days of receipt.

**Expected output:**
```text
PAYMENT
```

## Dataset

The dataset is stored in:
```text
data/items.jsonl
```

It contains:

- 100 total items
- 20 development items
- 80 test items
- 10 categories
- 10 items per category

Only the **80 test items** are used for the final benchmark.

The labeling definitions and labeling rules are documented in:
```text
data/labeling_note.md
```

## Models

All three models are installed and executed locally using Ollama.

```text
qwen2.5:7b
qwen2.5:3b
phi3.5:latest
```

## Hardware

The benchmark was executed on a system with:

```text
GPU: NVIDIA RTX 3060
VRAM: 12 GB
```

## Setup

Install the Python dependency:

```powershell
python -m pip install requests
```

Make sure Ollama is installed and the three models are available locally:

```powershell
ollama list
```

The expected models are:

```text
qwen2.5:7b
qwen2.5:3b
phi3.5:latest
```

## Running the Benchmark

From the project root:

```powershell
python src/run.py
```

The benchmark runs all 80 test items sequentially for each model.

This produces:

```text
results/per_item.csv
```

## Generating the Summary

```powershell
python src/summary.py
```

This produces:

```text
results/summary.csv
```

## Evaluation Settings

The same settings are used for all models:

```text
Temperature: 0
Maximum generated tokens: 20
Evaluation split: test
```

The prompt is defined once in:

```text
src/prompt.py
```

The automatic scoring logic is defined in:

```text
src/score.py
```

A prediction is counted as correct only when the model returns exactly one valid category after basic whitespace and case normalization.

## Benchmark Results

| Model | Correct | Accuracy | p50 Latency | p95 Latency | Tokens/sec |
|---|---:|---:|---:|---:|---:|
| `qwen2.5:7b` | 78/80 | 97.50% | 3262 ms | 3701 ms | 9.75 |
| `qwen2.5:3b` | 68/80 | 85.00% | 2321 ms | 2382 ms | 39.38 |
| `phi3.5:latest` | 77/80 | 96.25% | 2729 ms | 3029 ms | 19.42 |

The complete per-item results are stored in:

```text
results/per_item.csv
```

The summary is stored in:

```text
results/summary.csv
```

## Project Structure

```text
back-off/
├── .gitignore
├── data/
│   ├── items.jsonl
│   └── labeling_note.md
├── postmortem.md
├── README.md
├── report.md
├── results/
│   ├── per_item.csv
│   └── summary.csv
└── src/
    ├── error_examples.py
    ├── prompt.py
    ├── run.py
    ├── score.py
    └── summary.py
```

### Source Files

- `src/prompt.py` — defines the common classification prompt and categories.
- `src/run.py` — runs the benchmark against all three Ollama models.
- `src/score.py` — automatically parses and scores model outputs.
- `src/summary.py` — calculates accuracy and latency statistics.
- `src/error_examples.py` — displays representative model errors.

### Data Files

- `data/items.jsonl` — benchmark dataset.
- `data/labeling_note.md` — category definitions and labeling rules.

### Results

- `results/per_item.csv` — raw result for every model/item evaluation.
- `results/summary.csv` — aggregated benchmark results.

## Reproducibility

To reproduce the benchmark:

1. Install Ollama.
2. Install the three specified models.
3. Install the Python `requests` package.
4. Place the project in the required directory.
5. Run:

```powershell
python src/run.py
```

6. Generate the summary:

```powershell
python src/summary.py
```
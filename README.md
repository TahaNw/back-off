# CS496 AI Engineering — Project 0: The Bake-Off

## Project Overview

This project evaluates three locally hosted Large Language Models (LLMs) on a legal clause classification task.

The task is to classify each legal clause into exactly one predefined category. The same prompt, dataset, generation settings, parser, and evaluation procedure are used for all three models.

Unlike the original assignment setup, this implementation uses **three local models through Ollama** and does not use external API services or API keys.

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

The model must return only the category name, with no explanation or additional text.

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

The clauses are synthetic contract-style examples and do not contain confidential customer information.

The labeling definitions and labeling rules are documented in:

```text
data/labeling_note.md
```

## Models

All three models are installed and executed locally using Ollama.

| Model | Size | Role |
|---|---:|---|
| `qwen2.5:7b` | 7B | Larger local model |
| `qwen2.5:3b` | 3B | Smaller local model |
| `phi3.5:latest` | 3.8B class | Smaller local model |

The exact Ollama model tags used by the benchmark are:

```text
qwen2.5:7b
qwen2.5:3b
phi3.5:latest
```

No external model API is used.

## Hardware

The benchmark was executed on a system with:

```text
GPU: NVIDIA RTX 3060
VRAM: 12 GB
```

Ollama was used as the local model runtime.

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

The file contains one row for every model/item evaluation.

## Generating the Summary

After the benchmark finishes:

```powershell
python src/summary.py
```

This produces:

```text
results/summary.csv
```

The summary contains accuracy, latency, error counts, and average generation speed.

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

The same prompt is used for every model.

The automatic scoring logic is defined in:

```text
src/score.py
```

A prediction is counted as correct only when the model returns exactly one valid category after basic whitespace and case normalization.

Explanations, multiple categories, invalid categories, refusals, timeouts, and other invalid outputs are not manually corrected.

## Benchmark Results

The final benchmark contains 80 test items per model, for a total of 240 model evaluations.

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

## Error Examples

### `qwen2.5:7b`

**Item 044**

Expected:

```text
INDEMNIFICATION
```

Model output:

```text
LIABILITY
```

Clause:

> The service provider shall defend and hold the customer harmless from claims alleging that the services caused bodily injury due to the provider's negligence.

**Item 095**

Expected:

```text
NON_COMPETE
```

Model output:

```text
TERMINATION
```

Clause:

> For six months following termination, the executive shall not provide competing services to customers within the defined market.

### `qwen2.5:3b`

**Item 038**

Expected:

```text
LIABILITY
```

Model output:

```text
PAYMENT
```

**Item 039**

Expected:

```text
LIABILITY
```

Model output:

```text
TERMINATION
```

**Item 044**

Expected:

```text
INDEMNIFICATION
```

Model output:

```text
LIABILITY
```

### `phi3.5:latest`

**Item 044**

Expected:

```text
INDEMNIFICATION
```

Model output:

```text
WARRANTY
```

**Item 086**

Expected:

```text
WARRANTY
```

Model output:

```text
INTELLECTUAL_PROPERTY
```

**Item 089**

Expected:

```text
WARRANTY
```

Model output:

```text
You are a legal clause classification system with advanced
```

This was counted as a parse error because the output did not contain exactly one valid category.

More detailed error information can be generated with:

```powershell
python src/error_examples.py
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

## Cost Analysis

This implementation does not use external API models or API tokens.

The original assignment includes API cost analysis. Since all three models in this implementation are run locally through Ollama, API token costs are not applicable.

No artificial API prices or hardware/electricity costs are included in the results.

This is an explicit implementation deviation from the original API-based comparison requirement.

## Limitations

The benchmark uses synthetic legal clauses rather than real confidential business contracts.

The test set contains 80 items, so the measured accuracy and latency values should be interpreted within the scope of this dataset and hardware configuration.

The benchmark measures classification accuracy and runtime performance. It does not evaluate the legal validity of the clauses or provide legal advice.

## Contributions

Contributions should be documented here according to the actual work performed by each team member.

Example:

```text
- Name: dataset preparation and labeling
- Name: benchmark implementation and Ollama integration
- Name: evaluation analysis and report
```

Replace the example entries with the actual team members and contributions.

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

The benchmark uses the same 80 test items, prompt, generation settings, parser, and evaluation procedure for all three models.
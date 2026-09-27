# CS496 AI Engineering — Project 0: The Bake-Off

## 1. Task

The task is **legal clause classification**. Given a short contract clause, the model must classify it into exactly one of ten predefined categories:

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

For example, the clause *“The customer shall pay all invoices within thirty days of receipt”* should be classified as `PAYMENT`.

The benchmark uses automatic exact-match scoring. A response is correct only when it contains exactly one valid category after basic whitespace and case normalization. Explanations, invalid labels, multiple labels, refusals, and errors are counted as incorrect.

## 2. Data and Evaluation

The dataset contains **100 synthetic contract-style clauses**:

- 20 development items
- 80 test items
- 10 categories
- 10 items per category

Only the 80 test items were used for the final benchmark. The dataset was created specifically for this project and does not contain confidential customer information.

Category definitions and labeling rules are documented in `data/labeling_note.md`.

The benchmark uses the same 80 test items for every model. No failed items were removed and no model output was manually corrected.

## 3. Setup and Models

All three models were run locally using **Ollama**, rather than using external API services.

| Model | Runtime | Hardware |
|---|---|---|
| `qwen2.5:7b` | Ollama | NVIDIA RTX 3060 12 GB |
| `qwen2.5:3b` | Ollama | NVIDIA RTX 3060 12 GB |
| `phi3.5:latest` | Ollama | NVIDIA RTX 3060 12 GB |

The same prompt was used for all models. The generation settings were:

- Temperature: 0
- Maximum generated tokens: 20
- Sequential evaluation
- One model call per item
- Same parser and automatic scoring function

The prompt is implemented in `src/prompt.py`, while automatic scoring is implemented in `src/score.py`.

## 4. Results

Each model classified the same 80 test items, resulting in 240 total model evaluations.

| Model | Correct | Accuracy | p50 Latency | p95 Latency | Tokens/sec |
|---|---:|---:|---:|---:|---:|
| `qwen2.5:7b` | 78/80 | 97.50% | 3262 ms | 3701 ms | 9.75 |
| `qwen2.5:3b` | 68/80 | 85.00% | 2321 ms | 2382 ms | 39.38 |
| `phi3.5:latest` | 77/80 | 96.25% | 2729 ms | 3029 ms | 19.42 |

The results show a measurable trade-off between classification accuracy and generation speed. `qwen2.5:7b` had the highest measured accuracy in this experiment, while `qwen2.5:3b` had the highest measured token generation rate. `phi3.5:latest` produced accuracy close to the 7B model while having lower latency than the 7B model.

These measurements apply specifically to this dataset, model versions, Ollama configuration, and RTX 3060 hardware.

## 5. Representative Errors

### `qwen2.5:7b`

**Item 044**

Expected: `INDEMNIFICATION`

Output: `LIABILITY`

> The service provider shall defend and hold the customer harmless from claims alleging that the services caused bodily injury due to the provider's negligence.

**Item 095**

Expected: `NON_COMPETE`

Output: `TERMINATION`

> For six months following termination, the executive shall not provide competing services to customers within the defined market.

### `qwen2.5:3b`

**Item 038**

Expected: `LIABILITY`

Output: `PAYMENT`

> A party's aggregate liability under this agreement shall not exceed fifty thousand euros.

**Item 039**

Expected: `LIABILITY`

Output: `TERMINATION`

> The service provider shall not be liable for delays caused exclusively by events outside its reasonable control.

**Item 044**

Expected: `INDEMNIFICATION`

Output: `LIABILITY`

> The service provider shall defend and hold the customer harmless from claims alleging that the services caused bodily injury due to the provider's negligence.

### `phi3.5:latest`

**Item 044**

Expected: `INDEMNIFICATION`

Output: `WARRANTY`

> The service provider shall defend and hold the customer harmless from claims alleging that the services caused bodily injury due to the provider's negligence.

**Item 086**

Expected: `WARRANTY`

Output: `INTELLECTUAL_PROPERTY`

> The supplier represents that it possesses all licenses necessary to provide the contracted services.

**Item 089**

Expected: `WARRANTY`

Output: `You are a legal clause classification system with advanced`

This last response was counted as a parse error because it did not contain exactly one valid category.

## 6. Model Selection Considerations

The measurements provide different trade-offs rather than a single universal result.

`qwen2.5:7b` recorded the highest accuracy at 97.50%, with 78 correct classifications out of 80. Its p50 latency was 3262 ms and its average generation speed was 9.75 tokens/sec.

`qwen2.5:3b` recorded 85.00% accuracy and the highest generation speed at 39.38 tokens/sec. Its p50 latency was also the lowest at 2321 ms.

`phi3.5:latest` recorded 96.25% accuracy, with a p50 latency of 2729 ms and an average generation speed of 19.42 tokens/sec.

Therefore, the appropriate model depends on the application's requirements. A workload that prioritizes measured classification accuracy may place greater importance on the accuracy results, while a latency-sensitive workload may place greater importance on response time and generation speed. If the workload or hardware changes, the benchmark should be repeated before making a deployment decision.

## 7. Cost and Scope

This implementation uses three locally hosted Ollama models and does not use external API services or API tokens.

Therefore, API token pricing is not included in this comparison. Hardware and electricity costs are also not estimated because this project focuses on the measured local-model performance.

This is a deliberate deviation from the original API-based cost-analysis requirement.

## 8. Conclusion

The bake-off successfully established a reproducible evaluation pipeline for comparing three locally hosted LLMs on legal clause classification.

Using the same dataset, prompt, generation settings, parser, and scoring procedure produced measurable differences in accuracy and runtime performance. The results demonstrate why both task accuracy and system performance should be considered when evaluating local LLMs.

The complete per-item results are stored in `results/per_item.csv`, and the aggregated measurements are stored in `results/summary.csv`.
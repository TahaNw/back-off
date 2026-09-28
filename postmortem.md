# Project 0 — Bake-Off Postmortem

## What Worked

The benchmark pipeline successfully evaluated all three local models on the same 80 test items. The models were run sequentially through Ollama using the same classification prompt, temperature setting, maximum output-token limit, dataset, parser, and scoring procedure.

The automatic evaluation produced clear differences between the models. `qwen2.5:7b` achieved 78/80 correct (97.50%), `phi3.5:latest` achieved 77/80 correct (96.25%), and `qwen2.5:3b` achieved 68/80 correct (85.00%).

The results were saved automatically to `results/per_item.csv`, while `results/summary.csv` contains the aggregated accuracy and performance measurements. This made it possible to inspect individual errors without manually changing benchmark results.

The local setup also worked without external API services. All three models were installed through Ollama and evaluated on the same RTX 3060 12 GB system.

## What Went Wrong

The smaller `qwen2.5:3b` model produced substantially more classification errors than the other two models. Its accuracy was 85.00%, compared with 97.50% for `qwen2.5:7b` and 96.25% for `phi3.5:latest`.

Some errors occurred on clauses containing terminology associated with more than one category. For example, item 044 was labeled `INDEMNIFICATION` because it contains a duty to defend and hold another party harmless, but the models sometimes associated the clause with `LIABILITY` or `WARRANTY`. This shows that closely related legal concepts can make classification more difficult.

There was also an output-format failure from `phi3.5:latest`. For item 089, the model returned an incomplete explanatory response instead of one of the allowed category names. The scoring system correctly treated this as a parse error rather than manually correcting the response.

The local models also showed different latency and generation-speed characteristics. The larger `qwen2.5:7b` model had the highest measured accuracy but also the slowest generation speed, while `qwen2.5:3b` generated tokens substantially faster but had lower accuracy.

## What We Would Change

If we repeated the project, we would first expand the test dataset with more difficult examples involving closely related legal categories such as `LIABILITY` and `INDEMNIFICATION`, as well as `WARRANTY` and `INTELLECTUAL_PROPERTY`.

We would also include more examples designed to test strict output formatting. This would make it easier to measure how often a model produces a correct classification but fails the required output format.

Another improvement would be to record additional hardware information, such as GPU utilization and memory usage, during the benchmark. This would provide more context for comparing the local models' runtime characteristics.

## Main Lesson

The main lesson from the bake-off is that model size, accuracy, and generation speed involve measurable trade-offs. In this experiment, the 7B Qwen model achieved the highest measured accuracy, while the 3B Qwen model produced tokens much faster but made more classification errors.

The benchmark also demonstrated the importance of using an identical evaluation procedure. Using the same prompt, data, settings, parser, and automatic scoring function makes the measured differences between models easier to reproduce and interpret.

Finally, the project showed that a simple local evaluation harness can provide useful quantitative evidence for comparing LLMs without relying on API services. The results should still be interpreted within the limits of the specific dataset, task, models, and hardware used in this experiment.
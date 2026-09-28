# Legal Clause Classification — Labeling Guide

## Task

Each item contains a legal clause. The task is to assign exactly one predefined category to the clause.
The classifier must return exactly one of the following labels:
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

## Label Definitions

### CONFIDENTIALITY
Clauses concerning confidential information or obligations to keep information confidential.
### TERMINATION
Clauses concerning ending or cancelling the agreement.
### PAYMENT
Clauses concerning fees, prices or payment deadlines.
### LIABILITY
Clauses concerning responsibility for damages and losses.
### INDEMNIFICATION
Clauses requiring one party to defend or hold another party harmless against specified claims.
### INTELLECTUAL_PROPERTY
Clauses concerning ownership, licensing or use of intellectual property.
### GOVERNING_LAW
Clauses specifying which country's, state's, or jurisdiction's law governs the agreement.
### DATA_PROTECTION
Clauses concerning personal data, privacy, and data processing.
### WARRANTY
Clauses containing warranties, guarantees, or assurances.
### NON_COMPETE
Clauses restricting a party from competing with another party.

## Labeling Rules

1. Assign exactly one label to every item.
2. Select the label that represents the main legal subject of the clause.
3. Prefer explicit wording.
4. Each clause should be written so that a careful reviewer can identify one intended category.
5. Avoid clauses whose correct category depends on specialized legal interpretation.
6. Avoid clauses that equally represent two or more categories.
7. If a clause contains multiple concepts, the intended category should be the clearly dominant legal obligation.
8. The expected answer is the exact label written in uppercase with underscores where applicable.
9. No LLM is used to determine the label.
10. Every label is checked by two human reviewers.

## Output Format

The model must return exactly one category name and no explanation.

Example:

CONFIDENTIALITY

An answer containing an explanation, multiple labels, an invalid label, refusal, or otherwise unparseable output is counted as incorrect.
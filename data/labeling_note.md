# Legal Clause Classification — Labeling Guide

## Task

Each item contains one short legal or contractual clause. The task is to assign exactly one predefined category to the clause.

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
Clauses concerning confidential information, secrecy, disclosure restrictions, or obligations to keep information confidential.

### TERMINATION
Clauses concerning ending, terminating, cancelling, or ending the agreement or a party's contractual relationship.

### PAYMENT
Clauses concerning fees, prices, invoices, payment schedules, compensation, or payment deadlines.

### LIABILITY
Clauses concerning responsibility for damages, losses, liability limitations, exclusions of liability, or monetary responsibility for harm.

### INDEMNIFICATION
Clauses requiring one party to defend, indemnify, reimburse, or hold another party harmless against specified claims, damages, losses, or expenses.

### INTELLECTUAL_PROPERTY
Clauses concerning ownership, licensing, assignment, or use of intellectual property such as copyrights, patents, trademarks, inventions, software, or other protected works.

### GOVERNING_LAW
Clauses specifying which country's, state's, or jurisdiction's law governs the agreement.

### DATA_PROTECTION
Clauses concerning personal data, privacy, data processing, data security, or compliance with data-protection requirements.

### WARRANTY
Clauses containing warranties, guarantees, representations, or assurances about goods, services, performance, or contractual conditions.

### NON_COMPETE
Clauses restricting a party from competing with another party or engaging in specified competing business activities.

## Labeling Rules

1. Assign exactly one label to every item.
2. Select the label that represents the main legal subject of the clause.
3. Prefer explicit wording over assumptions about the broader agreement.
4. Each clause should be written so that a careful reviewer can identify one intended category.
5. Avoid clauses whose correct category depends on specialized legal interpretation.
6. Avoid clauses that equally represent two or more categories.
7. If a clause contains multiple concepts, the intended category should be the clearly dominant legal obligation or subject.
8. The expected answer is the exact label written in uppercase with underscores where applicable.
9. No LLM is used to determine the gold label.
10. Every gold label is checked by two human reviewers.

## Output Format

The model must return exactly one category name and no explanation.

Example:

CONFIDENTIALITY

An answer containing an explanation, multiple labels, an invalid label, refusal, or otherwise unparseable output is counted as incorrect.
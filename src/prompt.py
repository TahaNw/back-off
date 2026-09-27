CATEGORIES = [
    "CONFIDENTIALITY",
    "TERMINATION",
    "PAYMENT",
    "LIABILITY",
    "INDEMNIFICATION",
    "INTELLECTUAL_PROPERTY",
    "GOVERNING_LAW",
    "DATA_PROTECTION",
    "WARRANTY",
    "NON_COMPETE",
]

def build_prompt(clause: str) -> str:

    categories = "\n".join(f"- {category}" for category in CATEGORIES)

    return f"""You are a legal clause classification system.

Classify the following legal clause into exactly ONE of the categories below.

Categories:
{categories}

Rules:
1. Choose exactly one category.
2. Return only the category name.
3. Do not provide an explanation.
4. Do not include punctuation.
5. Do not return multiple categories.

Legal clause:
{clause}

Category:"""
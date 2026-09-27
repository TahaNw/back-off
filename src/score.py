from prompt import CATEGORIES

def normalize_prediction(output: str) -> str:

    if not output:
        return ""

    return output.strip().upper()


def parse_prediction(output: str) -> str | None:

    normalized = normalize_prediction(output)

    if normalized in CATEGORIES:
        return normalized

    return None

def score(output: str, expected: str) -> tuple[bool, str]:

    prediction = parse_prediction(output)

    if prediction is None:
        return False, "parse_error"

    if prediction == expected:
        return True, "correct"

    return False, "wrong"
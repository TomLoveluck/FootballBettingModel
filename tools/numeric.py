
def safe_division(numerator, denominator, default):

    if denominator == 0:
        return default
    else:
        return numerator / denominator

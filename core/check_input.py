

def validate_input(rd_spend, administration, marketing_spend, state):
    errors = []

    # Validate R&D Spend
    if not isinstance(rd_spend, (int, float)) or rd_spend < 0:
        errors.append("R&D Spend must be a non-negative number")

    # Validate Administration
    if not isinstance(administration, (int, float)) or administration < 0:
        errors.append("Administration must be a non-negative number")

    # Validate Marketing Spend
    if not isinstance(marketing_spend, (int, float)) or marketing_spend < 0:
        errors.append("Marketing Spend must be a non-negative number")

    # Validate State
    if not isinstance(state, str) or not state.strip():
        errors.append("State must be a non-empty string")

    return errors

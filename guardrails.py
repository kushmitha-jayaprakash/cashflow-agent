def validate_plan(plan):
    """
    Validate the proposed cash-flow plan.

    The agent may suggest scheduling changes,
    but it must never perform financial actions.
    """

    forbidden_actions = [
        "auto-debit",
        "make payment",
        "pay",
        "payment",
        "send message",
        "message landlord",
        "contact landlord",
        "transfer money",
        "transfer funds",
        "withdraw money"
    ]

    safe_plan = []

    for item in plan:
        checked_item = item.copy()
        action = str(checked_item.get("action", "")).lower()

        if any(forbidden in action for forbidden in forbidden_actions):
            checked_item["action"] = "Human approval required"

        safe_plan.append(checked_item)

    return safe_plan
if __name__ == "__main__":
    test_plan = [
        {
            "date": "30 Sep",
            "description": "Landlord Rent",
            "amount": 18000,
            "action": "Make payment to landlord"
        },
        {
            "date": "01 Oct",
            "description": "Electricity",
            "amount": 3200,
            "action": "Keep funds ready"
        },
        {
            "date": "02 Oct",
            "description": "Airtel Recharge",
            "amount": 999,
            "action": "Shift by 1 day to avoid collision"
        }
    ]

    checked_plan = validate_plan(test_plan)

    print("\nGuardrail test:")
    for item in checked_plan:
        print(item)
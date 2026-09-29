import pandas as pd
def detect_food_spike(transactions):
    food_keywords = ["swiggy", "zomato", "food"]

    food_transactions = transactions[
        transactions["description"]
        .str.lower()
        .str.contains("|".join(food_keywords), na=False)
    ]

    current_food_spend = food_transactions["amount"].sum()

    # Example of the household's usual weekly food spending
    usual_food_spend = 1900

    spike_ratio = current_food_spend / usual_food_spend

    if spike_ratio >= 3:
        return {
            "category": "Food",
            "current_spend": current_food_spend,
            "usual_spend": usual_food_spend,
            "ratio": spike_ratio,
            "message": "Food spending is about 3× the usual weekly amount."
        }

    return None
def detect_bill_collisions(transactions):
    bill_keywords = [
        "rent",
        "electricity",
        "recharge",
        "water",
        "internet",
        "bill"
    ]

    bills = transactions[
        transactions["description"]
        .str.lower()
        .str.contains("|".join(bill_keywords), na=False)
    ].copy()

    bills = bills.sort_values("date")

    collisions = []

    for i in range(len(bills)):
        for j in range(i + 1, len(bills)):
            if bills.iloc[j]["date"] == bills.iloc[i]["date"]:
                collisions.append({
                    "bill_1": bills.iloc[i]["description"],
                    "date_1": bills.iloc[i]["date"],
                    "amount_1": bills.iloc[i]["amount"],
                    "bill_2": bills.iloc[j]["description"],
                    "date_2": bills.iloc[j]["date"],
                    "amount_2": bills.iloc[j]["amount"]
                })

    return collisions
def create_seven_day_plan(transactions):
    """
    Create a 7-day plan that separates bill dates when possible.

    Demo assumption:
    - Rent is fixed.
    - Electricity is fixed.
    - Recharge can be shifted by 1 day.
    """

    bill_keywords = [
        "rent",
        "electricity",
        "recharge",
        "water",
        "internet",
        "bill"
    ]

    bills = transactions[
        transactions["description"]
        .str.lower()
        .str.contains("|".join(bill_keywords), na=False)
        & (transactions["type"] == "expense")
    ].copy()

    bills = bills.sort_values("date")

    plan = []
    occupied_dates = set()

    for _, row in bills.iterrows():
        original_date = row["date"]
        planned_date = original_date
        description = row["description"].lower()

        # Recharge is the only flexible bill in our demo.
        if "recharge" in description:
            if original_date in occupied_dates:
                planned_date = original_date + pd.Timedelta(days=1)

        occupied_dates.add(planned_date)

        plan.append({
            "date": planned_date.strftime("%d %b"),
            "description": row["description"],
            "amount": row["amount"],
            "original_date": original_date.strftime("%d %b"),
            "action": (
                "Shift by 1 day to avoid collision"
                if planned_date != original_date
                else "Keep funds ready"
            )
        })

    return plan
    

    bills = transactions[
        transactions["description"]
        .str.lower()
        .str.contains("|".join(bill_keywords), na=False)
        & (transactions["type"] == "expense")
    ].copy()

    bills = bills.sort_values("date")

    plan = []

    for _, row in bills.iterrows():
        plan.append({
            "date": row["date"].strftime("%d %b"),
            "description": row["description"],
            "amount": row["amount"],
            "action": "Keep funds ready"
        })

    return plan

def find_unmatched_transactions(transactions):
    known_keywords = [
        "swiggy",
        "zomato",
        "rent",
        "electricity",
        "recharge",
        "salary",
        "water",
        "internet",
        "food",
        "bill"
    ]

    unmatched = transactions[
        ~transactions["description"]
        .str.lower()
        .str.contains("|".join(known_keywords), na=False)
    ].copy()

    return unmatched
def create_cashflow_calendar(transactions):
    expenses = transactions[transactions["type"] == "expense"].copy()

    calendar = (
        expenses
        .groupby("date", as_index=False)["amount"]
        .sum()
        .sort_values("date")
    )

    calendar["date"] = calendar["date"].dt.strftime("%d %b")

    return calendar
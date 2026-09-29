import re
import pandas as pd


def parse_sms(sms_text):
    transactions = []

    lines = sms_text.splitlines()

    for line in lines:
        amount_match = re.search(r"₹\s*([\d,]+(?:\.\d+)?)", line)

        date_match = re.search(
            r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})",
            line
        )

        if not amount_match or not date_match:
            continue

        amount = float(amount_match.group(1).replace(",", ""))

        day, month, year = date_match.groups()
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        lower_line = line.lower()

        if "swiggy" in lower_line:
            description = "Swiggy"

        elif "zomato" in lower_line:
            description = "Zomato"

        elif "electricity" in lower_line or "eb " in lower_line:
            description = "Electricity"

        elif "recharge" in lower_line:
            description = "Recharge"

        else:
            description = "Unknown SMS transaction"

        transactions.append({
            "date": date,
            "person": "SMS",
            "description": description,
            "amount": amount,
            "type": "expense"
        })

    return pd.DataFrame(transactions)
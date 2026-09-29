import fitz
import re


def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()

    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_bill_details(text):
    details = {
        "bill_type": "Unknown",
        "amount": None,
        "due_date": None
    }

    text_lower = text.lower()

    # Detect bill type
    if "electricity" in text_lower or "electric" in text_lower:
        details["bill_type"] = "Electricity"

    elif "rent" in text_lower:
        details["bill_type"] = "Rent"

    elif "recharge" in text_lower:
        details["bill_type"] = "Recharge"

    # Detect amount
    amount_match = re.search(
        r"(?:total|amount|payable|due)[^\d₹]{0,20}₹?\s*([\d,]+(?:\.\d+)?)",
        text_lower
    )

    if amount_match:
        amount_text = amount_match.group(1).replace(",", "")
        details["amount"] = float(amount_text)

    # Detect a simple DD/MM/YYYY or DD-MM-YYYY date
    date_match = re.search(
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b",
        text
    )

    if date_match:
        details["due_date"] = date_match.group(1)

    return details
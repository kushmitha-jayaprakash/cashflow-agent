import streamlit as st
st.set_page_config(
    page_title="CashFlow Guardian",
    page_icon="💰",
    layout="wide"
)

from data_reader import load_transactions

from rules import (
    detect_food_spike,
    detect_bill_collisions,
    create_seven_day_plan,
    find_unmatched_transactions,
    create_cashflow_calendar
)

from guardrails import validate_plan
from llm import generate_weekly_note
from pdf_reader import extract_text_from_pdf,extract_bill_details
from sms_parser import parse_sms
st.title("💰 CashFlow Guardian")
st.caption("7-Day Household Cash-Flow Agent")

st.info(
    "Analyzes household cash flow, detects bill collisions and spending spikes, "
    "and creates a 7-day plan — without making payments automatically."
)

transactions = load_transactions()

st.subheader("Transactions")
st.dataframe(transactions)

# Detect unusual food spending
food_spike = detect_food_spike(transactions)

st.subheader("⚠️ Alerts")

if food_spike:
    st.warning(
        f"Food spending is ₹{food_spike['current_spend']:.0f}, "
        f"compared with the usual ₹{food_spike['usual_spend']:.0f}. "
        f"That's about {food_spike['ratio']:.1f}× the usual amount."
    )
else:
    st.success("No major spending spike detected.")
# Detect original bill collisions
bill_collisions = detect_bill_collisions(transactions)

# Create and validate the resolved 7-day plan
seven_day_plan = create_seven_day_plan(transactions)
seven_day_plan = validate_plan(seven_day_plan)

st.subheader("📅 Bill Collision Resolution")

if bill_collisions:
    st.error("⚠️ Bill collision detected in the original schedule.")

    for collision in bill_collisions:
        st.write(
            f"**Original collision:** "
            f"{collision['bill_1']} (₹{collision['amount_1']:.0f}) "
            f"and {collision['bill_2']} (₹{collision['amount_2']:.0f}) "
            f"occur within 1 day."
        )

    st.info("🤖 Proposed resolution:")

    for item in seven_day_plan:
        if "Shift by 1 day" in item["action"]:
            st.success(
                f"✅ {item['description']} → {item['date']} "
                f"(moved from {item['original_date']} to avoid the collision)"
            )

    st.success(
        "✅ The proposed 7-day plan separates the flexible bill from "
        "the original collision."
    )

else:
    st.success("✅ No bill collisions detected.")

st.subheader("🗓️ Resolved 7-Day Cash-Flow Plan")
st.caption(
    "Demo assumption: recharge is the only flexible bill and may be shifted by 1 day."
)
st.dataframe(
    seven_day_plan,
    use_container_width=True
)

# Generate weekly note
weekly_note = generate_weekly_note(
    seven_day_plan,
    food_spike,
    bill_collisions
)
st.caption("🧪 Demo mode: weekly note uses the local fallback when the LLM API is unavailable.")

st.subheader("📝 Weekly Cash-Flow Note")

st.info(weekly_note)
# Find unmatched transactions
unmatched_transactions = find_unmatched_transactions(transactions)

st.subheader("❓ Unmatched Transactions")

if not unmatched_transactions.empty:
    st.warning(
        "These transactions could not be confidently categorized. "
        "The agent will not guess their category."
    )

    st.dataframe(
        unmatched_transactions[
            ["date", "person", "description", "amount", "type"]
        ],
        use_container_width=True
    )
else:
    st.success("All transactions were categorized.")
    # Cash-flow calendar
cashflow_calendar = create_cashflow_calendar(transactions)

st.subheader("📅 Cash-Flow Calendar")

st.dataframe(
    cashflow_calendar,
    use_container_width=True
)
st.subheader("📄 Upload Bill PDFs")

uploaded_bills = st.file_uploader(
    "Upload one or two bill PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_bills:
    for bill in uploaded_bills:
        bill_text = extract_text_from_pdf(bill)

        st.write(f"**{bill.name}**")

        if bill_text.strip():
            st.success("Bill PDF read successfully.")

            bill_details = extract_bill_details(bill_text)

            st.write("**Detected bill details:**")

            st.write(f"Bill type: {bill_details['bill_type']}")

            if bill_details["amount"] is not None:
                st.write(f"Amount: ₹{bill_details['amount']:.0f}")
            else:
                st.write("Amount: Not confidently detected")

            if bill_details["due_date"]:
                st.write(f"Due date: {bill_details['due_date']}")
            else:
                st.write("Due date: Not confidently detected")

        else:
            st.warning("No readable text was found in this PDF.")

st.subheader("📱 Sample SMS Input")

sms_text = st.text_area(
    "Paste sample bank/UPI SMS messages here",
    placeholder="Example: UPI payment of ₹850 to Swiggy on 29-09-2026"
)

if sms_text.strip():
    sms_transactions = parse_sms(sms_text)

    if not sms_transactions.empty:
        st.success("SMS transactions extracted successfully.")

        st.write("**Extracted SMS transactions:**")
        st.dataframe(
            sms_transactions,
            use_container_width=True
        )
    else:
        st.warning(
            "No transactions could be confidently extracted from the SMS."
        )
st.divider()

st.subheader("🤖 Agent Control")

if st.button("▶️ Run Cash-Flow Analysis", type="primary"):
    st.success("Analysis completed.")

    st.write("✅ Transactions analyzed")
    st.write("✅ Food-spending anomaly checked")
    st.write("✅ Bill collisions checked")
    st.write("✅ 7-day cash-flow plan created")
    st.write("✅ Unmatched transactions identified")
    st.write("✅ Guardrails applied")
    st.write("✅ Weekly note generated")
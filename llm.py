import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_local_note(plan, food_spike, collisions):
    """Local demo mode used when the LLM API is unavailable."""

    note = "Your 7-day cash-flow summary:\n\n"

    if collisions:
        note += (
            "⚠️ Bill collision detected in the original schedule. "
            "The proposed plan separates flexible bills where possible.\n"
        )
    else:
        note += "✅ No bill collisions were detected.\n"

    if food_spike:
        note += (
            f"🍔 Food spending is ₹{food_spike['current_spend']:.0f}, "
            f"compared with the usual ₹{food_spike['usual_spend']:.0f}. "
            f"That is about {food_spike['ratio']:.1f}× the usual amount.\n"
        )

    note += "\nProposed 7-day plan:\n"

    for item in plan:
        action = item["action"]

        if "Shift by 1 day" in action:
            note += (
                f"- {item['date']}: {item['description']} "
                f"₹{item['amount']:.0f} "
                f"(moved from {item['original_date']} to avoid a collision)\n"
            )
        else:
            note += (
                f"- {item['date']}: {item['description']} "
                f"₹{item['amount']:.0f}\n"
            )

    note += (
        "\nThe plan only proposes scheduling changes. "
        "No payments or messages have been sent automatically."
    )

    return note

def generate_weekly_note(plan, food_spike, collisions):
    """
    Generate the weekly note.

    If the API has available credits, use exactly one LLM call.
    Otherwise, use the local demo generator.
    """

    plan_text = "\n".join(
        f"- {item['date']}: {item['description']} ₹{item['amount']:.0f}"
        for item in plan
    )

    collision_text = "\n".join(
        f"- {item['bill_1']} ₹{item['amount_1']:.0f} "
        f"and {item['bill_2']} ₹{item['amount_2']:.0f}"
        for item in collisions
    )

    food_text = (
        f"Food spending: ₹{food_spike['current_spend']:.0f}; "
        f"usual: ₹{food_spike['usual_spend']:.0f}; "
        f"ratio: {food_spike['ratio']:.1f}x."
        if food_spike
        else "No food-spending spike detected."
    )

    prompt = f"""
You are the writing component of a household cash-flow agent.

Write a short, clear 7-day cash-flow note for three PG roommates.

Use ONLY the information provided below.

Important rules:
- Do not invent amounts, dates, bills, income, or transactions.
- The proposed plan is the source of truth for scheduled dates.
- If a bill was shifted, clearly say it was proposed to be shifted.
- Do not claim that a payment was made.
- Do not contact a landlord or any other person.
- Do not recommend automatic payments.
- Keep the note concise and easy to understand.

Food analysis:
{food_text}

Original bill collisions:
{collision_text if collision_text else "No bill collisions detected."}

Resolved 7-day plan:
{plan_text}

End with exactly:
"No payments or messages have been sent automatically."
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text

    except Exception:
        return generate_local_note(plan, food_spike, collisions)
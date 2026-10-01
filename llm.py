import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = None


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

    For now, use the local generator when no API key is available.
    """

    return generate_local_note(plan, food_spike, collisions)
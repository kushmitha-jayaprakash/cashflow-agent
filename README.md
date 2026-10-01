# 💰 CashFlow Guardian

## 7-Day Household Cash-Flow Agent

CashFlow Guardian is a rule-based household cash-flow agent designed for PG roommates and families.

It analyzes transactions, detects spending anomalies and bill collisions, and creates a 7-day cash-flow plan.

## Problem

Household accounts can fail because bills arrive close together, even when total spending is not unusually high.

The agent provides a seven-day warning and proposes a safer schedule.

## What it does

- Reads sample transaction data
- Detects unusual food spending
- Detects bill-date collisions
- Proposes a resolved 7-Day bill schedule
- Reads bill PDFs
- Parses sample UPI/SMS transactions
- Identifies unmatched transactions without guessing
- Generates a short weekly cash-flow note
- Applies guardrails to prevent financial actions

## Demo scenario

The demo uses a PG of three roommates:

- Arun
- Priya
- Rahul

A planted food-spending anomaly is included.

Two transactions are intentionally left unmatched.

## Safety

CashFlow Guardian does not:

- Make payments
- Transfer money
- Auto-debit accounts
- Contact landlords
- Invent bill amounts
- Guess unmatched transactions

The system only proposes a plan for human review.

## Architecture

Transactions / SMS / PDFs
        ↓
Data parsing
        ↓
Rule-based analysis
        ↓
Food anomaly + bill collision detection
        ↓
Collision resolution
        ↓
Guardrails
        ↓
Weekly cash-flow note

The language model is used only for generating the human-readable weekly note.

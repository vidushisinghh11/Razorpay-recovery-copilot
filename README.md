# Recovery Copilot 💸
AI agent that detects failed payments, diagnoses root cause, and executes bounded recovery actions.

## Problem
Revenue loss rarely happens in one step — payments degrade, checkouts get abandoned, subscriptions fail. This agent closes the loop: detect → diagnose → recover.

## How it works
1. Ingests failed payment events (Razorpay test-mode style)
2. Classifies failure reason (insufficient funds, timeout, expired card, drop-off, repeat failure)
3. Triggers bounded action: auto-retry, WhatsApp/SMS nudge, or discount coupon
4. Logs every action with reasoning — full audit trail

## Bar we hit
- Explainable: every action has a one-line reason
- Bounded: max 2 retries, 1 coupon per customer
- Graceful failure: unresolved cases escalate to human, no infinite loops

## Run it
\`\`\`
pip install -r requirements.txt
python src/run_batch.py
\`\`\`
Open `dashboard/index.html` to view live recovery stats.

## Stack
Python, Razorpay Test APIs, LLM-based classification, HTML/JS dashboard
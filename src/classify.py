"""
Classifies a failed payment's reason code into a root-cause bucket
and decides the bounded recovery action + human-readable reasoning.
"""

RULES = {
    "insufficient_funds": {
        "bucket": "transient_funds",
        "action": "retry_later",
        "reason": "Insufficient funds often resolves within hours (salary credit, etc.) - retry after delay."
    },
    "bank_timeout": {
        "bucket": "transient_network",
        "action": "retry_now",
        "reason": "Bank server timeout is usually transient - safe to retry immediately."
    },
    "card_expired": {
        "bucket": "needs_update",
        "action": "send_update_link",
        "reason": "Card expired - cannot retry, customer must update payment method."
    },
    "checkout_dropoff": {
        "bucket": "abandoned",
        "action": "send_nudge",
        "reason": "Customer dropped off before completing payment - send reminder with saved cart."
    },
    "repeat_failure": {
        "bucket": "high_value_risk",
        "action": "send_coupon",
        "reason": "Repeat failure on this customer - offer small incentive to complete purchase."
    },
}

DEFAULT = {
    "bucket": "unclassified",
    "action": "escalate_human",
    "reason": "No known pattern matched - escalating to human review instead of guessing."
}


def classify_failure(payment):
    rule = RULES.get(payment["reason_code"], DEFAULT)
    return {
        **payment,
        "bucket": rule["bucket"],
        "action": rule["action"],
        "reasoning": rule["reason"],
    }

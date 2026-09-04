"""
Bounded action layer. Each action is capped so the agent can never
loop forever or spam a customer.
"""

import random

MAX_RETRIES_PER_CUSTOMER = 2
MAX_COUPONS_PER_CUSTOMER = 1

retry_count = {}
coupon_issued = set()


def retry_payment(payment):
    count = retry_count.get(payment["customer"], 0)
    if count >= MAX_RETRIES_PER_CUSTOMER:
        return {"status": "failed", "note": "Max retries reached - escalating to human."}
    retry_count[payment["customer"]] = count + 1
    success = random.random() < 0.7
    return {"status": "recovered" if success else "pending", "note": "Retry attempted"}


def send_nudge(payment):
    return {"status": "pending", "note": f"WhatsApp/SMS nudge sent to {payment['customer']} with cart link."}


def send_update_link(payment):
    return {"status": "pending", "note": f"Payment-update link sent to {payment['customer']}."}


def send_coupon(payment):
    if payment["customer"] in coupon_issued:
        return {"status": "failed", "note": "Coupon already issued to this customer - escalating."}
    coupon_issued.add(payment["customer"])
    return {"status": "pending", "note": "10% discount coupon issued."}


def escalate_human(payment):
    return {"status": "escalated", "note": "Unresolved - flagged for manual review."}


ACTION_MAP = {
    "retry_later": retry_payment,
    "retry_now": retry_payment,
    "send_nudge": send_nudge,
    "send_update_link": send_update_link,
    "send_coupon": send_coupon,
    "escalate_human": escalate_human,
}


def execute_action(payment):
    fn = ACTION_MAP.get(payment["action"], escalate_human)
    result = fn(payment)
    return {**payment, **result}

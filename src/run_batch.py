import json
import os
from classify import classify_failure
from actions import execute_action


def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "failed_payments.json")
    with open(data_path) as f:
        payments = json.load(f)

    results = []
    for p in payments:
        classified = classify_failure(p)
        outcome = execute_action(classified)
        results.append(outcome)

    total = len(results)
    recovered = sum(1 for r in results if r["status"] == "recovered")
    recovered_amount = sum(r["amount"] for r in results if r["status"] == "recovered")
    at_risk_amount = sum(r["amount"] for r in results)

    summary = {
        "total_cases": total,
        "recovered_count": recovered,
        "recovery_rate": round(recovered / total * 100, 1),
        "amount_at_risk": at_risk_amount,
        "amount_recovered": recovered_amount,
        "cases": results,
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "results.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Processed {total} cases | Recovered {recovered} (Rs.{recovered_amount}) | Rate: {summary['recovery_rate']}%")
    print(f"Results written to {out_path}")


if __name__ == "__main__":
    main()

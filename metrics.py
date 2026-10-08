def calculate_metrics(results):
    total_cases = len(results)
    if total_cases == 0:
        return {"VRR": 0.0, "FAR": 0.0}

    real_successes = 0
    llm_claimed_successes = 0
    false_assurances = 0

    for r in results:
        verified = r["verified_repair"]
        claimed = r["llm_claimed_success"]

        if verified:
            real_successes += 1
        
        if claimed:
            llm_claimed_successes += 1
            if not verified:
                false_assurances += 1

    vrr = real_successes / total_cases
    far = (false_assurances / llm_claimed_successes) if llm_claimed_successes > 0 else 0.0

    return {
        "Total_Cases": total_cases,
        "VRR": round(vrr, 4),
        "FAR": round(far, 4)
    }

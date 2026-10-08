import csv
import os
from llm_client import get_llm_patch
from vul4py_verifier import verify_patch
from metrics import calculate_metrics

test_samples = [
    {
        "id": "sample_1",
        "file_path": "vulnerable_code_1.py",
        "code": "import pickle\ndef unsafe_load(data):\n    return pickle.loads(data)"
    }
]

def run_experiment():
    results = []
    csv_file = "results.csv"
    fieldnames = ["sample_id", "latency", "llm_claimed_success", "confidence", "verified_repair"]

    # Crear un archivo de prueba vulnerable local para la demo
    with open(test_samples[0]["file_path"], "w") as f:
        f.write(test_samples[0]["code"])

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for sample in test_samples:
            print(f"Ejecutando evaluación para {sample['id']}...")
            
            llm_response = get_llm_patch(sample["code"])
            if not llm_response:
                continue

            patch_diff = llm_response.get("patch_diff", "")
            claimed_success = llm_response.get("llm_claimed_success", False)
            confidence = llm_response.get("confidence", 0.0)
            latency = llm_response.get("latency", 0.0)

            verified_success = verify_patch(sample["file_path"], patch_diff)

            result_row = {
                "sample_id": sample["id"],
                "latency": round(latency, 4),
                "llm_claimed_success": claimed_success,
                "confidence": confidence,
                "verified_repair": verified_success
            }

            writer.writerow(result_row)
            results.append(result_row)

    final_metrics = calculate_metrics(results)
    print("\n--- RESULTADOS FINALES DEL EXPERIMENTO ---")
    for k, v in final_metrics.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    run_experiment()

import os
import csv

# If you are already inside the folder, use current directory, otherwise create 'model_risk_overlay'
current_folder_name = os.path.basename(os.getcwd())
if current_folder_name == "model_risk_overlay":
    ROOT_DIR = "."
else:
    ROOT_DIR = "model_risk_overlay"

ARTIFACTS = {
    "MDD.md": "# Model Development Document (MDD)\n## 1. Executive Summary\n## 2. Data Lineage\n## 3. Feature Set\n## 4. Methodology\n## 5. Neutralization\n## 6. Limitations\n",
    "IVR.md": "# Independent Validation Report (IVR)\n## 1. Conceptual Soundness\n## 2. Data Controls\n## 3. Outcomes Analysis\n## 4. Sensitivity & Stress Tests\n## 5. Findings & Remediation\n",
    "Monitoring_Plan.md": "# Monitoring Plan\n## Weekly Checks (Drift & Decay)\n## Monthly Checks (Retraining & Regime)\n## Triggers (Amber/Red)\n",
    "Model_Inventory.md": "# Model Inventory Entry\n| Field | Value |\n|-------|-------|\n| Model ID | |\n| Owner | BPENROD |\n| Risk Tier | 1 (Critical) |\n| Validation Cycle | Annual |\n"
}

def create_overlay():
    # 1. Create Directory if strictly necessary
    if ROOT_DIR != "." and not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
        print(f"[+] Created directory: {ROOT_DIR}")

    # 2. Create Markdown Artifacts
    for filename, content in ARTIFACTS.items():
        filepath = os.path.join(ROOT_DIR, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"[+] Created artifact: {filepath}")

    # 3. Create Findings Tracker (CSV)
    csv_path = os.path.join(ROOT_DIR, "Findings_Tracker.csv")
    headers = ["finding_id", "severity", "description", "owner", "due_date", "status", "closure_evidence"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(["F-001", "High", "Look-ahead bias in feature engineering", "BPENROD", "2026-03-01", "Open", ""])
    print(f"[+] Created tracker: {csv_path}")

if __name__ == "__main__":
    create_overlay()
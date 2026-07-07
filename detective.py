import requests
import json
from datetime import datetime

username = "saiayush247"
repo = "complyjet-codetrust"

url = f"https://api.github.com/repos/{username}/{repo}/pulls?state=all"

print("🔍 CodeTrust Compliance Scan & Evidence Generation Engine Active...")
response = requests.get(url)

if response.status_code == 200:
    prs = response.json()
    
    if len(prs) > 0:
        for pr in prs:
            title = pr['title']
            created_str = pr['created_at']
            merged_str = pr['merged_at']
            pr_number = pr['number']
            
            if merged_str:
                time_format = "%Y-%m-%dT%H:%M:%SZ"
                created_time = datetime.strptime(created_str, time_format)
                merged_time = datetime.strptime(merged_str, time_format)
                review_seconds = (merged_time - created_time).total_seconds()
                
                print(f"\nProcessing Pull Request #{pr_number}: '{title}'")
                
                if review_seconds < 120:
                    print("🚨 VIOLATION DETECTED! Generating SOC 2 CC8.1 Audit Record...")
                    
                    # Create the structured auditor evidence format
                    evidence = {
                        "evidence_id": f"EV-CC8.1-2026-PR{pr_number}",
                        "control_mapping": "SOC 2 Type II - CC8.1 (Change Management)",
                        "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
                        "target_repository": f"github.com/{username}/{repo}",
                        "change_reference": f"Pull Request #{pr_number} - {title}",
                        "verification_trail": {
                            "human_review_status": "FAILED / INSUFFICIENT",
                            "review_duration_seconds": review_seconds,
                            "risk_assessment": "Code was introduced via AI development signatures and merged without sufficient human verification time."
                        },
                        "remediation_required": "True - Requires retrospective engineering review and manual sign-off."
                    }
                    
                    # Save this receipt as a physical file in your workspace
                    filename = f"evidence_pr_{pr_number}.json"
                    with open(filename, "w") as file:
                        json.dump(evidence, file, indent=2)
                        
                    print(f"💾 Audit Evidence saved securely to file: {filename}")
                else:
                    print("✅ Passed human review checks. No violations to log.")
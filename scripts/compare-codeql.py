import json
import os
import sys

BASELINE = "security/codeql-baseline.sarif"
CURRENT = "results/csharp.sarif"
EXCEPTIONS_FILE = "security/exceptions.json"

SEVERITY_FAIL = {"high", "critical"}

def safe_load(path):
    if not os.path.exists(path):
        print(f"⚠️ {path} not found, skipping baseline comparison")
        return None
    if os.path.getsize(path) == 0:
        print(f"⚠️ {path} is empty, skipping baseline comparison")
        return None

    with open(path) as f:
        return json.load(f)

def extract_findings(data):
    if data is None:
        return {}

    findings = {}
    for run in data.get("runs", []):
        rules = {r["id"]: r for r in run.get("tool", {}).get("driver", {}).get("rules", [])}

        for res in run.get("results", []):
            rule_id = res.get("ruleId")
            sev = float(rules.get(rule_id, {}).get("properties", {}).get("security-severity", "0"))

            if sev >= 9:
                severity = "critical"
            elif sev >= 7:
                severity = "high"
            elif sev >= 4:
                severity = "medium"
            else:
                severity = "low"

            key = rule_id + str(res.get("locations"))
            findings[key] = {
                "rule": rule_id,
                "severity": severity,
                "message": res.get("message", {}).get("text", "")
            }
    return findings

baseline = safe_load(BASELINE)
current = safe_load(CURRENT)
exceptions = safe_load(EXCEPTIONS_FILE) or {"rules": []}

if current is None:
    print("❌ No SARIF results found. CodeQL failed?")
    sys.exit(1)

base = extract_findings(baseline)
cur = extract_findings(current)

new = {k:v for k,v in cur.items() if k not in base}

violations = [
    f for f in new.values()
    if f["severity"] in SEVERITY_FAIL and f["rule"] not in exceptions["rules"]
]

if violations:
    print("❌ New HIGH/CRITICAL vulnerabilities detected:")
    for v in violations:
        print(f" - [{v['severity'].upper()}] {v['rule']}: {v['message']}")
    sys.exit(1)

print("✅ No new HIGH/CRITICAL vulnerabilities")

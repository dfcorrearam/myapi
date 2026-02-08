import json
import os
import sys

BASELINE = "security/codeql-baseline.sarif"
CURRENT = "results/csharp.sarif"
EXCEPTIONS_FILE = "security/exceptions.json"

SEVERITY_FAIL = {"high", "critical"}

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

def extract_findings(data):
    findings = {}
    for run in data.get("runs", []):
        rules = {r["id"]: r for r in run.get("tool", {}).get("driver", {}).get("rules", [])}
        for res in run.get("results", []):
            rule_id = res.get("ruleId")
            sev = rules.get(rule_id, {}).get("properties", {}).get("security-severity", "0.0")
            sev = float(sev)
            severity = "low"
            if sev >= 9.0:
                severity = "critical"
            elif sev >= 7.0:
                severity = "high"
            elif sev >= 4.0:
                severity = "medium"

            key = rule_id + str(res.get("locations"))
            findings[key] = {
                "rule": rule_id,
                "severity": severity,
                "message": res.get("message", {}).get("text", "")
            }
    return findings

baseline = load_json(BASELINE)
current = load_json(CURRENT)
exceptions = load_json(EXCEPTIONS_FILE) or {}

if current is None:
    print("❌ No SARIF current file found")
    sys.exit(1)

base_findings = extract_findings(baseline) if baseline else {}
cur_findings = extract_findings(current)

new_findings = {k:v for k,v in cur_findings.items() if k not in base_findings}

filtered = []
for f in new_findings.values():
    if f["rule"] in exceptions.get("rules", []):
        continue
    if f["severity"] in SEVERITY_FAIL:
        filtered.append(f)

if filtered:
    print("❌ New HIGH/CRITICAL vulnerabilities detected:")
    for f in filtered:
        print(f"- [{f['severity'].upper()}] {f['rule']} -> {f['message']}")
    sys.exit(1)

print("✅ No new HIGH/CRITICAL vulnerabilities")

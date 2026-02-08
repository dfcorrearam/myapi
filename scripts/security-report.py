import json

with open("results/csharp.sarif") as f:
    sarif = json.load(f)

findings = []

for run in sarif.get("runs", []):
    rules = {r["id"]: r for r in run["tool"]["driver"]["rules"]}
    for res in run["results"]:
        rid = res["ruleId"]
        sev = float(rules[rid]["properties"].get("security-severity", "0"))
        findings.append((rid, sev, res["message"]["text"]))

print("## 🔐 Security Report\n")

if not findings:
    print("✅ No vulnerabilities detected.")
    exit()

print("| Rule | Severity | Message |")
print("|------|---------|--------|")

for r, s, m in findings:
    sev = "LOW"
    if s >= 9: sev = "CRITICAL"
    elif s >= 7: sev = "HIGH"
    elif s >= 4: sev = "MEDIUM"
    print(f"| {r} | {sev} | {m[:120]} |")

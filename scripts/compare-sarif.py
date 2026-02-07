import json

def load(path):
    with open(path) as f:
        return json.load(f)

baseline = load("security/codeql-baseline.sarif")
current = load("results/csharp.sarif")

def get_ids(data):
    ids = set()
    for run in data["runs"]:
        for r in run.get("results", []):
            ids.add(r["ruleId"] + str(r.get("locations", "")))
    return ids

base_ids = get_ids(baseline)
cur_ids = get_ids(current)

new = cur_ids - base_ids

if new:
    print("❌ New vulnerabilities detected:")
    for n in new:
        print("  -", n)
    exit(1)

print("✅ No new vulnerabilities")

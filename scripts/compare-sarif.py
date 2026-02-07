import json
import os
import sys

def load(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print(f"⚠️ Baseline not found or empty: {path}")
        print("Skipping baseline comparison")
        sys.exit(0)

    with open(path) as f:
        return json.load(f)

baseline = load("security/codeql-baseline.sarif")
current = load("results/csharp.sarif")

def get_ids(data):
    ids = set()
    for run in data.get("runs", []):
        for r in run.get("results", []):
            ids.add(r.get("ruleId", "unknown") + str(r.get("locations", "")))
    return ids

base_ids = get_ids(baseline)
cur_ids = get_ids(current)

new = cur_ids - base_ids

if new:
    print("❌ New vulnerabilities detected:")
    for n in new:
        print("  -", n)
    sys.exit(1)

print("✅ No new vulnerabilities")

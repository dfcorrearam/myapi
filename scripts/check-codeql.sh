#!/usr/bin/env bash
set -e

FILE="results/csharp.sarif"

if [ ! -f "$FILE" ]; then
  echo "❌ SARIF file not found"
  exit 1
fi

CRITICAL=$(jq '[.runs[].results[] | select(.level=="error")] | length' $FILE)
HIGH=$(jq '[.runs[].results[] | select(.level=="warning")] | length' $FILE)

echo "==============================="
echo "CodeQL Vulnerability Summary"
echo "Critical: $CRITICAL"
echo "High:     $HIGH"
echo "==============================="

if [ "$CRITICAL" -gt 0 ]; then
  echo "❌ FAIL: Critical vulnerabilities detected"
  exit 1
fi

if [ "$HIGH" -gt 0 ]; then
  echo "❌ FAIL: High vulnerabilities detected"
  exit 1
fi

echo "✅ Security gate passed"

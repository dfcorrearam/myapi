$ErrorActionPreference = "Stop"

$threshold = @("High", "Critical")
$exceptionsFile = "security/vulnerability-exceptions.json"

$exceptions = @()
if (Test-Path $exceptionsFile) {
    $exceptions = (Get-Content $exceptionsFile | ConvertFrom-Json).ignore
}

$json = dotnet list package --vulnerable --include-transitive --format json | ConvertFrom-Json

$violations = @()

foreach ($project in $json.projects) {
    foreach ($fw in $project.frameworks) {
        foreach ($pkg in $fw.dependencies) {
            if ($pkg.vulnerabilities) {
                foreach ($vuln in $pkg.vulnerabilities) {
                    if ($threshold -contains $vuln.severity) {

                        $isIgnored = $exceptions | Where-Object {
                            $_.package -eq $pkg.name -and
                            $_.cve -eq $vuln.advisoryUrl.Split("/")[-1]
                        }

                        if (-not $isIgnored) {
                            $violations += [PSCustomObject]@{
                                Package  = $pkg.name
                                Severity = $vuln.severity
                                Advisory = $vuln.advisoryUrl
                            }
                        }
                    }
                }
            }
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "❌ High/Critical vulnerabilities found:"
    $violations | Format-Table
    exit 1
}

Write-Host "✅ No blocking vulnerabilities found"

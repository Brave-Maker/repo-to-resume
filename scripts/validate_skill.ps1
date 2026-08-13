param(
    [string]$SkillRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$failures = [System.Collections.Generic.List[string]]::new()

function Assert-Check {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        $failures.Add($Message)
    }
}

$skillPath = Join-Path $SkillRoot 'SKILL.md'
Assert-Check (Test-Path -LiteralPath $skillPath) 'SKILL.md is missing'

if (Test-Path -LiteralPath $skillPath) {
    $skillText = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillPath
    $frontmatter = [regex]::Match(
        $skillText,
        '(?s)^---\r?\nname:\s*([^\r\n]+)\r?\ndescription:\s*([^\r\n]+)\r?\n---'
    )

    Assert-Check $frontmatter.Success 'Frontmatter must begin with name and a single-line description'
    if ($frontmatter.Success) {
        Assert-Check ($frontmatter.Groups[1].Value.Trim() -eq 'repo-to-resume') 'Frontmatter name must be repo-to-resume'
        Assert-Check ($frontmatter.Groups[2].Value.Trim().Length -le 1024) 'Frontmatter description exceeds 1024 characters'
    }

    Assert-Check ($skillText -match 'CHECKPOINT') 'No explicit CHECKPOINT found'
    Assert-Check ($skillText -match 'evidence-manifest\.json') 'Manifest contract is not referenced'
    Assert-Check ($skillText -match 'BLOCKED') 'Failure status is not encoded'

    $runtimePattern = 'Claude Code skill|Claude Code users?|Cursor only|~/\.claude/skills/[a-z]|/plugin install\b'
    Assert-Check (-not [regex]::IsMatch($skillText, $runtimePattern, [Text.RegularExpressions.RegexOptions]::IgnoreCase)) 'Runtime-specific red flag found in SKILL.md'

    $referenceMatches = [regex]::Matches($skillText, 'references/[a-z0-9.-]+')
    foreach ($match in $referenceMatches) {
        $relativeReference = $match.Value -replace '/', [IO.Path]::DirectorySeparatorChar
        $referencePath = Join-Path $SkillRoot $relativeReference
        Assert-Check (Test-Path -LiteralPath $referencePath) "Missing reference: $($match.Value)"
    }
}

$jsonFiles = @(
    (Join-Path $SkillRoot 'evals\evals.json'),
    (Join-Path $SkillRoot 'evals\manifest-minimal.json'),
    (Join-Path $SkillRoot 'references\evidence-manifest.schema.json'),
    (Join-Path $SkillRoot 'test-prompts.json')
)

foreach ($jsonFile in $jsonFiles) {
    Assert-Check (Test-Path -LiteralPath $jsonFile) "Missing JSON file: $jsonFile"
    if (Test-Path -LiteralPath $jsonFile) {
        try {
            $null = Get-Content -Raw -Encoding UTF8 -LiteralPath $jsonFile | ConvertFrom-Json
        }
        catch {
            $failures.Add("Invalid JSON: $jsonFile - $($_.Exception.Message)")
        }
    }
}

$allMarkdown = Get-ChildItem -LiteralPath $SkillRoot -Recurse -File -Filter '*.md' |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' }
$combinedText = ($allMarkdown | ForEach-Object {
    Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName
}) -join "`n"

$bannedLegacyPatterns = @(
    '10-100x',
    '10-1000x',
    '99%.*99\.9%',
    'count_action_items_lte:10.*output_not_contains_regex'
)

foreach ($pattern in $bannedLegacyPatterns) {
    Assert-Check (-not [regex]::IsMatch($combinedText, $pattern)) "Legacy anti-pattern remains: $pattern"
}

$requiredReferences = @(
    'business-chain-extractor.md',
    'claim-policy.md',
    'contribution-mapper.md',
    'experience-lab.md',
    'claim-grill.md',
    'interview-script-generator.md',
    'quality-gate.md',
    'output-contracts.md',
    'evidence-manifest.schema.json'
)

$schemaPath = Join-Path $SkillRoot 'references\evidence-manifest.schema.json'
if (Test-Path -LiteralPath $schemaPath) {
    $schemaText = Get-Content -Raw -Encoding UTF8 -LiteralPath $schemaPath
    Assert-Check ($schemaText -match 'NEEDS_EVIDENCE') 'Claim status enum is missing from manifest schema'
    Assert-Check ($schemaText -match '"status"') 'Claim status is not required by manifest schema'
}

foreach ($name in $requiredReferences) {
    $requiredPath = Join-Path $SkillRoot "references\$name"
    Assert-Check (Test-Path -LiteralPath $requiredPath) "Required module missing: $name"
}

if ($failures.Count -gt 0) {
    Write-Host "Validation failed with $($failures.Count) issue(s):"
    foreach ($failure in $failures) {
        Write-Host "- $failure"
    }
    exit 1
}

Write-Host "Validation passed: $SkillRoot"
Write-Host "Markdown files: $($allMarkdown.Count)"
Write-Host "Required modules: $($requiredReferences.Count)"
exit 0

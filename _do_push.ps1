$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\ASUS\Desktop\sistemas\piayetIa"
$StatusFile = Join-Path $ProjectDir "push_status.txt"
$LogFile = Join-Path $ProjectDir "push_run.log"
$RepoUrl = "https://github.com/terrafirmaperu/piaget.git"

function Write-Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts $msg" | Out-File -FilePath $LogFile -Append -Encoding utf8
}

try {
    Set-Location $ProjectDir
    Write-Log "Starting push workflow"

    # Read token from permisos.txt
    $permisosPath = "C:\Users\ASUS\Desktop\sistemas\TERRAFIRMA\factora-master\factora-master\app\permisos.txt"
    $tokenLine = Select-String -Path $permisosPath -Pattern "^token GitHub:\s*(.+)$" | Select-Object -First 1
    if (-not $tokenLine) { throw "GitHub token not found in permisos.txt" }
    $token = $tokenLine.Matches.Groups[1].Value.Trim()
    if (-not $token) { throw "GitHub token is empty" }
    Write-Log "Token loaded (redacted)"

    # git init if needed
    if (-not (Test-Path ".git")) {
        git init | Out-File -FilePath $LogFile -Append -Encoding utf8
        Write-Log "git init completed"
    }

    # Local config only
    git config --local user.name "Neo"
    git config --local user.email "neo@jeanpiaget.ia"
    Write-Log "Local git user configured"

    # Ensure on main branch
    $currentBranch = git rev-parse --abbrev-ref HEAD 2>$null
    if ($LASTEXITCODE -ne 0 -or $currentBranch -eq "HEAD") {
        git checkout -B main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    } elseif ($currentBranch -ne "main") {
        git checkout -B main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    }
    Write-Log "On branch main"

    # Stage and commit if needed
    git add -A 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    $status = git status --porcelain
    if ($status) {
        git commit -m "Initial commit: Django Jean Piaget project" 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
        Write-Log "Created commit"
    } else {
        Write-Log "Nothing to commit"
    }

    $commitHash = (git rev-parse HEAD).Trim()
    Write-Log "Commit hash: $commitHash"

    # Set remote with token
    $authUrl = "https://x-access-token:${token}@github.com/terrafirmaperu/piaget.git"
    $remoteExists = git remote get-url origin 2>$null
    if ($LASTEXITCODE -eq 0) {
        git remote set-url origin $authUrl
    } else {
        git remote add origin $authUrl
    }
    Write-Log "Remote set with token (redacted)"

    # Fetch remote to check state
    git fetch origin 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
    $remoteHasMain = git ls-remote --heads origin main 2>$null
    $pushOk = $false
    $pushMethod = ""

    if ($remoteHasMain) {
        # Try push first
        git push -u origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
        if ($LASTEXITCODE -eq 0) {
            $pushOk = $true
            $pushMethod = "direct"
        } else {
            # Check if remote only has README
            git fetch origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
            $remoteFiles = git ls-tree -r --name-only origin/main 2>$null
            $onlyReadme = ($remoteFiles.Count -le 2) -and ($remoteFiles -contains "README.md")
            Write-Log "Remote has commits. onlyReadme=$onlyReadme fileCount=$($remoteFiles.Count)"

            if ($onlyReadme) {
                git push -u origin main --force 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
                if ($LASTEXITCODE -eq 0) {
                    $pushOk = $true
                    $pushMethod = "force (README only)"
                }
            } else {
                git pull --rebase origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
                if ($LASTEXITCODE -eq 0) {
                    git push -u origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
                    if ($LASTEXITCODE -eq 0) {
                        $pushOk = $true
                        $pushMethod = "rebase then push"
                    }
                }
            }
        }
    } else {
        git push -u origin main 2>&1 | Out-File -FilePath $LogFile -Append -Encoding utf8
        if ($LASTEXITCODE -eq 0) {
            $pushOk = $true
            $pushMethod = "initial push"
        }
    }

    # Remove token from remote URL
    git remote set-url origin $RepoUrl
    Write-Log "Remote URL sanitized"

    if (-not $pushOk) {
        throw "Push failed - see push_run.log"
    }

    Write-Log "Push succeeded via $pushMethod"
    @(
        "OK",
        "URL: $RepoUrl",
        "Commit: $commitHash",
        "Method: $pushMethod"
    ) | Out-File -FilePath $StatusFile -Encoding utf8
    Write-Log "Status written"
    exit 0
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    @(
        "FAIL",
        "URL: $RepoUrl",
        "Error: $($_.Exception.Message)"
    ) | Out-File -FilePath $StatusFile -Encoding utf8
    exit 1
}

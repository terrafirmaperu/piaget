Set-Location "C:\Users\ASUS\Desktop\sistemas\piayetIa"
$log = Join-Path $PWD "deploy_run_log.txt"
"=== START $(Get-Date -Format o) ===" | Out-File $log -Encoding utf8
& "C:\Users\ASUS\Envs\Neo\Scripts\python.exe" -m pip install paramiko *>> $log 2>&1
"`n=== _push_and_deploy.py ===" | Add-Content $log
& "C:\Users\ASUS\Envs\Neo\Scripts\python.exe" "_push_and_deploy.py" *>> $log 2>&1
$code = $LASTEXITCODE
"`n=== EXIT CODE: $code ===" | Add-Content $log
exit $code

$kubectl = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\kubectl.exe"
$pod = (& $kubectl get pod -n dvwa -l app=dvwa -o jsonpath="{.items[0].metadata.name}").Trim()

if ($pod) {
    Write-Host "[*] Found DVWA Pod: $pod" -ForegroundColor Cyan
    & $kubectl exec -n dvwa $pod -- /etc/init.d/mysql start
    Start-Sleep -Seconds 2
    & $kubectl exec -n dvwa $pod -- mysql -u root -e "CREATE DATABASE IF NOT EXISTS dvwa; GRANT ALL ON dvwa.* TO 'app'@'127.0.0.1' IDENTIFIED BY 'vulnerables'; GRANT ALL ON dvwa.* TO 'app'@'localhost' IDENTIFIED BY 'vulnerables'; FLUSH PRIVILEGES;"
    Write-Host "[+] MySQL started and database initialized on pod $pod." -ForegroundColor Green
} else {
    Write-Error "[!] No running DVWA pod found in namespace dvwa."
}

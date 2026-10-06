# AccuKnox Solution Engineer Trainee - Technical Assessment Deliverables

Welcome to the complete solution workspace for the **AccuKnox Solution Engineer Trainee** evaluation.

---

## 📁 Repository Structure & Deliverables

```
test/
├── Solution Engineer Trainee Problem statement.pdf
├── README.md                                    <-- Master Navigation & Overview
├── Problem_Statement_2_DVWA_Execution_Report.md <-- Full DVWA K8s Attack & Mitigation Report
│
├── presentations/                               <-- Problem Statement 1 PPT Decks & Scripts
│   ├── generate_all_pptx.py                     <-- Python script to regenerate PPTX slides
│   │
│   ├── Topic1_Kubernetes_Attack_Vectors/
│   │   ├── Top_5_Kubernetes_Security_Attack_Vectors.pptx  <-- PowerPoint Presentation Deck (4 Slides)
│   │   ├── slides.html                          <-- Interactive Web Slide Deck (Open in Browser)
│   │   └── Presentation_Top_5_Kubernetes_Attack_Vectors.md <-- Slide Text & 5-Min Speaker Notes
│   │
│   └── Topic3_Falco_vs_KubeArmor/
│       ├── Falco_vs_KubeArmor_Runtime_Security.pptx       <-- PowerPoint Presentation Deck (4 Slides)
│       ├── slides.html                          <-- Interactive Web Slide Deck (Open in Browser)
│       └── Presentation_Falco_vs_KubeArmor.md   <-- Slide Text & 5-Min Speaker Notes
│
└── k8s-dvwa/                                    <-- Problem Statement 2 Kubernetes Setup & Exploits
    ├── setup-cluster.ps1                        <-- Automated deploy script (Windows PowerShell)
    ├── setup-cluster.sh                         <-- Automated deploy script (Linux/macOS Bash)
    ├── k8s-manifests/
    │   ├── dvwa.yaml                            <-- Kubernetes Deployment & NodePort Service
    │   └── kubearmor-dvwa-security-policies.yaml<-- Zero-Trust Active LSM Defense Policy
    └── attack-demos/
        ├── exploit_dvwa.py                      <-- Python exploit script for all 3 attack surfaces
        └── exploit_dvwa.ps1                     <-- PowerShell exploit script for all 3 attack surfaces
```

---

## 🎯 Problem Statement 1: Technical Presentations (10 Mins Total)

We prepared presentation packages for the two selected high-impact topics:

### Presentation A: Top 5 Kubernetes Security Attack Vectors
- **Artifacts:**
  - PowerPoint Deck: [Top_5_Kubernetes_Security_Attack_Vectors.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx)
  - Interactive Web Deck: [slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/slides.html)
  - Speaker Script: [Presentation_Top_5_Kubernetes_Attack_Vectors.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic1_Kubernetes_Attack_Vectors/Presentation_Top_5_Kubernetes_Attack_Vectors.md)
- **Topics Covered:** Control plane & RBAC misconfigurations, Insecure container supply chains, In-pod RCE & ServiceAccount token theft, Flat network lateral movement, Container breakouts & host escapes.

### Presentation B: Falco vs KubeArmor (CNCF Runtime Security)
- **Artifacts:**
  - PowerPoint Deck: [Falco_vs_KubeArmor_Runtime_Security.pptx](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx)
  - Interactive Web Deck: [slides.html](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/slides.html)
  - Speaker Script: [Presentation_Falco_vs_KubeArmor.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/presentations/Topic3_Falco_vs_KubeArmor/Presentation_Falco_vs_KubeArmor.md)
- **Topics Covered:** Architectural analysis (Syscall tracing vs Linux Security Modules / BPF-LSM), Detection vs Active Inline Enforcement, Kubernetes CRD native design, Zero-Trust whitelisting, and AccuKnox enterprise CNAPP advantages.

---

## 🚀 Problem Statement 2: Kubernetes DVWA Deployment & 3 Attack Surfaces Demo

### Quick Start Guide:
1. **Deploy DVWA to local Kubernetes:**
   ```powershell
   .\k8s-dvwa\setup-cluster.ps1
   # Or on Linux/macOS:
   ./k8s-dvwa/setup-cluster.sh
   ```
2. **Forward port to access:**
   ```bash
   kubectl port-forward -n dvwa svc/dvwa-service 8080:80
   ```
3. **Execute the automated 3-Attack Surface exploit demonstration:**
   ```bash
   python k8s-dvwa/attack-demos/exploit_dvwa.py --url http://localhost:8080
   # Or using PowerShell:
   .\k8s-dvwa\attack-demos\exploit_dvwa.ps1 -BaseUrl "http://localhost:8080"
   ```

### 3 Attack Surfaces Demonstrated:
1. **Command Injection:** Spawns arbitrary container commands (`whoami; id; uname -a`) and probes the mounted Kubernetes ServiceAccount credentials.
2. **SQL Injection:** Executes `1' UNION SELECT user, password FROM users #` to extract all application user accounts and password hashes.
3. **Local File Inclusion (LFI) & Kubernetes Token Theft:** Traverses container directory structure to read `/etc/passwd` and exfiltrates `/var/run/secrets/kubernetes.io/serviceaccount/token`, enabling direct cluster API server compromise.

### Active Defense Hardening:
- Apply KubeArmor active blocking policy:
  ```bash
  kubectl apply -f k8s-dvwa/k8s-manifests/kubearmor-dvwa-security-policies.yaml
  ```
- Blocks unauthorized shell spawns (`/bin/sh`, `/bin/bash`) and blocks reads to `/var/run/secrets/kubernetes.io/serviceaccount/token` directly at the Linux kernel LSM layer.

---

*For detailed execution logs, screenshots guide, and technical explanations, refer to [Problem_Statement_2_DVWA_Execution_Report.md](file:///c:/Users/Jaya%20Krishna%20Sai/Downloads/Projects/test/Problem_Statement_2_DVWA_Execution_Report.md).*

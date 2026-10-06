# Presentation 1: Top 5 Kubernetes Security Attack Vectors

**Presenter:** Solution Engineer Candidate  
**Target Audience:** AccuKnox Technical Evaluation Panel / Enterprise Security Team  
**Estimated Time:** 5 Minutes (4 Slides)  

---

## Slide 1: Title & Executive Overview
### **Top 5 Kubernetes Security Attack Vectors: Anatomy of Modern Cloud-Native Threats**

#### **Key Points:**
- **The Shift to Cloud-Native:** Kubernetes abstracts infrastructure, but introduces dynamic, ephemeral attack surfaces spanning the Control Plane, Node, and Workloads.
- **The 4C's Security Model:** Cloud, Cluster, Container, Code.
- **Objective:** Identify the top 5 high-impact attack vectors across the Kubernetes lifecycle and how modern Zero-Trust architectures mitigate them.

> **Speaker Notes (1 min):**  
> *"Good morning/afternoon team. As organizations accelerate Kubernetes adoption, security boundaries shift from traditional network perimeters to distributed microservices and dynamic orchestrators. In this 5-minute presentation, we'll dissect the top 5 Kubernetes attack vectors seen in production environments—from API server exposure down to container runtime escapes—and discuss how defense-in-depth and Zero-Trust principles stop these exploits."*

---

## Slide 2: Attack Vectors 1 & 2 — Control Plane & Access Misconfigurations

### **1. Compromised / Misconfigured Kubernetes API Server & RBAC**
- **The Threat:** Publicly accessible Kube-API Server (Port 6443) or overly permissive RBAC roles (`cluster-admin`, `secrets: ["get", "list"]`, wildcard permissions `*`).
- **Attack Path:** Stolen credentials/service tokens allow an attacker to create malicious pods, modify daemonsets, or exfiltrate cluster secrets.
- **Real-World Impact:** Tesla (2018) unauthenticated dashboard/API exposed leading to cryptojacking; Capital One SSRF pivot to instance metadata.

### **2. Insecure Supply Chain & Malicious Container Images**
- **The Threat:** Vulnerable base images, malicious packages in public registries, or poisoned CI/CD build pipelines.
- **Attack Path:** Deploying images containing Known CVEs (Log4j, OpenSSL) or backdoored entrypoints that establish reverse shells upon pod start.
- **Real-World Impact:** Doki malware, Kinsing worm targeting container registries and Docker daemons.

> **Speaker Notes (1.5 mins):**  
> *"Starting at the upper layers: Vector 1 is the API Server and RBAC. The Kube-API is the nervous system of the cluster. When organizations use wildcard RBAC permissions or expose the API server publicly without strict OIDC/MFA, any leaked token gives cluster control. Vector 2 is the Supply Chain: over 80% of container images in public repos contain known vulnerabilities. Once an image is deployed, static scanning alone is insufficient because zero-days execute at runtime."*

---

## Slide 3: Attack Vectors 3, 4 & 5 — Runtime, Network & Infrastructure Escapes

### **3. Vulnerable Web Applications & In-Pod Remote Code Execution (RCE)**
- **The Threat:** Exposed workloads (e.g., Spring4Shell, Log4Shell, SQLi/Command Injection) exploited to gain initial shell access inside a pod.
- **Attack Path:** Attacker uses RCE to query the in-pod ServiceAccount token at `/var/run/secrets/kubernetes.io/serviceaccount/token` and pivot horizontally.

### **4. Unrestricted Lateral Movement & Flat Pod Networking**
- **The Threat:** Default K8s networking is completely open (any pod can talk to any pod across namespaces).
- **Attack Path:** Lack of egress/ingress `NetworkPolicies` allows attackers who breach a single non-critical pod to query internal databases, payment gateways, or AWS/GCP cloud metadata (`169.254.169.254`).

### **5. Container Breakout & Host Kernel Compromise**
- **The Threat:** Misconfigured security contexts (`privileged: true`, `hostPID: true`, `CAP_SYS_ADMIN`) or Linux kernel CVEs (e.g., Dirty Pipe, Dirty COW).
- **Attack Path:** Escaping container cgroups/namespaces to gain root access on the underlying K8s worker node.

> **Speaker Notes (1.5 mins):**  
> *"Moving to runtime and infrastructure: Vector 3 is in-pod RCE. When a front-end pod is compromised, the attacker immediately inspects mounted service tokens and environment variables. Vector 4 is flat networking: without strict NetworkPolicies or eBPF-based microsegmentation, lateral movement to sensitive workloads is trivial. Finally, Vector 5 is container breakouts. A privileged container or kernel exploit allows attackers to break isolation boundaries and take over the underlying host node."*

---

## Slide 4: Comprehensive Mitigation & The AccuKnox Zero-Trust Paradigm

| Attack Vector | Traditional Mitigation | AccuKnox / Modern Zero-Trust Solution |
| :--- | :--- | :--- |
| **1. API / RBAC Abuse** | Least-privilege RBAC, Audit logs | Dynamic admission control (OPA/Kyverno) + continuous posture drift detection (Kube-Bench) |
| **2. Vulnerable Images** | Static image scanning (Trivy/Clair) | Admission gating + Software Bill of Materials (SBOM) verification |
| **3. In-Pod RCE & SA Token Theft** | Read-only root filesystem | **KubeArmor** active LSM/eBPF runtime blocking on unauthorized binaries & token access |
| **4. Flat Network Lateral Movement** | Standard K8s NetworkPolicies | eBPF-driven zero-trust microsegmentation (Cilium/AccuKnox CNAPP) with DNS & L7 visibility |
| **5. Container Breakout** | Deprecate privileged pods, Seccomp | Linux Security Modules (AppArmor/SELinux/BPF-LSM) active system call blocking |

### **Summary Conclusion:**
- Security cannot rely solely on pre-deployment scanning.
- **Zero-Trust Runtime Enforcement (KubeArmor)** + **Shift-Left Posture Management** provides end-to-end cloud-native defense.

> **Speaker Notes (1 min):**  
> *"To summarize: static scanning and basic RBAC are table stakes, but real resilience requires continuous runtime protection. By combining dynamic admission policies with KubeArmor's active LSM/eBPF enforcement—which actively blocks unauthorized file reads, process spawns, and network connections in real-time—we stop attacks at the earliest stage of the kill chain. Thank you, and I'd be happy to take questions."*

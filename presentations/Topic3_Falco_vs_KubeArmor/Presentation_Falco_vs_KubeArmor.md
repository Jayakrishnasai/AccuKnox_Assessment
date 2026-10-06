# Presentation 2: Falco vs KubeArmor — Deep Architectural Comparison & Kubernetes Runtime Security

**Presenter:** Solution Engineer Candidate  
**Target Audience:** AccuKnox Technical Evaluation Panel / Security Architects  
**Estimated Time:** 5 Minutes (4 Slides)  

---

## Slide 1: Title & Executive Context
### **Falco vs KubeArmor: Detection vs. Inline Active Enforcement in Cloud-Native Runtime Security**

#### **Key Points:**
- **The Runtime Security Mandate:** Static scanning (SAST/DAST/Image Scans) stops known vulnerabilities before deployment, but runtime defense protects live containers against zero-days, privilege escalation, and active exploits.
- **Two Leading Open-Source CNCF Projects:**
  - **Falco:** CNCF Graduated project created by Sysdig — Focused on rule-based anomaly *detection & alerting*.
  - **KubeArmor:** CNCF Sandbox project created by AccuKnox — Focused on policy-driven *inline active enforcement & prevention* utilizing Linux Security Modules (LSMs) & eBPF.
- **Core Question:** Why is detection alone insufficient for modern Zero-Trust, and how do their underlying architectures differ?

> **Speaker Notes (1 min):**  
> *"Good day everyone. Today we are comparing two of the most prominent open-source runtime security engines in the CNCF ecosystem: Falco and KubeArmor. While both monitor container activities, they solve fundamentally different problems in their design philosophy: Falco acts as a runtime security camera that records and alerts when an intrusion happens, whereas KubeArmor acts as an inline security guard that actively blocks the attack from succeeding in the first place. Over the next 4 minutes, let's explore their core architectures, enforcement mechanisms, and enterprise use cases."*

---

## Slide 2: Architectural Deep Dive — How They Work Under the Hood

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

### **Falco Architecture:**
- **Mechanism:** Captures system calls via kernel probe / tracepoint (`sys_enter` / `sys_exit`) via eBPF or kernel module.
- **Processing:** Streams events to userspace ring buffer; evaluates events against YAML rule condition syntax.
- **Action Mode:** **Asynchronous / Post-incident**. Falco *notifies* after the syscall completes. It cannot natively block an in-flight system call without separate third-party sidecars (e.g., Falco Talon / killing the pod).

### **KubeArmor Architecture:**
- **Mechanism:** Directly leverages **Linux Security Modules (LSMs)** — AppArmor, SELinux, and modern **BPF-LSM** hooks inside the Linux kernel.
- **Processing:** Enforces policies directly at the kernel hook point before the operation executes.
- **Action Mode:** **Synchronous Inline Prevention**. If a process attempts to execute an unauthorized binary or read a sensitive file, the kernel immediately returns `-EACCES` (Permission Denied).

> **Speaker Notes (1.5 mins):**  
> *"Let's look at the underlying architecture on Slide 2. Falco relies on system call tracing. When a command runs inside a container, the syscall enters the kernel, executes, and a copy of the event is streamed via a ring buffer to the Falco userspace daemon. Falco parses the event and issues an alert. This means by the time you receive the alert, the malicious binary has already executed and the payload has run.
> In contrast, KubeArmor taps directly into Linux Security Modules—such as AppArmor, SELinux, and BPF-LSM. When an unauthorized syscall is attempted, the LSM interceptor evaluates the KubeArmor policy in-kernel and blocks the operation synchronously before execution. KubeArmor then emits rich eBPF-based audit logs for telemetry without impacting application latency."*

---

## Slide 3: Feature & Capability Comparison Matrix

| Dimension | Falco | KubeArmor |
| :--- | :--- | :--- |
| **Primary Philosophy** | Threat Detection & Anomaly Auditing | Zero-Trust Inline Prevention & Active Enforcement |
| **Enforcement Mechanism** | None natively (Alerts only; requires external sidecars/killing pod) | Native Kernel LSMs (AppArmor, SELinux, BPF-LSM) + eBPF |
| **Attack Prevention** | Post-Exploit notification | **Pre-Exploit blocking** (Blocks unauthorized execution instantly) |
| **Policy Language** | Custom Falco Rule Syntax (Macros, Lists, Rules) | **Kubernetes-Native CRDs** (`KubeArmorPolicy`, `KubeArmorHostPolicy`) |
| **Zero-Trust Workload Hardening** | Difficult (Rule tuning required to reduce noise) | Native (White-listing / Black-listing of processes, files, network) |
| **Performance Overhead** | High userspace context switching under heavy I/O | Extremely lightweight (LSM hooks evaluated directly in kernel) |
| **Host & VM Support** | Kubernetes & Linux Hosts | Kubernetes, Bare-Metal, Linux VMs, and Edge (K3s/MicroK8s) |
| **Compliance & Frameworks** | MITRE ATT&CK, NIST 800-53, PCI-DSS (Audit logs) | MITRE ATT&CK, CIS Benchmarks, NIST Zero-Trust (Direct Enforcement) |

> **Speaker Notes (1.5 mins):**  
> *"Slide 3 outlines the key operational differences. First, policy definition: Falco uses a proprietary rule format, whereas KubeArmor uses native Kubernetes Custom Resource Definitions (CRDs) like `KubeArmorPolicy`, allowing DevOps and SecOps teams to manage security policies using familiar GitOps workflows like ArgoCD and Helm.
> Second, Zero-Trust posture: With KubeArmor, you can easily define default-deny or strict whitelisting policies—for instance, allowing `nginx` to only execute its worker process and preventing it from ever spawning `/bin/sh` or `/usr/bin/curl`. If an attacker exploits a zero-day RCE, the spawn attempt is immediately denied at the kernel level."*

---

## Slide 4: Strategic Recommendation & The Enterprise Solution (AccuKnox CNAPP)

### **When to Choose Which?**
1. **Choose Falco When:**
   - The primary requirement is broad behavioral observability, SIEM/SOC alerting, and historical forensics without risking workload disruption.
2. **Choose KubeArmor When:**
   - The organization requires true **Zero-Trust runtime defense**, regulatory compliance requiring active blocking, and automated policy discovery.

### **The AccuKnox CNAPP Advantage:**
- **Automated Policy Discovery:** Automatically analyzes application behavior and generates least-privilege KubeArmor security policies.
- **Unified Defense-in-Depth:** Integrates CSPM (Cloud Security Posture Management), CWPP (Cloud Workload Protection Platform), and KubeArmor runtime enforcement into a single pane of glass.
- **Inline Multi-Layer Defense:** Stops ransomware, crypto-mining, lateral movement, and container breakouts before damage occurs.

> **Speaker Notes (1 min):**  
> *"To conclude: Falco is a valuable telemetry and detection tool, but in high-stakes enterprise environments, detection after breach is not enough. KubeArmor brings true Zero-Trust to the Linux kernel by proactively preventing malicious actions while maintaining Kubernetes-native ergonomics. AccuKnox builds upon KubeArmor by automating policy discovery and integrating CWPP and CSPM into a comprehensive Cloud-Native Application Protection Platform. Thank you!"*

"""
Python script to generate professional .pptx presentation decks for:
1. Topic 1: Top 5 Kubernetes Security Attack Vectors
2. Topic 3: Falco vs KubeArmor: Runtime Security & Active Enforcement
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Styling Constants
NAVY = RGBColor(15, 23, 42)        # Slate 900
PRIMARY = RGBColor(37, 99, 235)     # Blue 600
ACCENT = RGBColor(14, 165, 233)     # Sky 500
DARK_GRAY = RGBColor(51, 65, 85)    # Slate 700
LIGHT_BG = RGBColor(248, 250, 252)  # Slate 50
WHITE = RGBColor(255, 255, 255)
RED = RGBColor(225, 29, 72)         # Rose 600
GREEN = RGBColor(22, 163, 74)       # Green 600

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="ACCUKNOX SOLUTION ENGINEER TRAINEE"):
    # Category / Tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = PRIMARY
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

def create_card(slide, left, top, width, height, title, content_items, accent_color=PRIMARY, border=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    if border:
        shape.line.color.rgb = accent_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    tf.margin_right = Inches(0.25)
    tf.margin_bottom = Inches(0.2)

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = accent_color

    for item in content_items:
        p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

def build_topic1_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- SLIDE 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY)
    
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "ACCUKNOX SOLUTION ENGINEER TRAINEE ASSESSMENT"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT
    p0.space_after = Pt(10)
    
    p1 = tf.add_paragraph()
    p1.text = "Top 5 Kubernetes Security Attack Vectors"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(15)
    
    p2 = tf.add_paragraph()
    p2.text = "Anatomy of Cloud-Native Vulnerabilities, Lateral Movement & Zero-Trust Mitigation"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    
    # --- SLIDE 2: Vectors 1 & 2 ---
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)
    add_header(slide2, "Control Plane & Supply Chain Threats")
    
    create_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
                "1. Misconfigured Kube-API Server & RBAC",
                [
                    "Threat: Publicly exposed API server (port 6443) or overly permissive RBAC roles (cluster-admin, wildcard * verbs).",
                    "Exploit Path: Stolen tokens allow attackers to deploy rogue pods, mount secrets, and take over cluster controls.",
                    "Real Impact: Tesla cryptojacking incident via exposed unauthenticated Kubernetes dashboard.",
                    "Mitigation: Private API endpoints, strict OIDC authentication, automated RBAC least-privilege auditing."
                ],
                RED, border=True)

    create_card(slide2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8),
                "2. Insecure Supply Chain & Container Images",
                [
                    "Threat: Base images containing known CVEs, unvetted public registries, or poisoned CI/CD build pipelines.",
                    "Exploit Path: Deploying backdoored containers that establish reverse shells on startup.",
                    "Real Impact: Kinsing & Doki malware targeting misconfigured container registries and engines.",
                    "Mitigation: Mandatory image signature verification (Cosign/Notary), vulnerability gating in CI/CD, and SBOM generation."
                ],
                RED, border=True)

    # --- SLIDE 3: Vectors 3, 4 & 5 ---
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)
    add_header(slide3, "Runtime, Network & Host-Level Attack Vectors")
    
    create_card(slide3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
                "3. In-Pod RCE & SA Token Theft",
                [
                    "Threat: Web app vulnerabilities (Command Injection, LFI, Log4j).",
                    "Exploit Path: Attacker steals pod ServiceAccount token at /var/run/secrets/... to pivot to K8s API.",
                    "Mitigation: KubeArmor file/process blocking, automountServiceAccountToken: false."
                ],
                PRIMARY)

    create_card(slide3, Inches(4.85), Inches(1.8), Inches(3.6), Inches(4.8),
                "4. Flat Pod Networking & Lateral Drift",
                [
                    "Threat: Default open east-west traffic between all namespaces.",
                    "Exploit Path: Compromised pod scans internal VPC, DBs, and cloud metadata (169.254.169.254).",
                    "Mitigation: Default-deny NetworkPolicies, eBPF microsegmentation, Cilium/AccuKnox CNAPP."
                ],
                PRIMARY)

    create_card(slide3, Inches(8.9), Inches(1.8), Inches(3.6), Inches(4.8),
                "5. Container Breakout & Host Escape",
                [
                    "Threat: Privileged containers (privileged: true, hostPID, CAP_SYS_ADMIN) or kernel CVEs.",
                    "Exploit Path: Escapes container isolation to root host node.",
                    "Mitigation: Restrictive Pod Security Standards (PSS), Seccomp, and BPF-LSM enforcement."
                ],
                PRIMARY)

    # --- SLIDE 4: Defense-in-Depth & AccuKnox ---
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)
    add_header(slide4, "Defense-in-Depth & The AccuKnox Zero-Trust Architecture")

    # Comparison Table
    rows, cols = 6, 3
    table_shape = slide4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.733)

    headers = ["Attack Vector", "Traditional Security Approach", "AccuKnox / Modern Zero-Trust Solution"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE

    data = [
        ("1. API & RBAC Abuse", "Manual RBAC review, audit logs", "Dynamic Admission Control (Kyverno/OPA) + Posture Management"),
        ("2. Supply Chain Risks", "Static image scanning in CI/CD", "Signature validation + SBOM + Admission Policy gating"),
        ("3. In-Pod RCE & Token Theft", "Static container file permissions", "KubeArmor Active LSM/eBPF runtime process & file blocking"),
        ("4. Lateral Movement", "Basic K8s NetworkPolicies", "eBPF-driven zero-trust microsegmentation with L7/DNS filtering"),
        ("5. Container Breakout", "Pod Security Standards (PSS)", "LSM (AppArmor / SELinux / BPF-LSM) system call prevention")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY if col_idx == 0 else (DARK_GRAY if col_idx == 1 else PRIMARY)
            if col_idx == 2:
                p.font.bold = True

    prs.save("presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx")
    print("[+] Generated Topic 1 PPTX: presentations/Topic1_Kubernetes_Attack_Vectors/Top_5_Kubernetes_Security_Attack_Vectors.pptx")

def build_topic3_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- SLIDE 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY)
    
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "ACCUKNOX SOLUTION ENGINEER TRAINEE ASSESSMENT"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT
    p0.space_after = Pt(10)
    
    p1 = tf.add_paragraph()
    p1.text = "Falco vs KubeArmor"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(15)
    
    p2 = tf.add_paragraph()
    p2.text = "Deep Architectural Comparison: Detection & Alerting vs Inline Active Enforcement"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)

    # --- SLIDE 2: Architectural Comparison ---
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)
    add_header(slide2, "Underlying Architectures: How They Operate")

    create_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
                "FALCO: System Call Tracing & Detection",
                [
                    "Architecture: Syscall monitoring via eBPF probe / kernel module -> Userspace Ring Buffer.",
                    "Operation Mode: Asynchronous / Post-incident. Emits alert AFTER the system call occurs.",
                    "Blocking Ability: Cannot natively block in-flight syscalls (requires external sidecars or pod termination).",
                    "Analogy: A high-resolution security camera recording a burglary as it happens."
                ],
                PRIMARY, border=True)

    create_card(slide2, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8),
                "KUBEARMOR: Linux Security Modules (LSM) & Active Prevention",
                [
                    "Architecture: Direct integration with Linux Security Modules (AppArmor, SELinux, BPF-LSM) + eBPF telemetry.",
                    "Operation Mode: Synchronous Inline Enforcement. Evaluates policy BEFORE the syscall executes.",
                    "Blocking Ability: Natively returns -EACCES (Permission Denied) to halt malicious binaries/file access instantly.",
                    "Analogy: An impenetrable locked door with an active guard preventing unauthorized entry."
                ],
                GREEN, border=True)

    # --- SLIDE 3: Comparison Matrix ---
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)
    add_header(slide3, "Feature & Capability Matrix: Falco vs KubeArmor")

    rows, cols = 7, 3
    table_shape = slide3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(4.4)
    table.columns[2].width = Inches(4.533)

    headers = ["Feature / Dimension", "Falco (Sysdig)", "KubeArmor (AccuKnox / CNCF)"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE

    data = [
        ("Core Philosophy", "Threat Detection & Anomaly Auditing", "Zero-Trust Active Prevention & Enforcement"),
        ("Enforcement Hook", "eBPF tracepoints / kprobes (Post-exec)", "Kernel LSMs (AppArmor / SELinux / BPF-LSM)"),
        ("Action on Threat", "Logs / Alerts / Notifications", "Inline Syscall Blocking (-EACCES) + Rich Logs"),
        ("Policy Definition", "Custom Falco YAML Rule DSL", "Kubernetes-Native CRDs (KubeArmorPolicy)"),
        ("Zero-Trust Hardening", "Requires manual tuning / Alert noise", "Native Default-Deny & Binary Whitelisting"),
        ("Workload Support", "K8s & Linux Hosts", "K8s, Linux VMs, Bare-Metal & Edge (K3s)")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY if col_idx == 0 else (DARK_GRAY if col_idx == 1 else GREEN)
            if col_idx == 2:
                p.font.bold = True

    # --- SLIDE 4: Strategic Recommendation & AccuKnox ---
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)
    add_header(slide4, "Enterprise Strategic Positioning & AccuKnox CNAPP")

    create_card(slide4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
                "Strategic Evaluation: When to Choose Which",
                [
                    "Falco is best suited for SIEM/SOC teams wanting broad behavioral visibility and historical event auditing.",
                    "KubeArmor is essential when organizations mandate active Zero-Trust workload isolation and strict compliance (NIST/PCI/CIS).",
                    "Combined Value: Telemetry + Active Enforcement forms the ultimate cloud-native security posture."
                ],
                PRIMARY)

    create_card(slide4, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8),
                "The AccuKnox Enterprise Advantage",
                [
                    "Automated Policy Discovery: AI-driven discovery engines observe application telemetry and automatically generate least-privilege KubeArmor policies.",
                    "Unified CNAPP Platform: Integrates CSPM (Cloud Posture), CWPP (Workload Protection), and CIEM into a single pane of glass.",
                    "True Zero-Trust: Protects against zero-day RCE, credential theft, and ransomware with zero performance penalty."
                ],
                NAVY, border=True)

    prs.save("presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx")
    print("[+] Generated Topic 3 PPTX: presentations/Topic3_Falco_vs_KubeArmor/Falco_vs_KubeArmor_Runtime_Security.pptx")

if __name__ == "__main__":
    build_topic1_presentation()
    build_topic3_presentation()

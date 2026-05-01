#!/usr/bin/env python3
"""
Professional PIE - Patent Information Extraction Form
Styled to match the official Chitkara University format
"""

import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus.flowables import Flowable
from datetime import datetime

# ─── Colour palette ───────────────────────────────────────────────────────────
RED       = colors.HexColor("#C0392B")
DARK      = colors.HexColor("#1A1A2E")
MID_GRAY  = colors.HexColor("#4A4A4A")
LIGHT_BG  = colors.HexColor("#F5F5F5")
TABLE_HDR = colors.HexColor("#1A1A2E")
WHITE     = colors.white
BLACK     = colors.black
GOLD      = colors.HexColor("#D4AF37")
BORDER    = colors.HexColor("#CCCCCC")

# ─── Inventory data ───────────────────────────────────────────────────────────
TOPIC   = "An Intelligent DCNN-Based Framework for Anomaly Detection and Performance Degradation Analysis"
SCHOOL  = "Chitkara University, Rajpura, Punjab"
ADDRESS = "Chandigarh-Patiala National Highway (NH-64), Jhansala (V), Rajpura, Patiala, Punjab - 140401, India"

PRIMARY = {
    "name":       "Gunjan Mehta",
    "emp_code":   "2210991590",
    "mobile":     "9315636376",
    "uni_email":  "gunjan1590.be22@chitkara.edu.in",
    "per_email":  "mehtagunjan098@gmail.com",
}

OTHERS = [
    ("Gaganveer Singh", "2210994783",
     "Chitkara University, gaganveer4783.be22@chitkara.edu.in, 8295055789"),
    ("Gunjan Mehta",    "2210991590",
     "Chitkara University, gunjan1590.be22@chitkara.edu.in, 9315636376"),
    ("Vidur Sharma",    "2210992524",
     "Chitkara University, vidur2524.be22@chitkara.edu.in, 8570840245"),
    ("",               "",  ""),   # Student 4 (blank)
    ("Dr. Rajat Takkar (Mentor)", "",
     "Chitkara University, DCSE Department"),
]

KEY_PHRASES = [
    ("1", "Video Forgery Detection"),
    ("2", "DCNN-Based Anomaly Detection"),
    ("3", "Multi-Feature Fusion (DCT + DWT + LBP)"),
    ("4", "Transfer Learning with ResNet50"),
    ("5", "Copy-Move Forgery Detection"),
    ("6", "Temporal Inconsistency Analysis"),
    ("7", "Performance Degradation Analysis"),
    ("8", "Digital Video Forensics"),
]

# ─── Style helpers ────────────────────────────────────────────────────────────
def S(name, **kw):
    base = {
        "fontName": "Helvetica",
        "fontSize": 10,
        "leading":  14,
        "textColor": BLACK,
        "spaceAfter": 0,
        "spaceBefore": 0,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

STYLES = {
    "pie_title":  S("pie_title",  fontName="Helvetica-Bold", fontSize=28,
                    alignment=TA_CENTER, textColor=DARK, spaceAfter=2),
    "pie_sub":    S("pie_sub",    fontName="Helvetica-Bold", fontSize=13,
                    alignment=TA_CENTER, textColor=DARK, spaceAfter=8),
    "label_red":  S("label_red",  fontName="Helvetica-Bold", fontSize=10,
                    textColor=RED),
    "label":      S("label",      fontName="Helvetica-Bold", fontSize=10,
                    textColor=DARK),
    "value":      S("value",      fontName="Helvetica",      fontSize=10,
                    textColor=MID_GRAY),
    "section_hdr":S("section_hdr",fontName="Helvetica-Bold", fontSize=10,
                    alignment=TA_CENTER, textColor=DARK, spaceAfter=4),
    "q_label":    S("q_label",    fontName="Helvetica-Bold", fontSize=10,
                    textColor=DARK),
    "q_body":     S("q_body",     fontName="Helvetica",      fontSize=9.5,
                    textColor=MID_GRAY, alignment=TA_JUSTIFY, leading=14),
    "footer_txt": S("footer_txt", fontName="Helvetica",      fontSize=8,
                    alignment=TA_CENTER, textColor=MID_GRAY),
    "page2_title":S("page2_title",fontName="Helvetica-Bold", fontSize=11,
                    alignment=TA_CENTER, textColor=DARK, spaceAfter=6),
    "cell_hdr":   S("cell_hdr",   fontName="Helvetica-Bold", fontSize=9,
                    alignment=TA_CENTER, textColor=WHITE),
    "cell_val":   S("cell_val",   fontName="Helvetica",      fontSize=9,
                    textColor=MID_GRAY, leading=12),
    "cell_red":   S("cell_red",   fontName="Helvetica-Bold", fontSize=9,
                    textColor=RED),
}

# ─── Page template with header/footer ────────────────────────────────────────
class HeaderFooterCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        w, h = A4

        # ── TOP: dark banner ─────────────────────────────────────────────────
        self.setFillColor(DARK)
        self.rect(0, h - 28*mm, w, 28*mm, fill=1, stroke=0)

        # University name (right side of header)
        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 12)
        self.drawRightString(w - 10*mm, h - 12*mm, "CHITKARA UNIVERSITY")
        self.setFont("Helvetica", 8)
        self.drawRightString(w - 10*mm, h - 19*mm, "Rajpura, Punjab")

        # Left: CU badge text
        self.setFillColor(GOLD)
        self.setFont("Helvetica-Bold", 16)
        self.drawString(10*mm, h - 16*mm, "CU")
        self.setFillColor(WHITE)
        self.setFont("Helvetica", 8)
        self.drawString(22*mm, h - 13*mm, "Chalkpad Innovation Portal")
        self.drawString(22*mm, h - 19*mm, "Patent Information Extraction")

        # Red accent line
        self.setStrokeColor(RED)
        self.setLineWidth(2)
        self.line(0, h - 28*mm, w, h - 28*mm)

        # ── FOOTER ────────────────────────────────────────────────────────────
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(10*mm, 18*mm, w - 10*mm, 18*mm)

        self.setFillColor(MID_GRAY)
        self.setFont("Helvetica", 7)
        self.drawCentredString(w / 2, 13*mm, ADDRESS)
        self.drawCentredString(w / 2, 9*mm,
            "Confidential | Chitkara University IPR Cell | " +
            datetime.now().strftime("%B %Y"))
        # Page number
        self.setFont("Helvetica-Bold", 8)
        self.drawCentredString(w / 2, 5*mm,
            f"{self._pageNumber}")

        self.restoreState()


# ─── Build story ─────────────────────────────────────────────────────────────
def build_pie_pdf(out_path):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        topMargin=32*mm,
        bottomMargin=25*mm,
        leftMargin=18*mm,
        rightMargin=18*mm,
    )

    story = []
    W = A4[0] - 36*mm   # usable width

    # ════════════════════ PAGE 1 ═════════════════════════════════════════════

    # ── Title block ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("PIE", STYLES["pie_title"]))
    story.append(Spacer(1, 1*mm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=RED))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("PATENT INFORMATION EXTRACTION FORM", STYLES["pie_sub"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 4*mm))

    # ── TOPIC ─────────────────────────────────────────────────────────────────
    topic_data = [[
        Paragraph("TOPIC:", STYLES["label"]),
        Paragraph(f'<font color="#C0392B"><b>{TOPIC}</b></font>',
                  S("tv", fontName="Helvetica-Bold", fontSize=10,
                    textColor=RED, leading=13)),
    ]]
    topic_tbl = Table(topic_data, colWidths=[18*mm, W - 18*mm])
    topic_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story.append(topic_tbl)

    # ── SCHOOL ────────────────────────────────────────────────────────────────
    school_data = [[
        Paragraph("SCHOOL:", STYLES["label"]),
        Paragraph(SCHOOL, STYLES["value"]),
    ]]
    school_tbl = Table(school_data, colWidths=[18*mm, W - 18*mm])
    school_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(school_tbl)
    story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER))
    story.append(Spacer(1, 4*mm))

    # ── Inventor who uploaded ─────────────────────────────────────────────────
    story.append(Paragraph(
        "<u><b>INVENTOR'S DETAIL WHO UPLOADED THE PATENT ON CHALKPAD</b></u>",
        STYLES["section_hdr"]
    ))
    story.append(Spacer(1, 3*mm))

    inv_rows = [
        ("NAME:",             PRIMARY["name"]),
        ("EMPLOYEE CODE:",    PRIMARY["emp_code"]),
        ("MOBILE NO:",        PRIMARY["mobile"]),
        ("MAIL ID (UNIVERSITY):", PRIMARY["uni_email"]),
        ("MAIL ID (PERSONAL):",   PRIMARY["per_email"]),
    ]
    for lbl, val in inv_rows:
        row = [[
            Paragraph(lbl, STYLES["label"]),
            Paragraph(val,  STYLES["value"]),
        ]]
        t = Table(row, colWidths=[48*mm, W - 48*mm])
        t.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ]))
        story.append(t)

    story.append(Spacer(1, 5*mm))

    # ── Other inventors table ─────────────────────────────────────────────────
    story.append(Paragraph(
        "<u><b>OTHER INVENTORS DETAIL</b></u>",
        STYLES["section_hdr"]
    ))
    story.append(Spacer(1, 2*mm))

    hdr = [
        Paragraph("NAME",                        STYLES["cell_hdr"]),
        Paragraph("EMP CODE / ROLL",              STYLES["cell_hdr"]),
        Paragraph("ADDRESS WITH EMAIL AND MOBILE NO.", STYLES["cell_hdr"]),
    ]
    rows = [hdr]
    labels = ["Student 1", "Student 2", "Student 3", "Student 4", "Mentor"]
    for i, (name, code, addr) in enumerate(OTHERS):
        display_name = name if name else labels[i]
        name_style   = STYLES["cell_red"] if name else STYLES["cell_red"]
        rows.append([
            Paragraph(display_name, name_style),
            Paragraph(code,         STYLES["cell_val"]),
            Paragraph(addr,         STYLES["cell_val"]),
        ])

    inv_tbl = Table(rows, colWidths=[45*mm, 32*mm, W - 77*mm],
                    repeatRows=1)
    inv_tbl.setStyle(TableStyle([
        # Header
        ("BACKGROUND",   (0,0), (-1,0), TABLE_HDR),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 9),
        ("ALIGN",        (0,0), (-1,0), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        # Rows
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LIGHT_BG]),
        # Grid
        ("GRID",         (0,0), (-1,-1), 0.5, BORDER),
        ("LINEABOVE",    (0,0), (-1,0),  1.5, DARK),
        ("LINEBELOW",    (0,-1),(-1,-1), 1,   DARK),
        # Padding
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(inv_tbl)
    story.append(Spacer(1, 6*mm))

    # ── Questions ─────────────────────────────────────────────────────────────
    story.append(Paragraph(
        "<b>Answer the following questions in brief: (use extra sheets if needed, "
        "submit pics/videos etc. which can help us to understand the invention better)</b>",
        S("qintro", fontName="Helvetica-Bold", fontSize=9.5,
          textColor=DARK, leading=13)
    ))
    story.append(Spacer(1, 5*mm))

    questions = [
        ("Q1.", "What was the problem?",
         "Video forgery and digital manipulation are growing threats in digital forensics, "
         "legal proceedings, media integrity, and security. Existing detection methods "
         "rely on limited features (1-2 methods) and lack the ability to detect both "
         "active (frame insertion/deletion) and passive (compression artifact) forgeries "
         "simultaneously. There is a critical need for a comprehensive, automated, "
         "and accurate multi-feature detection system."),

        ("Q2.", "How did you solve it (Inventive Step)?",
         "We developed a novel multi-feature fusion framework combining 7 complementary "
         "feature extraction methods: (1) Frame Difference for temporal inconsistencies, "
         "(2) DCT for compression artifacts, (3) DWT for texture analysis, "
         "(4) LBP for local pattern detection, (5) Binarization for shape changes, "
         "(6) Morphology for structural anomalies, and (7) Eigen Vector Analysis for "
         "statistical deviations. These 7 features are fused into a 12-channel tensor "
         "and processed through a frozen ResNet50 backbone followed by a custom "
         "classification head - achieving 85-95% accuracy."),

        ("Q3.", "What were the other possible solutions and why they could not be done?",
         "Keypoint Matching (SIFT/SURF): 70-80% accuracy, fails on blurred/compressed regions. | "
         "Statistical Methods: 75-85% accuracy, limited feature coverage. | "
         "Single CNN (ResNet50 only): 79% accuracy, no temporal or frequency analysis. | "
         "Deepfake-specific methods: Narrow scope, only face-swap detection. | "
         "None of these methods provide the comprehensive multi-domain analysis "
         "(temporal + frequency + spatial + statistical) needed for general video forgery detection."),

        ("Q4.", "What are the advantages of the solution proposed by you?",
         "1. High Accuracy: 85-95% on real datasets (6-16% improvement over baselines). "
         "2. Comprehensive Coverage: 7 feature types across temporal, frequency, spatial, and statistical domains. "
         "3. Robust Ensemble: Hard to fool all 7 detectors simultaneously. "
         "4. Interpretable Hybrid: Traditional CV provides explainability; deep learning provides power. "
         "5. Automated Pipeline: One-command training and prediction. "
         "6. Production-Ready: 2,500+ lines of clean, modular code. "
         "7. Transfer Learning: ResNet50 provides 23.6M pre-trained parameters at no training cost."),

        ("Q5.", "Explain the stepwise working of the innovation explaining all the components used in "
                "the invention and the specific function they are performing.",
         "Step 1 - Frame Extraction: OpenCV extracts frames from input video, resized to 240x320. "
         "Step 2 - Preprocessing: Grayscale conversion + Canny edge detection (thresholds: 100, 200). "
         "Step 3 - Feature Extraction (7 parallel methods): "
         "Frame Difference detects temporal anomalies; "
         "DCT identifies JPEG double compression; "
         "DWT (Haar) decomposes texture into 4 sub-bands; "
         "LBP encodes local texture patterns; "
         "Binarization (Otsu) extracts shape boundaries; "
         "Morphology (erosion + opening) detects structural irregularities; "
         "Eigen Vector Analysis (PCA on 8x8 patches) captures statistical anomalies. "
         "Step 4 - Feature Fusion: All features combined into 12-channel tensor (240x320x12). "
         "Step 5 - Channel Reduction: Conv2D layers reduce 12 channels to 3. "
         "Step 6 - Deep Feature Extraction: Frozen ResNet50 extracts 2048 deep features. "
         "Step 7 - Classification: Dense layers (512-256-128-1) with sigmoid output "
         "produce final binary decision: FORGED or AUTHENTIC with confidence score."),

        ("Q6.", "Attach drawing hand-made / computer made showing all the components of the invention.",
         "System Architecture Diagram:\n"
         "[ Input Video ] --> [ Frame Extraction (OpenCV) ] --> "
         "[ Preprocessing: Grayscale + Canny Edge ] --> "
         "[ 7 Feature Extractors: Frame Diff | DCT | DWT | LBP | Binary | Morphology | Eigen ] --> "
         "[ Feature Fusion: 12-Channel Tensor (240x320x12) ] --> "
         "[ Channel Reduction Conv2D: 12->3 channels ] --> "
         "[ ResNet50 Backbone (Frozen, 23.6M params) ] --> "
         "[ MaxPool + Global Average Pooling ] --> "
         "[ Dense Classifier: 512->256->128->1 ] --> "
         "[ Output: FORGED / AUTHENTIC + Confidence % ]\n\n"
         "Model Parameters: 24,827,076 total | 1,239,172 trainable (5%) | "
         "Model Size: 94.71 MB | Expected Accuracy: 85-95%"),
    ]

    for qnum, qtitle, qanswer in questions:
        q_data = [[
            Paragraph(f"<b>{qnum}</b>", STYLES["q_label"]),
            Paragraph(f"<b>{qtitle}</b>", STYLES["q_label"]),
        ]]
        q_tbl = Table(q_data, colWidths=[10*mm, W - 10*mm])
        q_tbl.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ]))
        story.append(q_tbl)
        story.append(Paragraph(qanswer, STYLES["q_body"]))

        # Answer box
        ans_data = [[""]]
        ans_tbl = Table(ans_data, colWidths=[W], rowHeights=[28*mm])
        ans_tbl.setStyle(TableStyle([
            ("BOX",         (0,0), (-1,-1), 0.5, BORDER),
            ("BACKGROUND",  (0,0), (-1,-1), LIGHT_BG),
            ("TOPPADDING",  (0,0), (-1,-1), 3),
            ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ]))
        story.append(ans_tbl)
        story.append(Spacer(1, 4*mm))

    # ════════════════════ PAGE 2 ═════════════════════════════════════════════
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(Spacer(1, 4*mm))

    # ── Key Phrases table ─────────────────────────────────────────────────────
    story.append(Paragraph(
        "Relevant Key phrases relating to your invention",
        STYLES["page2_title"]
    ))
    story.append(Spacer(1, 3*mm))

    kp_hdr = [
        Paragraph("S.No", STYLES["cell_hdr"]),
        Paragraph("Key Phrase", STYLES["cell_hdr"]),
    ]
    kp_rows = [kp_hdr]
    for sno, phrase in KEY_PHRASES:
        kp_rows.append([
            Paragraph(sno,    STYLES["cell_val"]),
            Paragraph(phrase, STYLES["cell_val"]),
        ])

    kp_tbl = Table(kp_rows, colWidths=[20*mm, W - 20*mm], repeatRows=1)
    kp_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), TABLE_HDR),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ALIGN",         (0,0), (0,-1),  "CENTER"),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
        ("LINEABOVE",     (0,0), (-1,0),  1.5, DARK),
        ("LINEBELOW",     (0,-1),(-1,-1), 1,   DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ]))
    story.append(kp_tbl)
    story.append(Spacer(1, 8*mm))

    # ── Technical Summary ─────────────────────────────────────────────────────
    story.append(Paragraph("Technical Innovation Summary", STYLES["page2_title"]))
    story.append(Spacer(1, 3*mm))

    tech_data = [
        [Paragraph("<b>Parameter</b>",   STYLES["cell_hdr"]),
         Paragraph("<b>Detail</b>",      STYLES["cell_hdr"])],
        ["Total Model Parameters",       "24,827,076"],
        ["Trainable Parameters",         "1,239,172  (5%)"],
        ["ResNet50 Frozen Parameters",   "23,587,904  (95%)"],
        ["Model File Size",              "94.71 MB  (Keras format)"],
        ["Input Tensor Shape",           "240 x 320 x 12 channels"],
        ["Feature Extraction Methods",   "7 (Frame Diff, DCT, DWT, LBP, Binary, Morphology, Eigen)"],
        ["Training Accuracy (Real Data)","85 - 95%"],
        ["Validation Accuracy",          "80 - 90%"],
        ["False Positive Rate",          "< 10%"],
        ["Processing Time",              "5 - 10 seconds per video"],
        ["Training Time",                "10 - 15 minutes  (CPU)"],
        ["Supported Formats",            "MP4, AVI, MOV, MKV, FLV, WMV"],
        ["Dataset Used",                 "REWIND Dataset  (Politecnico di Milano)  +  SULFA Dataset"],
        ["Programming Language",         "Python 3.9+"],
        ["Deep Learning Framework",      "TensorFlow 2.21+  /  Keras"],
    ]

    tech_tbl = Table(tech_data, colWidths=[70*mm, W - 70*mm], repeatRows=1)
    tech_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), TABLE_HDR),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ("GRID",          (0,0), (-1,-1), 0.5, BORDER),
        ("LINEABOVE",     (0,0), (-1,0),  1.5, DARK),
        ("LINEBELOW",     (0,-1),(-1,-1), 1,   DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("FONTNAME",      (0,1), (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (0,-1),  DARK),
    ]))
    story.append(tech_tbl)
    story.append(Spacer(1, 8*mm))

    # ── Declaration ───────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "<b>Declaration:</b>  We hereby declare that the above information is true and "
        "correct to the best of our knowledge and belief. We further declare that this "
        "invention is original and has not been disclosed publicly or filed as a patent "
        "anywhere else.",
        S("decl", fontName="Helvetica", fontSize=9, textColor=MID_GRAY,
          alignment=TA_JUSTIFY, leading=13)
    ))
    story.append(Spacer(1, 10*mm))

    # Signature block
    sig_names = [inv[0] for inv in OTHERS if inv[0]]
    sig_data = [[
        Paragraph(f"_______________\n<b>{n}</b>", S(f"sig{i}",
            fontName="Helvetica-Bold", fontSize=8.5,
            alignment=TA_CENTER, textColor=DARK, leading=12))
        for i, n in enumerate(sig_names[:3])
    ]]
    col_w = W / 3
    sig_tbl = Table(sig_data, colWidths=[col_w, col_w, col_w])
    sig_tbl.setStyle(TableStyle([
        ("ALIGN",  (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(sig_tbl)

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, canvasmaker=HeaderFooterCanvas)
    print(f"[OK] PIE Form PDF created: {out_path}")


if __name__ == "__main__":
    output = r"C:\Users\GunjanMehta\Desktop\patent\PIE_Patent_Form.pdf"
    print("Generating professional PIE Patent Form...")
    build_pie_pdf(output)
    print("Done! File saved at:", output)

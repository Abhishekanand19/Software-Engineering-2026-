"""Build the required PDF once four genuine terminal screenshots are provided."""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether,
)

ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "screenshots"
OUTPUT = ROOT / "PES1UG24CS017_Lab7_Fuzz_Testing_Report.pdf"
REQUIRED = [
    ("01_buggy_application.png", "Step 2 - Original buggy application", "An invalid withdrawal amount causes the original script to terminate with an exception."),
    ("02_failing_fuzz_tests.png", "Step 4 - Failing Hypothesis tests", "Hypothesis exposes edge-case exceptions and invalid return values in the original implementation."),
    ("03_fixed_application.png", "Step 5 - Fixed application", "The same malformed values are handled without crashing; explicit safe defaults are returned."),
    ("04_passing_fuzz_tests.png", "Step 6 - Passing Hypothesis tests", "Property-based and regression tests pass against the hardened implementation."),
]


def build_report() -> bool:
    missing = [name for name, _, _ in REQUIRED if not (SHOTS / name).exists()]
    if missing:
        print("\nPDF not generated yet: add these REAL terminal screenshots to screenshots/:")
        for name in missing:
            print("  -", name)
        print("Then rerun run_lab7.cmd (or: python build_report.py).")
        return False

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="LabTitle", parent=styles["Title"], fontSize=18, leading=22,
        textColor=colors.HexColor("#17365D"), spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="LabSection", parent=styles["Heading2"], fontSize=12,
        textColor=colors.HexColor("#17365D"), spaceBefore=10,
    ))
    styles.add(ParagraphStyle(
        name="LabCaption", parent=styles["Normal"], fontSize=10,
        leading=15, spaceAfter=8,
    ))

    # Explicit page dimensions keep screenshots clear and within the printable page.
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=42, rightMargin=42,
        topMargin=44, bottomMargin=44,
        title="Lab 7 - Fuzzing for Input Validation Bugs - ATM Withdrawal",
        author="Abhishek Anand",
    )
    width, height = A4
    frame = Frame(42, 44, width-84, height-88, leftPadding=0,
                  rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="normal", frames=[frame]))

    s = []
    s.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", styles["LabTitle"]))
    s.append(Paragraph("ATM Withdrawal - Software Engineering Lab", styles["Heading2"]))
    s.append(Spacer(1, 8))
    meta = [
        ("Student", "Abhishek Anand"),
        ("SRN", "PES1UG24CS017"),
        ("Section", "5A"),
        ("Date", date.today().strftime("%d %B %Y")),
        ("Source", "SETAPESU26/L6_L7_18_atm_withdrawal, Lab 7"),
    ]
    tab = Table([[Paragraph(f"<b>{k}</b>", styles["Normal"]), Paragraph(v, styles["Normal"])] for k,v in meta], colWidths=[110, 390])
    tab.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
    ]))
    s.append(tab)
    s.append(Paragraph("Objective", styles["LabSection"]))
    s.append(Paragraph("Use Hypothesis property-based fuzzing to identify input-validation bugs in three ATM helper functions, harden those functions, and verify the fixes with regression tests.", styles["Normal"]))
    s.append(Paragraph("Bugs identified and fixes applied", styles["LabSection"]))
    details = [
        ("notes_needed()", "Original code fails on nonnumeric/None inputs. Fixed code validates formatted nonnegative whole-number amounts and returns 0 for malformed input."),
        ("mask_card()", "Original code assumes at least four space-delimited groups. Fixed code validates a 16-digit card, supports spaces/hyphens, and only reveals the last four digits."),
        ("average_withdrawal()", "Original code fails on empty or malformed CSV input. Fixed code checks each amount and safely handles missing values before averaging."),
    ]
    for name, explanation in details:
        s.append(Paragraph(f"<b>{name}</b> - {explanation}", styles["LabCaption"]))
    s.append(Paragraph("Testing method", styles["LabSection"]))
    s.append(Paragraph("The original code and the fixed code were exercised independently with the same automated pytest/Hypothesis suite. Tests include fuzz-generated Unicode and missing inputs, valid-value properties, and explicit regression examples. The outputs shown below are captured from actual local execution.", styles["Normal"]))
    s.append(PageBreak())

    for idx, (filename, heading, explanation) in enumerate(REQUIRED):
        if idx:
            s.append(PageBreak())
        s.append(Paragraph(heading, styles["Heading2"]))
        s.append(Paragraph(explanation, styles["LabCaption"]))
        screenshot = SHOTS / filename
        image_width, image_height = ImageReader(str(screenshot)).getSize()
        max_width = width - 84
        max_height = height - 190
        scale = min(max_width / image_width, max_height / image_height, 1.0)
        img = Image(str(screenshot), width=image_width * scale, height=image_height * scale)
        img.hAlign = "CENTER"
        s.append(img)
        s.append(Spacer(1, 12))
        s.append(Paragraph(f"Evidence: <font face='Courier'>{filename}</font>", styles["LabCaption"]))

    s.append(PageBreak())
    s.append(Paragraph("Result and conclusion", styles["Heading2"]))
    s.append(Paragraph("The original implementation's input assumptions were demonstrated to fail on edge cases. Defensive validation was added to all three functions, and the same suite was used to check that the corrected code no longer crashes and preserves expected behavior on valid inputs.", styles["Normal"]))
    s.append(Spacer(1, 14))
    s.append(Paragraph("Submitted source files: <b>atm_withdrawal.py</b> and <b>test_atm_withdrawal.py</b>.", styles["Normal"]))
    doc.build(s)
    print("PDF report generated:", OUTPUT)
    return True


if __name__ == "__main__":
    build_report()

import io
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_resume_pdf(data: Dict[str, Any], template_id: str = "minimal_ats") -> bytes:
    """
    Generates a high-quality, ATS-readable PDF resume with selectable text using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    story = []

    # Configure Color Theme based on template
    if template_id == "software_engineer":
        primary_color = colors.HexColor("#0f172a")    # Slate 900
        secondary_color = colors.HexColor("#2563eb")  # Blue 600
    elif template_id == "modern_professional":
        primary_color = colors.HexColor("#1e1b4b")    # Indigo 950
        secondary_color = colors.HexColor("#7c3aed")  # Purple 600
    else:  # minimal_ats
        primary_color = colors.HexColor("#111827")    # Dark gray
        secondary_color = colors.HexColor("#374151")  # Muted gray

    # Custom Paragraph Styles
    name_style = ParagraphStyle(
        "CandidateName",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        "ContactInfo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=12
    )

    section_header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=4
    )

    bold_body_style = ParagraphStyle(
        "BoldBodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=primary_color
    )

    bullet_style = ParagraphStyle(
        "BulletTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        leftIndent=12,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=2
    )

    # --- 1. PERSONAL INFORMATION HEADER ---
    personal = data.get("personal", {})
    name = personal.get("full_name") or "John Doe"
    story.append(Paragraph(name.upper(), name_style))

    contact_parts = []
    if personal.get("email"): contact_parts.append(personal.get("email"))
    if personal.get("phone"): contact_parts.append(personal.get("phone"))
    if personal.get("location"): contact_parts.append(personal.get("location"))
    if personal.get("linkedin"): contact_parts.append(f"LinkedIn: {personal.get('linkedin')}")
    if personal.get("github"): contact_parts.append(f"GitHub: {personal.get('github')}")
    if personal.get("portfolio"): contact_parts.append(f"Portfolio: {personal.get('portfolio')}")

    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), contact_style))

    story.append(HRFlowable(width="100%", thickness=1, color=secondary_color, spaceBefore=0, spaceAfter=8))

    # --- 2. PROFESSIONAL SUMMARY ---
    summary = data.get("summary")
    if summary and summary.strip():
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_header_style))
        story.append(Paragraph(summary.strip(), body_style))
        story.append(Spacer(1, 6))

    # --- 3. EDUCATION ---
    education = data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", section_header_style))
        for edu in education:
            inst = edu.get("institution", "")
            degree = edu.get("degree", "")
            field = edu.get("field", "")
            dates = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
            gpa = edu.get("cgpa", "")

            deg_str = f"{degree} in {field}" if field else degree
            story.append(Paragraph(f"<b>{inst}</b> — <i>{deg_str}</i> ({dates})", bold_body_style))
            if gpa:
                story.append(Paragraph(f"GPA / Grade: {gpa}", body_style))
            story.append(Spacer(1, 4))

    # --- 4. WORK EXPERIENCE ---
    experience = data.get("experience", [])
    if experience:
        story.append(Paragraph("WORK EXPERIENCE", section_header_style))
        for exp in experience:
            role = exp.get("role", "")
            company = exp.get("company", "")
            location = exp.get("location", "")
            dates = f"{exp.get('start_date', '')} - {exp.get('end_date', '')}"
            desc = exp.get("description", "")

            header = f"<b>{role}</b> | {company}"
            if location: header += f" ({location})"
            story.append(Paragraph(f"{header} <font color='#6b7280'>[{dates}]</font>", bold_body_style))

            if desc:
                bullets = [b.strip() for b in desc.split("\n") if b.strip()]
                for b in bullets:
                    bullet_text = b if b.startswith("-") or b.startswith("•") else f"• {b}"
                    story.append(Paragraph(bullet_text, bullet_style))
            story.append(Spacer(1, 4))

    # --- 5. PROJECTS ---
    projects = data.get("projects", [])
    if projects:
        story.append(Paragraph("PROJECTS", section_header_style))
        for proj in projects:
            pname = proj.get("name", "")
            tech = proj.get("tech_stack", "")
            desc = proj.get("description", "")
            github_url = proj.get("github_url", "")

            title_str = f"<b>{pname}</b>"
            if tech: title_str += f" | <i>Tech: {tech}</i>"
            if github_url: title_str += f" ({github_url})"

            story.append(Paragraph(title_str, bold_body_style))
            if desc:
                bullets = [b.strip() for b in desc.split("\n") if b.strip()]
                for b in bullets:
                    bullet_text = b if b.startswith("-") or b.startswith("•") else f"• {b}"
                    story.append(Paragraph(bullet_text, bullet_style))
            story.append(Spacer(1, 4))

    # --- 6. TECHNICAL SKILLS ---
    skills = data.get("skills", {})
    if skills:
        story.append(Paragraph("TECHNICAL SKILLS", section_header_style))
        if isinstance(skills, dict):
            for cat, items in skills.items():
                if items:
                    item_str = ", ".join(items) if isinstance(items, list) else str(items)
                    story.append(Paragraph(f"<b>{cat}:</b> {item_str}", body_style))
        elif isinstance(skills, list):
            story.append(Paragraph(", ".join(skills), body_style))
        story.append(Spacer(1, 4))

    # --- 7. CERTIFICATIONS & ACHIEVEMENTS ---
    certs = data.get("certifications", [])
    achievements = data.get("achievements", [])
    if certs or achievements:
        story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS", section_header_style))
        for c in certs:
            c_text = c if isinstance(c, str) else c.get("name", "")
            story.append(Paragraph(f"• {c_text}", bullet_style))
        for a in achievements:
            a_text = a if isinstance(a, str) else a.get("title", "")
            story.append(Paragraph(f"• {a_text}", bullet_style))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

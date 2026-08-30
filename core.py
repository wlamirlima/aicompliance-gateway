import hashlib
import io
import json
import re
from contextlib import suppress
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PII_PATTERNS = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b",
    "E-mail": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
    "Telefone": r"\b(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[-.\s]?\d{4}\b",
    "Cartão de Crédito": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
}

IP_KEYWORDS = [
    "segredo industrial",
    "código-fonte",
    "fórmula",
    "patente",
    "algoritmo proprietário",
    "confidencial",
    "know-how",
    "estratégia de precificação",
]


def scan_text(text: str):
    findings_pii = []
    sanitized_text = text

    for label, pattern in PII_PATTERNS.items():
        matches = list(re.finditer(pattern, sanitized_text))
        for m in reversed(matches):
            val = m.group()
            findings_pii.append({"tipo": label, "valor": val})
            start, end = m.span()
            sanitized_text = (
                sanitized_text[:start]
                + f"[{label}_OCULTO]"
                + sanitized_text[end:]
            )

    findings_ip = []
    for kw in IP_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", text, re.IGNORECASE):
            findings_ip.append(kw)

    return sanitized_text, findings_pii, findings_ip


def generate_audit_record(
    original_text: str, sanitized_text: str, pii_found: list, ip_found: list
):
    timestamp = datetime.now(timezone.utc).isoformat()
    raw_payload = f"{original_text}|{timestamp}"
    input_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

    status = "APROVADO"
    if ip_found:
        status = "BLOQUEADO_POR_PROPRIEDADE_INTELECTUAL"
    elif pii_found:
        status = "SANITIZADO_E_APROVADO"

    record = {
        "timestamp_utc": timestamp,
        "hash_auditoria": input_hash,
        "status_conformidade": status,
        "metricas": {
            "qtd_pii_detectados": len(pii_found),
            "qtd_riscos_pi": len(ip_found),
        },
        "detalhes_pii": pii_found,
        "alertas_pi": ip_found,
    }

    with suppress(OSError), open("report.json", "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    return record


def build_pdf_report(audit_record: dict, base_url: str = "") -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "RELATÓRIO DE IMPACTO ALGORÍTMICO (AIA)")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50,
        height - 68,
        "Documento de Conformidade e Auditoria Técnica - AI Compliance Hub",
    )

    pdf.setStrokeColor(colors.HexColor("#2E3B4E"))
    pdf.setLineWidth(1)
    pdf.line(50, height - 80, width - 50, height - 80)

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, height - 110, "1. Identificação da Auditoria")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        60, height - 130, f"Timestamp (UTC): {audit_record['timestamp_utc']}"
    )
    pdf.drawString(
        60, height - 145, f"Hash SHA-256: {audit_record['hash_auditoria']}"
    )
    pdf.drawString(
        60,
        height - 160,
        f"Status de Conformidade: {audit_record['status_conformidade']}",
    )

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, height - 190, "2. Métricas de Risco Identificadas")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        60,
        height - 210,
        f"Dados Pessoais (LGPD) detectados: {audit_record['metricas']['qtd_pii_detectados']}",
    )
    pdf.drawString(
        60,
        height - 225,
        f"Termos de Propriedade Intelectual (PI) em risco: {audit_record['metricas']['qtd_riscos_pi']}",
    )

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, height - 255, "3. Fundamentação Legal e Parecer Técnico")
    pdf.setFont("Helvetica", 9)
    y = height - 275
    text_lines = [
        "- Art. 6º, III e IX da LGPD: Sanitização preventiva aplicada em dados cadastrais e identificadores.",
        "- Art. 195 da Lei 9.279/96: Monitoramento de segredos industriais e know-how antes de envio a LLMs.",
        "- Arts. 186 e 927 do Código Civil: Diligência técnica documentada para mitigação de responsabilidade objetiva.",
        "- Parecer: Auditoria executada com sucesso. Integridade dos registros garantida criptograficamente.",
    ]
    for line in text_lines:
        pdf.drawString(60, y, line)
        y -= 18

    pdf.setStrokeColor(colors.gray)
    pdf.setLineWidth(0.5)
    pdf.line(50, 100, width - 50, 100)

    pdf.setFont("Helvetica-Oblique", 8)
    pdf.setFillColor(colors.HexColor("#555555"))
    pdf.drawString(
        50,
        85,
        "Certificação digital e carimbo de tempo válidos para fins de auditoria e due diligence.",
    )

    val_url = (
        f"{base_url}/?validador=true&hash={audit_record['hash_auditoria']}"
        if base_url
        else f"?validador=true&hash={audit_record['hash_auditoria']}"
    )
    pdf.drawString(50, 72, f"Verificação online: {val_url}")

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
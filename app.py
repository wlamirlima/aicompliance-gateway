import io

import qrcode
import streamlit as st

from core import build_pdf_report, generate_audit_record, scan_text

st.set_page_config(page_title="AI Compliance & Ethics Gateway", layout="wide")

query_params = st.query_params

if "validador" in query_params:
    val_hash = query_params.get("hash", "N/A")
    val_status = query_params.get("status", "N/A")

    st.title("Portal Público de Validação de Selo Ético")
    st.markdown("---")
    st.success("Selo de Conformidade Verificado com Sucesso")

    st.subheader("Metadados do Certificado Auditado")
    st.write(f"**Hash Criptográfico:** `{val_hash}`")
    st.write(f"**Status da Auditoria:** `{val_status}`")
    st.write("**Entidade Certificadora:** AI Compliance Gateway (SaaS)")
    st.write(
        "**Validade Jurídica:** Art. 107 e 421-A do Código Civil / Art. 20 da LGPD"
    )

    if st.button("Voltar ao Painel Principal"):
        st.query_params.clear()
        st.rerun()

else:
    st.title("Sistema de Auditoria e Selo de Conformidade de IA Generativa (SaaS)")
    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1. Inserção de Dados / Prompts Corporativos")
        exemplo = "Contrato de parceria com a Empresa X. Segredo industrial: fórmula do novo componente químico. Contato do responsável: Joao Silva, CPF: 123.456.789-00, email: joao@empresa.com. O algoritmo proprietário será executado."
        input_text = st.text_area(
            "Texto / Prompt para validação:", value=exemplo, height=180
        )
        executar = st.button("Auditar e Sanitizar Dados")

    if executar or "current_audit" in st.session_state:
        if executar:
            sanitized, pii_list, ip_list = scan_text(input_text)
            audit_data = generate_audit_record(
                input_text, sanitized, pii_list, ip_list
            )
            st.session_state["current_audit"] = audit_data
            st.session_state["current_sanitized"] = sanitized
            st.session_state["current_pii"] = pii_list
            st.session_state["current_ip"] = ip_list
        else:
            audit_data = st.session_state["current_audit"]
            sanitized = st.session_state["current_sanitized"]
            pii_list = st.session_state["current_pii"]
            ip_list = st.session_state["current_ip"]

        with col_left:
            st.subheader("2. Resultado da Sanitização em Tempo Real")
            st.text_area(
                "Prompt Seguro (Pronto para envio a LLMs):",
                value=sanitized,
                height=180,
            )

            if pii_list:
                st.warning(
                    f"LGPD: {len(pii_list)} dados pessoais identificados e mascarados."
                )
            if ip_list:
                st.error(
                    f"Propriedade Intelectual: {len(ip_list)} termos protegidos detectados."
                )

        with col_right:
            st.subheader("3. Relatório de Impacto e Auditoria Criptográfica")
            st.json(audit_data)

            pdf_bytes = build_pdf_report(audit_data)
            st.download_button(
                label="Baixar Relatório de Impacto Algorítmico (PDF)",
                data=pdf_bytes,
                file_name=f"Relatorio_AIA_{audit_data['hash_auditoria'][:8]}.pdf",
                mime="application/pdf",
            )

            st.subheader("4. Selo de Conformidade e Autenticidade")

            url_prefix = ""
            if "host" in st.context.headers:
                protocol = (
                    "https"
                    if "streamlit.app" in st.context.headers["host"]
                    else "http"
                )
                url_prefix = f"{protocol}://{st.context.headers['host']}"

            qr_content = f"{url_prefix}/?validador=true&hash={audit_data['hash_auditoria']}&status={audit_data['status_conformidade']}"

            qr = qrcode.QRCode(version=1, box_size=6, border=2)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(
                buf.getvalue(),
                caption="Selo de Conformidade Auditável (QR Code Universal)",
                width=180,
            )
            st.code(audit_data["hash_auditoria"], language="text")
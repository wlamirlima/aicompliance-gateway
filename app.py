import io

import qrcode
import streamlit as st

from core import (
    build_pdf_report,
    extract_text_from_file,
    generate_audit_record,
    scan_text,
)

st.set_page_config(page_title="AI Compliance & Ethics Gateway", layout="wide")

if "audit_history" not in st.session_state:
    st.session_state["audit_history"] = []

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

        tab_texto, tab_upload = st.tabs(
            ["📝 Inserção por Texto", "📁 Upload de Documento (PDF/TXT)"]
        )

        with tab_texto:
            cenario = st.selectbox(
                "Selecione um cenário pré-configurado:",
                [
                    "Caso 1: Risco Crítico (LGPD + Segredo Industrial)",
                    "Caso 2: Apenas Dados Pessoais (LGPD)",
                    "Caso 3: Prompt Seguro (Sem dados sensíveis)",
                    "Personalizado (Digitar livremente)",
                ],
            )

            if (
                cenario
                == "Caso 1: Risco Crítico (LGPD + Segredo Industrial)"
            ):
                exemplo_padrao = "Contrato de parceria com a Empresa X. Segredo industrial: fórmula do novo componente químico. Contato do responsável: Joao Silva, CPF: 123.456.789-00, email: joao@empresa.com. O algoritmo proprietário será executado."
            elif cenario == "Caso 2: Apenas Dados Pessoais (LGPD)":
                exemplo_padrao = "Favor resumir ata de reunião com Carlos Eduardo, CPF 098.765.432-11, telefone (11) 98765-4321, email: carlos.eduardo@empresa.com."
            elif cenario == "Caso 3: Prompt Seguro (Sem dados sensíveis)":
                exemplo_padrao = "Elabore uma proposta comercial padrão de consultoria jurídica regulatória para empresas de tecnologia."
            else:
                exemplo_padrao = ""

            input_text_manual = st.text_area(
                "Texto / Prompt corporativo:", value=exemplo_padrao, height=160
            )

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Envie um contrato ou relatório (.pdf ou .txt):",
                type=["pdf", "txt"],
            )
            extracted_text = ""
            if uploaded_file is not None:
                extracted_text = extract_text_from_file(uploaded_file)
                st.info(
                    f"Arquivo carregado: **{uploaded_file.name}** ({len(extracted_text)} caracteres extraídos)"
                )

        input_text = (
            extracted_text
            if (uploaded_file is not None and extracted_text)
            else input_text_manual
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

            st.session_state["audit_history"].append(
                {
                    "Timestamp (UTC)": audit_data["timestamp_utc"],
                    "Hash": audit_data["hash_auditoria"][:12] + "...",
                    "Status": audit_data["status_conformidade"],
                    "Qtd PII": audit_data["metricas"]["qtd_pii_detectados"],
                    "Qtd Risco PI": audit_data["metricas"]["qtd_riscos_pi"],
                }
            )
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
                height=160,
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

            url_prefix = ""
            if "host" in st.context.headers:
                protocol = (
                    "https"
                    if "streamlit.app" in st.context.headers["host"]
                    else "http"
                )
                url_prefix = f"{protocol}://{st.context.headers['host']}"

            pdf_bytes = build_pdf_report(audit_data, base_url=url_prefix)
            st.download_button(
                label="Baixar Relatório de Impacto Algorítmico (PDF)",
                data=pdf_bytes,
                file_name=f"Relatorio_AIA_{audit_data['hash_auditoria'][:8]}.pdf",
                mime="application/pdf",
            )

            st.subheader("4. Selo de Conformidade e Autenticidade")

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

    if st.session_state["audit_history"]:
        st.markdown("---")
        st.subheader("5. Log de Governança e Accountability (Art. 6º, X LGPD)")
        st.dataframe(
            st.session_state["audit_history"], use_container_width=True
        )
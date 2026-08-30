# AI Compliance & Ethics Gateway (SaaS)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Plataforma SaaS de Governança, Prevenção contra Vazamento de Dados (*Data Loss Prevention - DLP*) e Auditoria Algorítmica em conformidade com a **LGPD (Lei nº 13.709/2018)**, a **Lei de Propriedade Industrial (Lei nº 9.279/1996)** e as diretrizes do **Marco Legal da IA (PL 2338/2023)**.

---

## 🎓 Contexto Acadêmico e Origem do Projeto

Este protótipo foi idealizado e **desenvolvido de forma individual e autônoma** por iniciativa própria, após o convite de um amigo para colaborar no **Projeto de Extensão Universitário** do curso de **Direito**, vinculado à disciplina de **Inovação, Empreendedorismo e Direito Digital**.

Percebendo a oportunidade de ir além de discussões puramente teóricas, a motivação para a construção deste software foi tangibilizar conceitos jurídicos complexos (*accountability*, *due diligence*, minimização de dados e responsabilidade algorítmica) em uma **ferramenta prática, auditável e 100% funcional**, demonstrando como a Engenharia de Software pode solucionar gargalos regulatórios reais no uso corporativo de Inteligência Artificial.

---

## 📌 Visão Geral do Projeto

Com a rápida adoção de Grandes Modelos de Linguagem (*LLMs*) no ambiente corporativo, surge o desafio da *Shadow AI*: o envio inadvertido de dados pessoais protegidos, termos confidenciais e segredos industriais para infraestruturas de terceiros.

O **AI Compliance & Ethics Gateway** atua como uma camada intermediária (*middleware/proxy*) de governança e proteção técnica, interceptando prompts e documentos corporativos antes da transmissão aos provedores de IA, garantindo:
1. **Sanitização Automatizada de Dados Pessoais (PII):** Mascaramento preventivo de CPF, e-mails, telefones e cartões de crédito.
2. **Inspeção de Propriedade Intelectual (PI):** Identificação e bloqueio preventivo de segredos industriais, patentes, fórmulas e códigos-fonte.
3. **Auditoria Criptográfica Imutável:** Geração de carimbo de tempo UTC e hash SHA-256 para cada requisição processada.
4. **Relatório de Impacto Algorítmico (AIA):** Emissão automática de relatório pericial em formato PDF com fundamentação jurídica e parecer técnico.
5. **Selo Ético e Validador Público (QR Code):** Verificação de integridade e conformidade acessível via dispositivo móvel por meio de um portal público dedicado.
6. **Log de Governança e Accountability:** Registro tabular dos fluxos auditados em observância ao Art. 6º, X da LGPD.

---

## 🏛️ Fundamentação Legal e Regulatória

* **Art. 6º, III e VII da LGPD:** Princípios da *Necessidade (minimização de dados)* e *Segurança* mediante aplicação de pseudonimização/mascaramento antes do processamento externo.
* **Art. 6º, X da LGPD:** Princípio da *Responsabilização e Prestação de Contas (Accountability)* demonstrado através de logs estruturados e hashes de auditoria.
* **Art. 20 da LGPD:** Direito à revisão e auditoria de decisões e fluxos orientados por inteligência artificial.
* **Art. 195 da Lei nº 9.279/1996:** Salvaguarda contra concorrência desleal e mitigação de risco de quebra de sigilo industrial.
* **Arts. 186 e 927 do Código Civil:** Materialização de diligência técnica (*due diligence*) para mitigação de responsabilidade civil objetiva da controladora.

---

## 🚀 Arquitetura e Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Web / Dashboard:** [Streamlit](https://streamlit.io/)
* **Geração de Documentos e Relatórios:** [ReportLab](https://www.reportlab.com/) (geração de PDF nativo com formatação vetorial)
* **Processamento e Extração de Documentos:** [PyPDF](https://pypdf.readthedocs.io/) (leitura e extração de texto em memória)
* **Certificação e Selos Dinâmicos:** [QRCode](https://github.com/lincolnloop/python-qrcode) & [Pillow](https://python-pillow.org/)
* **Integridade Criptográfica:** Biblioteca padrão `hashlib` (SHA-256)

---

## 📂 Estrutura de Arquivos

```text
aicompliance_app/
├── app.py              # Interface do usuário, roteamento, lógica de validação pública e exibição
├── core.py             # Motor central de sanitização (regex), hasher SHA-256 e gerador de PDF
├── requirements.txt    # Dependências do projeto para deploy e execução
├── report.json         # Registro serializado da última auditoria executada (gerado em runtime)
└── README.md           # Documentação técnica, acadêmica e regulatória do projeto
```

---

## ⚙️ Instalação e Execução Local

### 1. Clonar o repositório
```bash
git clone [https://github.com/SEU_USUARIO/aicompliance-gateway.git](https://github.com/SEU_USUARIO/aicompliance-gateway.git)
cd aicompliance-gateway
```

### 2. Criar e ativar o ambiente virtual
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
streamlit run app.py
```

---

## 📋 Demonstração Passo a Passo

1. **Seleção de Cenário ou Digitação:** Escolha um cenário pré-configurado de teste ou digite um texto corporativo.
2. **Upload de Documentos:** Se preferir, alterne para a aba de arquivo e envie um contrato em `.pdf` ou `.txt`.
3. **Execução da Auditoria:** Clique em `Auditar e Sanitizar Dados`.
4. **Download do Relatório:** Faça o download do *Relatório de Impacto Algorítmico (AIA)* em formato PDF.
5. **Verificação do Selo Ético:** Aponte a câmera do celular para o QR Code gerado na tela para acessar a página pública de validação da conformidade.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para obter mais detalhes.
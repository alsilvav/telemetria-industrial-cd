# SITRE - Sistema de Monitoramento de Linha de Triagem em Tempo Real

O **SITRE** é uma solução de telemetria e monitorização industrial projetada para integrar o ecossistema de automação do Chão de Fábrica (OT) com sistemas de TI de alta performance. O projeto simula a recolha de dados de sensores de uma esteira de triagem de caixas (*Sorter*) num Centro de Distribuição logístico, processa essas informações através de uma API robusta e exibe os indicadores num painel executivo em tempo real.



---

## 🛠️ Arquitetura do Ecossistema

A solução foi desenhada seguindo os princípios da **Indústria 4.0**, dividida em três camadas principais:

1. **Camada de Campo (Simulador IoT - Python):** Script que emula o comportamento de um CLP/Gateway de campo, gerando dados de produção (contagem de caixas no ciclo e acumulado) e condições térmicas do motor principal. Os dados são estruturados em pacotes JSON e transmitidos via requisições HTTP POST.
2. **Camada de Backend (API Core - Go/Golang):** Servidor HTTP de alta performance construído nativamente em Go. É responsável por receber a telemetria, validar os payloads, executar lógicas de interrupção (alarmes de sobreaquecimento acima de 75°C) e disponibilizar os dados na memória de forma segura para consumo.
3. **Camada de Supervisão (Dashboard - Streamlit):** Aplicação Web que consome os endpoints GET do backend para renderizar gráficos temporais de temperatura do motor e cartões com os principais KPIs de produtividade do ativo.

---

## 📊 Interface do Sistema

<img width="1576" height="734" alt="image" src="https://github.com/user-attachments/assets/d48858a1-6c48-47dd-bc04-51f8f1b466a1" />



---

## ⚙️ Tecnologias Utilizadas

* **Python 3** (Simulação de variáveis físicas e interface gráfica com Streamlit)
* **Go (Golang)** (Desenvolvimento de microsserviços e APIs REST com concorrência segura)
* **Streamlit & Pandas** (Manipulação de dados e renderização de dashboards web)
* **GitHub** (Controlo de versão e portfólio de engenharia)

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
Certifique-se de que tem o **Python** e o **Go** instalados no seu sistema operacional.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/alsilvav/telemetria-industrial-cd.git](https://github.com/alsilvav/telemetria-industrial-cd.git)
cd telemetria-industrial-cd/telemetria-industrial-cd-main

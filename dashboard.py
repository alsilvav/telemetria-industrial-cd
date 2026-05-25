import streamlit as st
import requests
import time
import pandas as pd

# Configuração da página do navegador
st.set_page_config(page_title="SITRE - Telemetria Logística", layout="wide")

st.title("📊 SITRE - Monitoramento de Linha de Triagem em Tempo Real")
st.subheader("Integração de Automação de Campo com Backend em Go")
st.markdown("---")

# Placeholder para atualizar a tela dinamicamente
dashboard_placeholder = st.empty()

# Inicializa um histórico na memória do Streamlit para o gráfico
if "historico_temp" not in st.session_state:
    st.session_state.historico_temp = []

url_api_go = "http://localhost:8080/api/dashboard"

while True:
    try:
        # Faz uma requisição GET para o backend em Go para buscar o último dado
        resposta = requests.get(url_api_go, timeout=2)
        
        if resposta.status_code == 200 and resposta.text.strip() != "":
            dados = resposta.json()
            
            # Se o ID do equipamento estiver vazio, significa que o Go ainda não recebeu dados
            if not dados.get("id_equipamento"):
                with dashboard_placeholder.container():
                    st.warning("Aguardando o envio do primeiro ciclo de dados do simulador...")
            else:
                # Armazena a temperatura atual no histórico para o gráfico (limita em 20 pontos)
                st.session_state.historico_temp.append(dados["temperatura_motor_c"])
                if len(st.session_state.historico_temp) > 20:
                    st.session_state.historico_temp.pop(0)

                # Renderiza os componentes do Dashboard
                with dashboard_placeholder.container():
                    # Cartões de Indicadores (KPIs)
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(label="ID do Ativo", value=dados["id_equipamento"])
                    
                    with col2:
                        status_texto = "🟢 OPERANDO" if dados["status_operacao"] == 1 else "🔴 PARADO / FALHA"
                        st.metric(label="Status do Sistema", value=status_texto)
                    
                    with col3:
                        st.metric(label="Último Ciclo (Caixas)", value=f"{dados['caixas_processadas_ciclo']} un")
                    
                    with col4:
                        st.metric(label="Total Acumulado", value=f"{dados['total_acumulado']} un")

                    st.markdown("### Condições do Ativo")
                    col_grafico, col_info = st.columns([3, 1])

                    with col_grafico:
                        st.write("**Histórico de Temperatura do Motor Principal (°C)**")
                        df_temp = pd.DataFrame(st.session_state.historico_temp, columns=["Temperatura"])
                        st.line_chart(df_temp)

                    with col_info:
                        st.write("**Dados Atuais do Motor**")
                        temp_atual = dados["temperatura_motor_c"]
                        st.metric(label="Temperatura", value=f"{temp_atual} °C")
                        
                        if temp_atual > 75.0:
                            st.error("⚠️ CRÍTICO: Sobreaquecimento detectado no Sorter!")
                        elif temp_atual > 68.0:
                            st.warning("⚠️ ATENÇÃO: Temperatura acima da média de operação.")
                        else:
                            st.success("✅ Temperatura estável.")

        else:
            with dashboard_placeholder.container():
                st.error("Erro ao ler dados do backend Go.")

    except requests.exceptions.ConnectionError:
        with dashboard_placeholder.container():
            st.error("❌ Erro de Conexão: O servidor Backend em Go está desligado!")

    # Atualiza o dashboard a cada 2 segundos
    time.sleep(2)

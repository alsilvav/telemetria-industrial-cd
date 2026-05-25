import time
import random
import json
import requests  # Biblioteca necessária para fazer chamadas de API (HTTP)

def simular_dados_esteira():
    total_caixas = 0
    
    # Endereço local da nossa API em Go (Porta 8080 / Endpoint /api/telemetria)
    url_api = "http://localhost:8080/api/telemetria"
    
    print("=== SIMULADOR DE ESTEIRA COM ENVIO DE API INICIADO ===")
    print(f"Enviando dados para: {url_api}\n")

    while True:
        caixas_no_ciclo = random.randint(5, 15)
        total_caixas += caixas_no_ciclo
        temperatura_motor = round(random.uniform(55.0, 78.0), 1)
        status_esteira = 1 if temperatura_motor < 76.0 else 0

        # Monta o pacote JSON
        payload = {
            "id_equipamento": "SORTER_CD_01",
            "status_operacao": status_esteira,
            "caixas_processadas_ciclo": caixas_no_ciclo,
            "total_acumulado": total_caixas,
            "temperatura_motor_c": temperatura_motor
        }

        print(f"[Simulador] Enviando ciclo de produção...")

        try:
            # DISPARO DA API: Envia o JSON via HTTP POST para o Backend em Go
            resposta = requests.post(url_api, json=payload, timeout=3)
            
            # Verifica se o backend em Go recebeu e respondeu com sucesso (Status 200)
            if resposta.status_code == 200:
                print(f"➔ Resposta do Backend Go: {resposta.text}")
            else:
                print(f"⚠️ Erro no servidor: Código de status {resposta.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Erro de Conexão: O servidor Backend em Go está desligado ou inacessível!")

        print("-" * 50)
        time.sleep(5)

if __name__ == "__main__":
    try:
        simular_dados_esteira()
    except KeyboardInterrupt:
        print("\nSimulação finalizada pelo operador.")

import time
import random
import json

def simular_dados_esteira():
    # Inicialização de variáveis simuladas
    total_caixas = 0
    
    print("=== SIMULADOR DE ESTEIRA DE TRIAGEM (SORTER) INICIADO ===")
    print("Pressione Ctrl+C para encerrar a simulação.\n")

    while True:
        # Simula a passagem de caixas na triagem (entre 5 e 15 caixas a cada 5 segundos)
        caixas_no_ciclo = random.randint(5, 15)
        total_caixas += caixas_no_ciclo
        
        # Simula a temperatura do motor principal (flutuando entre 55°C e 78°C)
        # Eventualmente simula uma sobretemperatura para testarmos alarmes no futuro
        temperatura_motor = round(random.uniform(55.0, 78.0), 1)
        
        # Status da esteira: 1 = Operando Normal, 0 = Parada/Falha
        status_esteira = 1 if temperatura_motor < 76.0 else 0

        # Monta o pacote de dados estruturado (JSON) que será enviado para a API
        payload = {
            "id_equipamento": "SORTER_CD_01",
            "status_operacao": status_esteira,
            "caixas_processadas_ciclo": caixas_no_ciclo,
            "total_acumulado": total_caixas,
            "temperatura_motor_c": temperatura_motor
        }

        # Exibe os dados gerados no terminal
        print(json.dumps(payload, indent=4))
        print("-" * 40)

        # Aguarda 5 segundos para a próxima varredura/leitura de sensores
        time.sleep(5)

if __name__ == "__main__":
    try:
        simular_dados_esteira()
    except KeyboardInterrupt:
        print("\nSimulação finalizada pelo operador.")

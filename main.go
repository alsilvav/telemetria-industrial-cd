package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// DadosEsteira define a estrutura do JSON que a API vai receber (idêntico ao payload do Python)
type DadosEsteira struct {
	IDEquipamento     string  `json:"id_equipamento"`
	StatusOperacao    int     `json:"status_operacao"`
	CaixasProcessadas int     `json:"caixas_processadas_ciclo"`
	TotalAcumulado    int     `json:"total_acumulado"`
	TemperaturaMotor  float64 `json:"temperatura_motor_c"`
}

// handlerReceberDados processa a requisição da API (Endpoint: /api/telemetria)
func handlerReceberDados(w http.ResponseWriter, r *http.Request) {
	// Garante que a API só aceite requisições do tipo POST (envio de dados)
	if r.Method != http.MethodPost {
		http.Error(w, "Método não permitido. Use POST.", http.StatusMethodNotAllowed)
		return
	}

	var dados DadosEsteira

	// Decodifica o JSON recebido diretamente para a estrutura em Go
	err := json.NewDecoder(r.Body).Decode(&dados)
	if err != nil {
		http.Error(w, "Erro ao processar o JSON: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Exibe os dados recebidos no terminal do servidor backend
	fmt.Printf("\n[API] Dados recebidos do equipamento: %s\n", dados.IDEquipamento)
	fmt.Printf("Status: %d | Caixas no Ciclo: %d | Total: %d | Temp: %.1f°C\n", 
		dados.StatusOperacao, dados.CaixasProcessadas, dados.TotalAcumulado, dados.TemperaturaMotor)

	// LÓGICA DE INTERVENÇÃO (Business Logic): Simulação de Alerta de manutenção
	if dados.TemperaturaMotor > 75.0 {
		fmt.Printf("⚠️ [ALERTA MANUTENÇÃO] Crítico: Temperatura do motor atingiu %.1f°C!\n", dados.TemperaturaMotor)
		// No futuro, colocaremos o disparo automático para a API do Telegram aqui
	}

	// Responde para o simulador (Python) que os dados foram processados com sucesso
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Dados de telemetria processados com sucesso pelo Backend Go!"))
}

func main() {
	// Define a rota/endpoint da API HTTP
	http.HandleFunc("/api/telemetria", handlerReceberDados)

	fmt.Println("🚀 Servidor Backend em Go iniciado com sucesso!")
	fmt.Println("Ouvindo na porta :8080 (Endpoint: http://localhost:8080/api/telemetria)...")

	// Inicia o servidor HTTP escutando na porta local 8080
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Erro ao iniciar o servidor: ", err)
	}
}

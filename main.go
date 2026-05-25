package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
)

// DadosEsteira define a estrutura do JSON
type DadosEsteira struct {
	IDEquipamento     string  `json:"id_equipamento"`
	StatusOperacao    int     `json:"status_operacao"`
	CaixasProcessadas int     `json:"caixas_processadas_ciclo"`
	TotalAcumulado    int     `json:"total_acumulado"`
	TemperaturaMotor  float64 `json:"temperatura_motor_c"`
}

// Variáveis globais para armazenar o último dado na memória do servidor com segurança (Thread-safe)
var (
	ultimoDado DadosEsteira
	mu         sync.Mutex
)

// handlerReceberDados processa o POST do simulador Python
func handlerReceberDados(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Método não permitido.", http.StatusMethodNotAllowed)
		return
	}

	var dados DadosEsteira
	err := json.NewDecoder(r.Body).Decode(&dados)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Salva na memória global travando o Mutex para evitar conflito de leitura/escrita
	mu.Lock()
	ultimoDado = dados
	mu.Unlock()

	fmt.Printf("\n[API] Recebido de: %s | Temp: %.1f°C | Total: %d\n", 
		dados.IDEquipamento, dados.TemperaturaMotor, dados.TotalAcumulado)

	if dados.TemperaturaMotor > 75.0 {
		fmt.Printf("⚠️ [ALERTA] Sobreaquecimento crítico no motor!\n")
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Sucesso"))
}

// handlerEnviarParaDashboard envia o último dado via GET para o Streamlit
func handlerEnviarParaDashboard(w http.ResponseWriter, r *http.Request) {
	// Permite que qualquer página web acesse essa API (CORS)
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")

	mu.Lock()
	json.NewEncoder(w).Encode(ultimoDado)
	mu.Unlock()
}

func main() {
	// Rota que recebe os dados do simulador (POST)
	http.HandleFunc("/api/telemetria", handlerReceberDados)
	
	// Rota que entrega os dados para o Dashboard (GET)
	http.HandleFunc("/api/dashboard", handlerEnviarParaDashboard)

	fmt.Println("🚀 Servidor Backend em Go atualizado!")
	fmt.Println("API Dashboard: http://localhost:8080/api/dashboard")

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}

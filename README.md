# 🗣️ Assistente de Voz Inteligente com Respostas via Planilha Google

Um assistente de voz leve, feito em Python, com reconhecimento de fala e respostas automatizadas baseadas em palavras-chave armazenadas em uma planilha pública do Google Sheets.

## 📌 Funcionalidades

- 🎤 Grava áudio do microfone continuamente
- 🧠 Reconhece comandos de voz usando Google Speech Recognition
- 📄 Busca respostas em uma planilha pública no Google Sheets (modelo De/Para)
- 🖥 Interface gráfica em `customtkinter`, com feedback visual de status
- 🔔 Mostra respostas em um pop-up automático

---

## 🖼️ Interface

- **Status**: indicador de gravação (verde) ou pausa (vermelho)
- **Pop-up**: exibe a resposta detectada
- **Botão Iniciar/Parar**: ativa ou pausa a escuta por voz

---

## 🔧 Tecnologias utilizadas

- `customtkinter`
- `tkinter`
- `sounddevice`
- `speech_recognition`
- `pandas`
- `gspread` *(opcional, se desejar autenticação para planilhas privadas)*
- `threading`, `queue`, `wave`

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone git remote add origin https://github.com/OberdanMachado/Assistente-Script.git


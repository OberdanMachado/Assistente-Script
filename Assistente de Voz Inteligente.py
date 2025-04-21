#!/usr/bin/env python
# coding: utf-8

# In[1]:


import customtkinter as ctk
import tkinter as tk
from threading import Thread
import io
import sounddevice as sd
import wave
import speech_recognition as sr
import pandas as pd
from queue import Queue
import time

# Configurações
SAMPLERATE = 44100
DURATION = 3
SHEET_URL = "https://docs.google.com/spreadsheets/d/16GsaHJr0V7Wxl0wnEWGXgD-zsyLs_8GZ/export?format=csv"
DEVICE_ID = None  # Se necessário, defina um ID de microfone com sd.query_devices()

# Controle de gravação
is_recording = False
audio_queue = Queue()

# Carregar DePara da planilha pública
def load_depara():
    try:
        df = pd.read_csv(SHEET_URL).dropna()
        depara_dict = dict(zip(df["Palavra-chave"], df["Resposta"]))
        print(f"[INFO] DePara carregado com {len(depara_dict)} palavras-chave.")
        return depara_dict
    except Exception as e:
        print(f"[ERRO] Falha ao carregar DePara do Google Sheets: {e}")
        return {}

depara_dict = load_depara()

# Gravação de áudio
def record_loop():
    print("[INFO] Iniciando gravação...")
    while is_recording:
        audio_data = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE,
                            channels=1, dtype='int16', device=DEVICE_ID)
        sd.wait()
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLERATE)
            wf.writeframes(audio_data.tobytes())
        audio_buffer.seek(0)
        audio_queue.put(audio_buffer)

# Processamento de áudio
def process_audio():
    recognizer = sr.Recognizer()
    while is_recording:
        if not audio_queue.empty():
            audio_buffer = audio_queue.get()
            try:
                with sr.AudioFile(audio_buffer) as source:
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language="pt-BR").lower()
                    print(f"[INFO] Texto reconhecido: {text}")
                    for palavra, resposta in depara_dict.items():
                        if palavra.lower() in text:
                            print(f"[MATCH] Palavra-chave detectada: {palavra} → Resposta: {resposta}")
                            update_popup(resposta)
            except sr.UnknownValueError:
                print("[INFO] Nenhum reconhecimento possível.")
            except Exception as e:
                print(f"[ERRO] Erro no reconhecimento: {e}")
        time.sleep(0.2)

# Atualiza o status na interface
def update_status():
    if is_recording:
        status_label.configure(text="Gravando...", text_color="green")
    else:
        status_label.configure(text="Pausado", text_color="red")
    root.after(200, update_status)

# Inicia ou para a gravação
def toggle_recording():
    global is_recording
    is_recording = not is_recording
    if is_recording:
        print("[INFO] Assistente ativado.")
        Thread(target=record_loop, daemon=True).start()
        Thread(target=process_audio, daemon=True).start()
        toggle_btn.configure(text="⏹ Parar", fg_color="red")
        status_label.configure(text="Gravando...", text_color="green")
    else:
        print("[INFO] Assistente pausado.")
        toggle_btn.configure(text="▶ Iniciar", fg_color="green")
        status_label.configure(text="Pausado", text_color="red")

def show_popup():
    root.deiconify()
    root.attributes("-topmost", True)
    root.after(1000, lambda: root.attributes("-topmost", False))

def update_popup(text):
    popup_label.configure(text=text, text_color="yellow")
    root.after(3000, lambda: popup_label.configure(text=""))
    show_popup()

# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Interface principal
root = ctk.CTk()
root.title("Assistente de Voz Inteligente")
root.geometry("1150x80")

frame = ctk.CTkFrame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

status_label = ctk.CTkLabel(frame, text="Pausado", text_color="red", font=("Arial", 16, "bold"))
status_label.pack(side="left", padx=10)

popup_label = ctk.CTkLabel(frame, text="", text_color="yellow", font=("Arial", 16))
popup_label.pack(side="left", padx=10)

toggle_btn = ctk.CTkButton(frame, text="▶ Iniciar", fg_color="green", text_color="white", command=toggle_recording)
toggle_btn.pack(side="right", padx=10)

root.after(100, update_status)
root.mainloop()


# In[ ]:





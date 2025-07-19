#
# Aplicação Python para Baixar vídeos no formato M3U8 da Web (necessita FFmpeg intalado previamente)
# Versão 0.1
# Data: 2025 July 19
# Daniel Schulz
#

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import threading

def baixar_video():
    endereco_web = entrada_url.get()
    nome_arquivo_base = entrada_arquivo.get()
    formato = combo_formatos.get()

    if not endereco_web or not nome_arquivo_base:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    nome_arquivo = os.path.splitext(nome_arquivo_base)[0] + '.' + formato

    comando = [
        "ffmpeg",
        "-user_agent", "Mozilla/5.0",
        "-i", endereco_web,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        nome_arquivo
    ]

    # Limpa o console antes de começar
    area_saida.configure(state='normal')
    area_saida.delete(1.0, tk.END)
    area_saida.insert(tk.END, f"Iniciando download: {nome_arquivo}\n")
    area_saida.configure(state='disabled')

    def executar_ffmpeg():
        processo = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        for linha in processo.stdout:
            atualizar_console(linha)

        processo.stdout.close()
        retorno = processo.wait()

        if retorno == 0:
            atualizar_console("\nDownload concluído com sucesso!")
        else:
            atualizar_console("\nErro ao executar o FFmpeg.")

    threading.Thread(target=executar_ffmpeg).start()

def atualizar_console(texto):
    area_saida.configure(state='normal')
    area_saida.insert(tk.END, texto)
    area_saida.see(tk.END)
    area_saida.configure(state='disabled')

# Interface Gráfica
janela = tk.Tk()
janela.title("Baixar Vídeo com FFmpeg")
janela.geometry("600x500")

tk.Label(janela, text="Endereço da URL (m3u8):").pack(pady=5)
entrada_url = tk.Entry(janela, width=70)
entrada_url.pack()

tk.Label(janela, text="Nome do arquivo de saída (sem extensão):").pack(pady=5)
entrada_arquivo = tk.Entry(janela, width=70)
entrada_arquivo.pack()

tk.Label(janela, text="Formato de saída:").pack(pady=5)
formatos_suportados = ['mp4', 'mkv', 'mov', 'avi', 'flv', 'webm', 'mpeg', 'ts', 'ogv']
combo_formatos = ttk.Combobox(janela, values=formatos_suportados, state="readonly")
combo_formatos.current(0)
combo_formatos.pack()

tk.Button(janela, text="Iniciar Download", command=baixar_video).pack(pady=15)

tk.Label(janela, text="Saída do FFmpeg:").pack(pady=5)
area_saida = scrolledtext.ScrolledText(janela, width=80, height=15, state='disabled')
area_saida.pack(padx=10, pady=5)

janela.mainloop()

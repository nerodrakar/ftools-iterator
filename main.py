import pyautogui
import time
import os
import subprocess
import pandas as pd 
import streamlit as st

# Caminhos
ftool_path = r"Ftool.exe"  
pasta_ftl = r"C:\Users\rezio\OneDrive\Documentos\.git codes\ftools iterator\arquivos"  

# Abrir o Ftool
subprocess.Popen(ftool_path)
time.sleep(5)  # Tempo para o programa abrir

# Listar arquivos .ftl
arquivos_ftl = [f for f in os.listdir(pasta_ftl) if f.endswith(".ftl")]

print(f"Arquivos encontrados: {arquivos_ftl}")

for arquivo in arquivos_ftl:
    caminho_arquivo = os.path.join(pasta_ftl, arquivo)

    # Abrir a janela de abrir arquivos (Ctrl + O)
    pyautogui.hotkey("ctrl", "o")
    time.sleep(2)

    # Digitar o caminho do arquivo e pressionar Enter
    pyautogui.write(caminho_arquivo)
    pyautogui.press("enter")
    time.sleep(3)

    # Clicar em "Axial force"
    # posicao_axial_force = pyautogui.locateCenterOnScreen("axial_button.png")
    # pyautogui.click(posicao_axial_force)
    # time.sleep(1)

    # Clicar em "Bending Moment"
    posicao_bending_moment = pyautogui.locateCenterOnScreen("bending_button.png")
    pyautogui.click(posicao_bending_moment)
    time.sleep(1)
    
    # Abrir menu "File"
    pyautogui.hotkey("alt", "f")
    time.sleep(1)

    # Mover para "Export Line Results" e selecionar "Display Resolution"
    pyautogui.press("e")  # Letra inicial de "Export Line Results"
    time.sleep(1)
    pyautogui.press("right")  # Abrir submenu
    time.sleep(1)
    pyautogui.press("d")  # Letra inicial de "Display Resolution"
    pyautogui.press("enter")
    time.sleep(3)

    # Digitar o nome do arquivo de saída
    nome_txt = arquivo.replace(".ftl", ".txt")
    pyautogui.write(os.path.join(pasta_ftl, nome_txt))
    pyautogui.press("enter")
    time.sleep(3)

    #Caso o arquivo já exista
    try:
        botao_sim = pyautogui.locateCenterOnScreen("botao_sim.png")
        if botao_sim:
            pyautogui.click(botao_sim)
            print(f'Arquivo "{nome_txt}" substituído!')
    except pyautogui.ImageNotFoundException:
        print(f'Arquivo "{nome_txt}" criado!')
        pass

    pyautogui.move(0, 400)  # Mover o mouse para a posição (0, 0) para evitar erros
    time.sleep(2)

# Fechar o Ftool
pyautogui.hotkey("alt", "f4")
print("Todos os arquivos foram processados!")

# Criando os dataframes com os arquivos .txt
dataframes = []
for file_name in os.listdir(pasta_ftl):
    if file_name.endswith(".txt"):
        file_path = os.path.join(pasta_ftl, file_name)
        with open(file_path, "r") as file:
            lines = file.readlines()[1:]  # Ignora a primeira linha
                
            # Converte os dados para um DataFrame
            data = [list(map(float, line.split())) for line in lines]
            df = pd.DataFrame(data, columns=["x", "y"])
            dataframes.append(df)

print(dataframes[0].head())


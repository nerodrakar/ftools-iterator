import pyautogui
import time
import os
import subprocess
import pandas as pd

# Caminhos
ftool_path = r"Ftool.exe"  
pasta_ftl = r"C:\Users\rezio\OneDrive\Documentos\.git codes\ftools iterator\arquivos"  

# Abrir o Ftool
subprocess.Popen(ftool_path)
time.sleep(5)  # Tempo para o programa abrir

# Listar arquivos .ftl
arquivos_ftl = [f for f in os.listdir(pasta_ftl) if f.endswith(".ftl")]

print(f"Arquivos encontrados: {arquivos_ftl}")

def salvar_resultado(nome_txt):
    """Salva o resultado no arquivo txt."""
    pyautogui.hotkey("alt", "f")
    time.sleep(1)
    pyautogui.press("e")  # Letra inicial de "Export Line Results"
    time.sleep(1)
    pyautogui.press("right")  # Abrir submenu
    time.sleep(1)
    pyautogui.press("d")  # Letra inicial de "Display Resolution"
    pyautogui.press("enter")
    time.sleep(3)

    # Digitar o nome do arquivo de saída
    pyautogui.write(os.path.join(pasta_ftl, nome_txt))
    pyautogui.press("enter")
    time.sleep(2)
    print(f'Arquivo "{nome_txt}" criado!')    


def carregar_txt_para_dataframe(nome_txt):
    """Carrega os dados do txt gerado para um dataframe."""
    file_path = os.path.join(pasta_ftl, nome_txt)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()[1:]  # Ignora a primeira linha
            data = [list(map(float, line.split())) for line in lines]
            return pd.DataFrame(data, columns=["x", "y"])
    return "Arquivo não encontrado!"

dataframes_resultados = []
numerador = 0

for arquivo in arquivos_ftl:
    if "(permanente)" in arquivo:
        caminho_arquivo = os.path.join(pasta_ftl, arquivo)

        # Abrir a janela de abrir arquivos (Ctrl + O)
        pyautogui.hotkey("ctrl", "o")
        time.sleep(2)

        # Digitar o caminho do arquivo e pressionar Enter
        pyautogui.write(caminho_arquivo)
        pyautogui.press("enter")
        time.sleep(3)

        # Clicar em "Axial Force" e salvar
        posicao_axial_force = pyautogui.locateCenterOnScreen("axial_button.png")
        pyautogui.click(posicao_axial_force)
        time.sleep(1)
        nome_axial_txt = arquivo.replace(".ftl", ".txt")
        salvar_resultado(nome_axial_txt + str(numerador))
        df_axial = carregar_txt_para_dataframe(nome_axial_txt)
        if df_axial is not None:
            dataframes_resultados.append(df_axial)

        pyautogui.move(0, 400)  # Mover o mouse para a posição (0, 400) para evitar erros

        # Clicar em "Shear Force" e salvar
        posicao_shear_force = pyautogui.locateCenterOnScreen("shear_button.png")
        pyautogui.click(posicao_shear_force)
        time.sleep(1)
        nome_shear_txt = arquivo.replace(".ftl", ".txt")
        salvar_resultado(nome_shear_txt + str(numerador))
        df_shear = carregar_txt_para_dataframe(nome_shear_txt)
        if df_shear is not None:
            dataframes_resultados.append(df_shear)

        pyautogui.move(0, 400)  # Mover o mouse para a posição (0, 400) para evitar erros

        # Clicar em "Bending Moment" e salvar
        posicao_bending_moment = pyautogui.locateCenterOnScreen("bending_button.png")
        pyautogui.click(posicao_bending_moment)
        time.sleep(1)
        nome_bending_txt = arquivo.replace(".ftl", ".txt")
        salvar_resultado(nome_bending_txt + str(numerador))
        df_bending = carregar_txt_para_dataframe(nome_bending_txt )
        if df_bending is not None:
            dataframes_resultados.append(df_bending)

        pyautogui.move(0, 400)  # Mover o mouse para a posição (0, 400) para evitar erros

        print(f"Arquivo {arquivo} processado!")
        numerador += 1

# Fechar o Ftool
pyautogui.hotkey("alt", "f4")
print("Todos os arquivos foram processados!")

# Exibir os primeiros valores dos dataframes
print("\nPrimeiros valores dos dataframes:")
for df in dataframes_resultados:
    print(df.head(10))

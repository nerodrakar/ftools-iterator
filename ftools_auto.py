import pyautogui
import time
import os
import subprocess
import pandas as pd
import numpy as np

# Caminhos
ftool_path = r"Ftool.exe"  
pasta_ftl = r"C:\Users\rezio\OneDrive\Documentos\.git codes\ftools iterator\arquivos"

# Posição de x em Bending Moment
x_value = 10.00 

# Lista de valores para modificar a carga permanente
loc = 400
scale = 0.17 * loc
N = 3
carga_permanente = list(-np.abs(np.random.gumbel(loc, scale, N)))
print(carga_permanente)

# Função para modificar o valor da carga permanente dentro do arquivo .ftl
def modificar_ftl(arquivo, novo_valor):
    caminho_arquivo = os.path.join(pasta_ftl, arquivo)
    with open(caminho_arquivo, "r") as file:
        linhas = file.readlines()

    # Substituir o valor da carga permanente
    for i in range(len(linhas)):
        if "'Permanente'" in linhas[i]:  # Identifica a linha correta
            partes = linhas[i].split()
            partes[-1] = str(novo_valor)  # Modifica o valor
            linhas[i] = " ".join(partes) + "\n"
            break

    # Escrever de volta no arquivo
    with open(caminho_arquivo, "w") as file:
        file.writelines(linhas)


# Função para salvar o resultado como .txt
def salvar_resultado(nome_txt):
    pyautogui.hotkey("alt", "f")
    time.sleep(1)
    pyautogui.press("e")  
    time.sleep(1)
    pyautogui.press("right")
    time.sleep(1)
    pyautogui.press("d")
    pyautogui.press("enter")
    time.sleep(3)

    pyautogui.write(os.path.join(pasta_ftl, nome_txt))
    pyautogui.press("enter")


# Função para carregar o arquivo .txt gerado para um dataframe
def carregar_txt_para_dataframe(nome_txt):
    """Carrega os dados do txt gerado para um dataframe."""
    file_path = os.path.join(pasta_ftl, nome_txt)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()[1:]  # Ignora a primeira linha
            data = [list(map(float, line.split())) for line in lines]
            return pd.DataFrame(data, columns=["x", "y"])
    return "Arquivo não encontrado!"


# Dicionário para armazenar os resultados
dicionario_resultados = {}

# Abrir o Ftool
subprocess.Popen(ftool_path)
time.sleep(5)

# Lista para armazenar os valores da carga permanente e y correspondente em x
resultados_xm = []

# Processamento dos arquivos
for arquivo in os.listdir(pasta_ftl):
    if arquivo.endswith(".ftl") and "(permanente)" in arquivo:
        for valor in carga_permanente:
            print(f"Processando arquivo {arquivo} com valor {valor}...")
            modificar_ftl(arquivo, valor)

            caminho_arquivo = os.path.join(pasta_ftl, arquivo)
            pyautogui.hotkey("ctrl", "o")
            time.sleep(2)

            pyautogui.write(caminho_arquivo)
            pyautogui.press("enter")
            time.sleep(2)
            # Lista para armazenar os três dataframes (Axial, Shear, Bending Moment)
            lista_df = []
            y_bending_x = None

            # Processamento das forças
            for forca, imagem in zip(["Axial", "Shear", "Bending"], ["axial_button.png", "shear_button.png", "bending_button.png"]):
                posicao_forca = pyautogui.locateCenterOnScreen(imagem)
                if posicao_forca:
                    pyautogui.click(posicao_forca)
                    time.sleep(1)
                    nome_txt = arquivo.replace(".ftl", ".txt")
                    salvar_resultado(nome_txt + str(forca))
                    time.sleep(1)
                    df_forca = carregar_txt_para_dataframe(nome_txt)
                    if isinstance(df_forca, pd.DataFrame):
                        df_forca["Forca"] = forca  # Adiciona a coluna "Forca"
                        lista_df.append(df_forca)
                        
                        # Obter o valor de y correspondente ao valor de x para Bending
                        if forca == "Bending":
                            linha_bending = df_forca.loc[df_forca["x"] == x_value]
                            if not linha_bending.empty:
                                y_bending_x = linha_bending.iloc[0]["y"]
                                print(f"y correspondente ao valor de x em Bending: {y_bending_x}")

                pyautogui.move(0, 400)  

            # Concatenar os 3 dataframes em um só
            if lista_df:
                df_final = pd.concat(lista_df, ignore_index=True)
                dicionario_resultados[valor] = df_final
                
                if y_bending_x is not None:
                    resultados_xm.append([valor, y_bending_x])

        pyautogui.hotkey("alt", "f4")

# Criar DataFrame com os resultados específicos
results_xm = pd.DataFrame(resultados_xm, columns=["P", "m"])
results_xm.to_excel("resultados_xm.xlsx", index=False)

print("\n------------------------------------------------------")

# Exibir a saída final
for carga, df in dicionario_resultados.items():
    print(f"\nCarga: {carga}")
    print(df)

print("Todos os arquivos foram processados!")

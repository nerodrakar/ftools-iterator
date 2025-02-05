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
N = 1
carga_permanente = list(-np.abs(np.random.gumbel(loc, scale, N)))
print(carga_permanente)


# Função para ajustar coordenadas conforme a resolução da tela
def ajustar_coordenadas(x_ref, y_ref):
    resolucao_referencia = (1920, 1080)
    resolucao_atual = pyautogui.size()
    x_atual = int(x_ref * resolucao_atual[0] / resolucao_referencia[0])
    y_atual = int(y_ref * resolucao_atual[1] / resolucao_referencia[1])
    return x_atual, y_atual

# Posições baseadas na tela original
botao_1 = (1435, 200)
botao_2 = (botao_1[0] + 30, botao_1[1])  
botao_3 = (botao_2[0] + 30, botao_2[1])  
botao_4 = (1375, 200)

# Ajuste para a tela atual
botao_1_ajustado = ajustar_coordenadas(*botao_1)
botao_2_ajustado = ajustar_coordenadas(*botao_2)
botao_3_ajustado = ajustar_coordenadas(*botao_3)
botao_4_ajustado = ajustar_coordenadas(*botao_4)

# Função para modificar o valor da carga permanente dentro do arquivo .ftl
def modificar_ftl(arquivo, novo_valor):
    caminho_arquivo = os.path.join(pasta_ftl, arquivo)
    with open(caminho_arquivo, "r") as file:
        linhas = file.readlines()

    for i in range(len(linhas)):
        if "'Permanente'" in linhas[i]:  
            partes = linhas[i].split()
            partes[-1] = str(novo_valor)  
            linhas[i] = " ".join(partes) + "\n"
            break

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
    file_path = os.path.join(pasta_ftl, nome_txt)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()[1:]  # Ignora a primeira linha
            data = [list(map(float, line.split())) for line in lines]
        
        num_colunas = len(data[0]) if data else 2  
        colunas = ["x", "y"] if num_colunas == 2 else ["x", "y", "z"] 
        
        return pd.DataFrame(data, columns=colunas)
    
    return "Arquivo não encontrado!"


# Abrir o Ftool
subprocess.Popen(ftool_path)
time.sleep(5)

dicionario_resultados = {}
resultados_xm = []
tempo_inicio = time.time()

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
            
            lista_df = []
            y_bending_x = None

            # Processamento das forças com cliques ajustados
            for forca, posicao_botao in zip(["Axial", "Shear", "Bending"], [botao_1_ajustado, botao_2_ajustado, botao_3_ajustado]):
                pyautogui.click(posicao_botao)
                time.sleep(1)
                nome_txt = arquivo.replace(".ftl", ".txt")
                salvar_resultado(nome_txt + str(forca))
                time.sleep(1)
                
                df_forca = carregar_txt_para_dataframe(nome_txt)
                if isinstance(df_forca, pd.DataFrame):
                    df_forca["Forca"] = forca  
                    lista_df.append(df_forca)
                    
                    if forca == "Bending":
                        linha_bending = df_forca.loc[df_forca["x"] == x_value]
                        if not linha_bending.empty:
                            y_bending_x = linha_bending.iloc[0]["y"]
                            print(f"y correspondente ao valor de x em Bending: {y_bending_x}")

                    pyautogui.move(0, 400)  


            if lista_df:
                df_final = pd.concat(lista_df, ignore_index=True)
                dicionario_resultados[valor] = df_final
                
                if y_bending_x is not None:
                    resultados_xm.append([valor, y_bending_x])

        pyautogui.hotkey("alt", "f4")
        # Criar DataFrame com os resultados específicos
        results_xm = pd.DataFrame(resultados_xm, columns=["P", "m"])
        results_xm.to_excel("resultados_permanente_xm.xlsx", index=False)

    if arquivo.endswith(".ftl") and "(variavel)" in arquivo:
        for valor in carga_permanente:
            print(f"Processando arquivo {arquivo} com valor {valor}...")
            modificar_ftl(arquivo, valor)

            caminho_arquivo = os.path.join(pasta_ftl, arquivo)
            pyautogui.hotkey("ctrl", "o")
            time.sleep(2)

            pyautogui.write(caminho_arquivo.encode("utf-8").decode("latin-1"))
            pyautogui.press("enter")
            time.sleep(2)
            
            lista_df = []
            y_bending_x = None

            pyautogui.click(botao_4_ajustado)
            time.sleep(1)

            # Processamento das forças com cliques ajustados
            for forca, posicao_botao in zip(["Shear", "Bending"], [botao_2_ajustado, botao_3_ajustado]):
                pyautogui.click(posicao_botao)
                time.sleep(1)
                nome_txt = arquivo.replace(".ftl", ".txt")
                salvar_resultado(nome_txt + str(forca))
                time.sleep(1)
                
                df_forca = carregar_txt_para_dataframe(nome_txt)
                if isinstance(df_forca, pd.DataFrame):
                    df_forca["Forca"] = forca  
                    lista_df.append(df_forca)
                    
                    if forca == "Bending":
                        linha_bending = df_forca.loc[df_forca["x"] == x_value]
                        if not linha_bending.empty:
                            y_bending_x, z_bending_x = linha_bending.iloc[0][["y", "z"]]
                            print(f"y correspondente ao valor de x em Bending: {y_bending_x}")
                            print(f"z correspondente ao valor de x em Bending: {z_bending_x}")

                    pyautogui.move(0, 400)  


            if lista_df:
                df_final = pd.concat(lista_df, ignore_index=True)
                dicionario_resultados[valor] = df_final
                
                if y_bending_x is not None:
                    resultados_xm.append([valor, y_bending_x, z_bending_x])

        pyautogui.hotkey("alt", "f4")
        # Criar DataFrame com os resultados específicos
        results_xm = pd.DataFrame(resultados_xm, columns=["P", "m1", "m2"])
        results_xm.to_excel("resultados_variavel_xm.xlsx", index=False)            



tempo_fim = time.time()
tempo_execucao = tempo_fim - tempo_inicio
print(f"Tempo total de execução: {tempo_execucao:.2f} segundos")

print("\n------------------------------------------------------")

# Exibir a saída final
for carga, df in dicionario_resultados.items():
    print(f"\nCarga: {carga}")
    print(df)

print("Todos os arquivos foram processados!")
print(f"Tempo total de execução: {tempo_execucao:.2f} segundos")
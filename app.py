import streamlit as st
import os

# Criar uma pasta no diretório onde os arquivos serão armazenados
pasta_local = "ftool_arquivos" 
os.makedirs(pasta_local, exist_ok=True)

# Obter o caminho absoluto da pasta
pasta_ftl = os.path.abspath(pasta_local)
print(f"Caminho absoluto da pasta: {pasta_ftl}")

# Recebe o arquivo .ftl
arquivos_ftl = st.file_uploader("Selecione os arquivos .ftl", type="ftl", accept_multiple_files=False)

if arquivos_ftl:
    arquivo = arquivos_ftl  
    caminho_arquivo = os.path.join(pasta_local, arquivo.name)
    
    # Verificar se o arquivo já existe e excluí-lo antes de salvar o novo
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)  # Remove o arquivo existente
    
    # Salvar o novo arquivo
    with open(caminho_arquivo, "wb") as f:
        f.write(arquivo.getbuffer())  # Salva o arquivo no diretório especificado
    
    caminho_absoluto = os.path.abspath(caminho_arquivo)  # Obtém o caminho absoluto do arquivo
    print(f"Arquivo salvo: {caminho_absoluto}")


    # Definindo os parâmetros
    x_value = 10.00 
    loc = 400
    scale = 0.17 * loc
    N = 1
    loc_P = 255
    scale_P = 0.17 * loc_P
    loc_live = 36.35
    scale_live = 0.17 * loc_live

    # Executar a automação após clique
    if st.button("Executar a automação"):
        from ftool_functions import ftools_auto_main
        dicionario_resultados, tempo_execucao = ftools_auto_main("Ftool.exe", pasta_ftl, x_value, N, loc, scale, loc_P, scale_P, loc_live, scale_live)
        
        for valor, resultados in dicionario_resultados.items():
            st.write(f"Valor: {valor}")
            st.table(resultados.head())
        st.write(f"Tempo de execução: {tempo_execucao} segundos")

        # Remover a pasta e os arquivos após a execução
        for arquivo in os.listdir(pasta_ftl):
            caminho_arquivo = os.path.join(pasta_ftl, arquivo)
            os.remove(caminho_arquivo)
        os.rmdir(pasta_ftl)
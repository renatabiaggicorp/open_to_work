import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os

# page settings
st.set_page_config(page_title="Open to Work- PED e EBA",
                   page_icon=":rocket:",
                   layout="wide")

# Title and header home page
st.title(":rocket: Open to Work - PED e EBA")
st.header("")
st.markdown("""
### Bem-vindo, Recrutador!

Esta aplicação foi desenvolvida especialmente para você, que busca candidatos com o melhor fit para sua vaga. Nosso banco de dados inclui alunos dos cursos **EBA - Estatística do Básico ao Avançado** e **PED - Preparatório para Entrevistas em Dados**, ministrados pela Tech Lead e Cientista de Dados Renata Biaggi.

**Funcionalidades da Aplicação:**

1. **Overview dos Candidatos**:
   - Tenha uma visão geral dos nossos candidatos.
   - Veja quais ferramentas são mais utilizadas.
   - Verifique a disponibilidade para novos projetos.
   - Conheça os cargos pretendidos pelos candidatos.
   

2. **Painel de Candidatos**:
   - Filtre sua própria lista de candidatos.
   - Use os filtros na aba esquerda para criar uma listagem personalizada.
   - **Sobre os filtros** : Os filtros foram pensados para que você possa rankear os candidados de acordo com o número de ferramentas que eles dominam. Quanto mais ferramentas selecionadas por vocês, o candidato tiver, maior será a colocação dele na listagem de candidatos.

**Nota Importante**:
- Não se surpreenda se algum candidato aparecer mais de uma vez na listagem. Nossos alunos possuem a bagagem técnica necessária para exercer múltiplos cargos (por exemplo, Analista de Dados ou Cientista de Dados), o que pode resultar em um mesmo candidato aparecendo em listagens de diferentes cargos pretendidos.
- Abaixo você encontrará um botão para **"Atualizar Dados"**, caso nas páginas seguintes, ocorra algum problema com o carregamento, basta clicar neste botão e tentar acessar novamente. Caso o erro persista, pode entrar em contacto com uma das autoras.
Esperamos que esta aplicação o ajude a selecionar o melhor candidato para sua empresa!
""")

# importing pipeline module
from pipeline import main, load_sheet_data, authenticate_with_google_sheets, transform_dataframe

 # Create a button to load the data 
if st.button("Atualizar Dados"):
   try:
      df = main()
        
      if df is not None:
         st.session_state["data"] = transform_dataframe(df)
         st.success("Dados atualizados com sucesso.")
      else:
         st.error("Nenhum dado retornado após a transformação.")
   except Exception as e:
      st.error(f"Erro ao carregar e transformar os dados: {e}")
      
# Messenge to confirm if the data were loaded
if 'data' in st.session_state:
    st.write("Os dados foram carregados e armazenados com sucesso. Você pode acessar os dados armazenados para outros usos.")
else:
    st.write("Clique no botão 'Atualizar Dados' para carregar e armazenar os dados.")
    
st.sidebar.write("##")
st.sidebar.markdown("Desenvolvido por :")
st.sidebar.markdown("**[Vanessa Gaigher](https://www.linkedin.com/in/vanessagaigher/)**")
st.sidebar.markdown("**[Renata Biaggi](https://renatabiaggi.com/)**") 
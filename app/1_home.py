import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os


from pipeline import main, load_sheet_data, authenticate_with_google_sheets, transform_dataframe

# page settings
st.set_page_config(page_title="Open2Work- PED e EBA",
                   page_icon=":rocket:",
                   layout="wide")

# Title and header home page
st.title(":rocket: Open2Work - PED e EBA")
st.title("")
st.markdown("""
### Bem-vindo, Recrutador!

Esta aplicação foi desenvolvida especialmente para você, que busca candidatos com o melhor fit para sua vaga.""")

#Title for button
st.markdown("##")
st.markdown("""##### Carregamento de Dados""")
st.markdown("""Clique no botão abaixo para carregar e armazenar os dados!""")

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
      
st.markdown("""No canto superior direito de cada aba, você verá uma mensagem de "Running", o que significa que os dados estão em processo de carregamento. Isto pode levar alguns segundos para que a aba **People Analytics** ou **Our Talents** sejam atualizadas. """)


st.markdown("### Sobre a nossa aplicação")
st.markdown("")
st.markdown(""" Nosso banco de dados inclui alunos dos cursos **EBA - Estatística do Básico ao Avançado** e **PED - Preparatório para Entrevistas em Dados**, ministrados pela Tech Lead e Cientista de Dados Renata Biaggi.

**Funcionalidades da Aplicação:**

1. **People Analytics Dashboard**:
   - Tenha uma visão geral dos nossos candidatos.
   - Veja quais ferramentas são mais utilizadas.
   - Verifique a disponibilidade para novos projetos.
   - Conheça os cargos pretendidos pelos candidatos.
   

2. **Our Talents**:
   - Filtre sua própria lista de candidatos.
   - Use os filtros na aba esquerda para criar uma listagem personalizada.
   - **Sobre os filtros** : Os filtros foram pensados para que você possa rankear os candidados de acordo com o número de ferramentas que eles dominam. Quanto mais ferramentas selecionadas por vocês, o candidato tiver, maior será a colocação dele na listagem de candidatos.

**Nota Importante**:
- Não se surpreenda se algum candidato aparecer mais de uma vez na listagem. Nossos alunos possuem a bagagem técnica necessária para exercer múltiplos cargos (por exemplo, Analista de Dados ou Cientista de Dados), o que pode resultar em um mesmo candidato aparecendo em listagens de diferentes cargos pretendidos.

""")


    
st.sidebar.write("##")
st.sidebar.markdown("👥 **Quer fazer parte da nossa rede de alunos?  [Conheça o PED e o EBA](https://renatabiaggi.com/)**")


st.sidebar.write("#")
st.sidebar.markdown("⚙️ **Esta aplicação foi desenvolvida por :**")
st.sidebar.markdown("**[Vanessa Gaigher](https://www.linkedin.com/in/vanessagaigher/)**")
st.sidebar.markdown("**[Renata Biaggi](https://www.linkedin.com/in/renatabiaggi/)**")
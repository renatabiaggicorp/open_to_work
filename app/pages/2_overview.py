import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import sys
import os


data_transformed = st.session_state["data"]


# Título da página
st.title('Overview dos Candidatos')

# Definindo cores de paleta:
colors = ['#4A7069', '#D9D1C7', '#F4CA49', '#D97C0B', '#A65208']

# Criando 2 colunas
st.markdown("---")
#col1, col2= st.columns(2)
col1, col2, col3 = st.columns((1, 2, 1.5))

# COLUNA 1
# Candidatos com disponibilidade de mudança (todos os 'Sim')
disponibilidade_sim = data_transformed[data_transformed['Disponibilidade de Mudança'] != 'Não'].shape[0]

# Candidatos sem disponibilidade de mudança (apenas 'Não')
disponibilidade_nao = data_transformed[data_transformed['Disponibilidade de Mudança'] == 'Não'].shape[0]

porcentagem_sim = (disponibilidade_sim / data_transformed.shape[0]) * 100
porcentagem_nao = (disponibilidade_nao / data_transformed.shape[0]) * 100

col1.markdown('##### Estatísticas Gerais')
with col1:
    st.metric(label="Total de Candidatos", value=data_transformed.shape[0])

    st.metric(label="Disponíveis para Mudança", value=f"{porcentagem_sim:.2f}%")

    st.metric(label="Não Disponíveis para Mudança", value=f"{porcentagem_nao:.2f}%")
    
col1.markdown('#')
col1.markdown('####')
col1.markdown("---")


# Grafico senioridade
senioridade_counts = data_transformed['Senioridade'].str.strip().value_counts().reset_index()
senioridade_counts.columns = ['Senioridade', 'Count']

# Criando o gráfico de barras horizontal
col1.markdown("##### Nível de Senioridade")
fig = px.bar(senioridade_counts, 
             x='Count', 
             y='Senioridade', 
             orientation='h',
             color='Senioridade',
             color_discrete_map={
                 'júnior': colors[0], 
                 'sênior': colors[1], 
                 'pleno': colors[2], 
                 'estágio': colors[3], 
                 'estágio a sênior': colors [4]
                 },
             text_auto=True
             )

# Configuração do gráfico
fig.update_layout(
    xaxis_visible=False,
    yaxis_visible=False,
    yaxis_title='',
    showlegend=True,
    width=300,  # Largura do gráfico
    height=400,  # Altura do gráfico
    legend=dict(
        x=1,          # Posição horizontal (1 é a extrema direita)
        y=0,          # Posição vertical (0 é a base)
        xanchor='right', # Ancorar a legenda no lado direito
        yanchor='bottom' # Ancorar a legenda na parte inferior
    )
)
#fig.update_traces(textposition="outside")
col1.plotly_chart(fig)


# COLUNA 2
# Grafico Modalidade trabalho
col2.markdown('##### Cargos por Modalidade de Trabalho')
df_counts = data_transformed.groupby(['Cargo Pretendido', 'Regime de Trabalho']).size().reset_index(name='Contagem')

# Calcular a porcentagem
df_counts['Porcentagem'] = df_counts.groupby('Cargo Pretendido')['Contagem'].transform(lambda x: x / x.sum() * 100)
# Arredondar os valores e formatar com '%'
df_counts['Porcentagem'] = df_counts['Porcentagem'].round(2)
df_counts['Texto'] = df_counts['Porcentagem'].astype(str) + '%'


# Criar o gráfico de barras agrupadas
fig = px.bar(df_counts, 
             x='Cargo Pretendido', 
             y='Porcentagem', 
             color='Regime de Trabalho',
             color_discrete_map={
                 'Aceito trabalhos híbridos ou remotos': colors[0], 
                 'Sem restrições - híbrido, remoto ou presencial': colors[2], 
                 'Só aceito remoto': colors[4]
                 },
             barmode='group',
             #text='Texto'  # Usar a coluna de texto formatado
            )

# Atualizar layout do gráfico
fig.update_layout(
                  xaxis_title='',
                  yaxis_title='Porcentagem',
                  legend_title='Regime de Trabalho',
                  width=800, height=400,
                  legend=dict(
                              orientation='h',  # Orientar a legenda horizontalmente
                              yanchor='top',    # Ancorar a legenda no topo
                              y= 1.8,           # Posicionar a legenda abaixo do gráfico
                              xanchor='center', # Centralizar a legenda horizontalmente
                              x=0.5             # Posição horizontal da legenda
                             )
                  )  # Tamanho do gráfico

# Atualizar a posição do texto para a parte superior das barras
fig.update_traces(textposition='outside')

# Exibir o gráfico
col2.plotly_chart(fig)
col2.markdown('---')

# Grafico Skills 
col2.markdown("##### Principais Skills dos Candidatos")

skill_mapping = {
    'Estatística básica (descritiva)': 'Estatística',
    'Estatística Avançada (testes de hipótese/ regressão)': 'Estatística'
}
def consolidate_skills(skill):
    skills = skill.split(', ')
    consolidated_skills = [skill_mapping.get(s, s) for s in skills]
    return ', '.join(consolidated_skills)

data_transformed['Skills Dominadas Consolidada'] = data_transformed['Skills Dominadas'].apply(consolidate_skills)

# Aplicar a função à coluna 'Skills Dominadas'
skills_series = data_transformed['Skills Dominadas Consolidada'].str.split(', ').explode().value_counts()
skills_series = skills_series.sort_values(ascending=True)

# Grafico de barras horizontais
fig_skills = px.bar(skills_series, 
                    x=skills_series.values, 
                    y=skills_series.index, 
                    orientation='h',
                    color_discrete_sequence = ['#4A7069', '#D9D1C7', '#F4CA49']
                    )
# Removendo legenda
fig_skills.update_layout(xaxis_visible=False,
                         yaxis_title='',
                         showlegend=False)                     
fig_skills.update_traces(textposition="outside")
col2.plotly_chart(fig_skills)

 


# COLUNA 3

# Cargos pretendidos

cargo_counts = data_transformed['Cargo Pretendido'].value_counts(normalize=True) * 100

df_cargo_counts = cargo_counts.reset_index()
df_cargo_counts.columns = ['Cargo Pretendido', 'Porcentagem']

df_cargo_counts = df_cargo_counts.sort_values(by='Porcentagem', ascending=False)

# Aplica o Streamlit
col3.markdown('##### Distribuição de Cargos Pretendidos')
col3.markdown('# ')


# Cria o gráfico de pizza
fig, ax = plt.subplots()  # Define o tamanho da figura (largura, altura)
ax.pie(df_cargo_counts['Porcentagem'], 
       labels=df_cargo_counts['Cargo Pretendido'], 
       autopct='%1.1f%%', 
       startangle=90,
       colors=[colors[0], colors[3], colors[1]])
ax.axis('equal')  # Assegura que o gráfico de pizza seja desenhado como um círculo.
col3.pyplot(fig)

col3.markdown('### ')
col3.markdown('---')

# Candidatos por país

# Grouping the data by 'País' and counting the number of candidates
df_countries = data_transformed.groupby('País').size().reset_index(name='Número de Candidatos')

# Convert the max value to an int to ensure it's JSON serializable
max_value = int(df_countries['Número de Candidatos'].max())

# Custom HTML and CSS for styling
html = df_countries.to_html(
    index=False,
    classes='dataframe'
    
)

# Adding custom CSS for the headers and table
css = """
<style>
.dataframe thead th {
    background-color: #f5f5f5; /* Change to your desired header color */
    color: #333; /* Change to your desired text color */
    text-align: center;
}
.dataframe td {
    text-align: center;
}
</style>
"""

# Combine CSS and HTML
html = css + html

# Display the styled dataframe

col3.markdown('##### Candidatos por Países')
col3.markdown('# ')
col3.markdown(html, unsafe_allow_html=True)





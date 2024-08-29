import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import sys
import os


data_transformed = st.session_state["data"]


# Page Title
st.title('People Analytics Dashboard')
st.markdown("""
Veja abaixo as principais características dos nossos candidatos. Nosso foco foi em dar uma visão geral, a você recrutador, das estatísticas gerais acerca da disponibilidade de mudança, cargos pretendidos, ferramentas mais utilizadas pelos nossos talentos e modalidade de trabalho pretendida.

**Sabemos que pode encontrar a pessoa que você precisa bem aqui!**
""")


# Define color pallet
colors = ['#4A7069', '#D9D1C7', '#F4CA49', '#D97C0B', '#A65208']

# Create 3 columns
st.markdown("---")
col1, col2, col3 = st.columns((1, 2, 1.5))

# COLUMN 1
# Candidates willing to move ('Yes')
disponibilidade_sim = data_transformed[data_transformed['Disponibilidade de Mudança'] != 'Não'].shape[0]

# Candidates without availability to change ('No')
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


# Seniority graph
senioridade_counts = data_transformed['Senioridade'].str.strip().value_counts().reset_index()
senioridade_counts.columns = ['Senioridade', 'Count']

# Creating the horizontal bar chart
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

# Settings
fig.update_layout(
    xaxis_visible=False,
    yaxis_visible=False,
    yaxis_title='',
    showlegend=True,
    width=300,  
    height=400,  
    legend=dict(
        x=1,          # horizontal position (1 is on the right)
        y=0,          # vertical position (0 is under)
        xanchor='right', # Anchor the caption on the right side
        yanchor='bottom' # Anchor the caption at the bottom
    )
)
#fig.update_traces(textposition="outside")
col1.plotly_chart(fig)


# COLUMN 2
# Work mode graphic
col2.markdown('##### Cargos por Modalidade de Trabalho')
df_counts = data_transformed.groupby(['Cargo Pretendido', 'Regime de Trabalho']).size().reset_index(name='Contagem')

# Calculate percentage
df_counts['Porcentagem'] = df_counts.groupby('Cargo Pretendido')['Contagem'].transform(lambda x: x / x.sum() * 100)
# Round 2 and format with '%'
df_counts['Porcentagem'] = df_counts['Porcentagem'].round(2)
df_counts['Texto'] = df_counts['Porcentagem'].astype(str) + '%'


# Create the clustered bar chart
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
            )

# Update chart layout
fig.update_layout(
                  xaxis_title='',
                  yaxis_title='Porcentagem',
                  legend_title='Regime de Trabalho',
                  width=800, height=400,
                  legend=dict(
                              orientation='h', 
                              yanchor='top',    
                              y= 1.8,           # Position the legend below the graph
                              xanchor='center', # Center caption horizontally
                              x=0.5             # Horizontal position of the caption
                             )
                  )

# Update text position to top of bars
fig.update_traces(textposition='outside')

col2.plotly_chart(fig)
col2.markdown('---')

# Skills Graphs
col2.markdown("##### Principais Skills dos Candidatos")

skill_mapping = {
    'Estatística básica (descritiva)': 'Estatística',
    'Estatística avançada (testes de hipótese/ regressão)': 'Estatística'
}
def consolidate_skills(skill):
    skills = skill.split(', ')
    consolidated_skills = [skill_mapping.get(s, s) for s in skills]
    return ', '.join(set(consolidated_skills))

data_transformed['Skills Dominadas Consolidada'] = data_transformed['Skills Dominadas'].apply(consolidate_skills)

# Apply the function from the 'Mastered Skills' column
skills_series = data_transformed['Skills Dominadas Consolidada'].str.split(', ').explode().value_counts()
total_candidates = len(data_transformed)
skills_percentage = round((skills_series / total_candidates) * 100,2)
skills_percentage = skills_percentage.sort_values(ascending=True)

# creating df
df_skills_percentage = pd.DataFrame({
    'Skill': skills_percentage.index,
    'Percentual': skills_percentage.values
})
# Horizontal bar chart
fig_skills = px.bar(df_skills_percentage, 
                    x='Percentual', 
                    y='Skill', 
                    orientation='h',
                    color_discrete_sequence = ['#4A7069', '#D9D1C7', '#F4CA49']
                    )
# Removing subtitle
fig_skills.update_layout(xaxis_visible=False,
                         yaxis_title='',
                         showlegend=False)                     
fig_skills.update_traces(textposition="outside")
col2.plotly_chart(fig_skills)

 
# COLUMN 3

# Desired positions

cargo_counts = data_transformed['Cargo Pretendido'].value_counts(normalize=True) * 100

df_cargo_counts = cargo_counts.reset_index()
df_cargo_counts.columns = ['Cargo Pretendido', 'Porcentagem']

df_cargo_counts = df_cargo_counts.sort_values(by='Porcentagem', ascending=False)

col3.markdown('##### Distribuição de Cargos Pretendidos')
col3.markdown('#####')
col3.write('')

# Create the pie chart
fig, ax = plt.subplots(figsize=(5,5)) 
ax.pie(df_cargo_counts['Porcentagem'], 
       labels=df_cargo_counts['Cargo Pretendido'], 
       autopct='%1.1f%%', 
       startangle=90,
       colors=[colors[0], colors[3], colors[1]])
ax.axis('equal')  
col3.pyplot(fig)

col3.markdown('## ')
col3.markdown('---')

# Candidates by country

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


st.markdown("""
**NOTA IMPORATANTE**: As estatísticas mencionadas não incluem candidatos únicos. Nossos alunos possuem a formação técnica necessária para atuar em diversos cargos. Portanto, nossa abordagem é sempre alinhada com o cargo específico almejado.
""")


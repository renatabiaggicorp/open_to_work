import streamlit as st
import pandas as pd
from io import BytesIO

# Load the data from session state
data = st.session_state["data"]
data_transformed = data[['Nome_Completo',
                         'Email',
                         'Telefone',
                         'LinkedIn',
                         'Disponibilidade de Mudança',
                         'Regime de Trabalho',
                         'Formação Acadêmica',
                         'Experiência em Dados',
                         'Descrição da Experiência',
                         'Cargo Pretendido',
                         'Cargo Atual',
                         'Regime de Estudo',
                         'Skills Dominadas',
                         'Cursos Cursados',
                         'Nível de Inglês',
                         'Senioridade',
                         'País',
                         'Estado',
                         'Cidade']]

# Title of the page
st.title('Our Talents')
st.markdown("""
            Chegou a hora de encontrar o seu candidato. Use os filtros que encontrará do lado esquerdo para selecionar a sua listagem de candidatos de acordo com os requisitos da vaga.\n
            
            Os filtros foram projetados para permitir que você classifique os candidatos com base na quantidade de ferramentas que eles dominam. Quanto mais ferramentas você selecionar e o candidato dominar, mais alta será a posição dele na lista de candidatos.\n
            
            Ao final, você poderá fazer o download da listagem dos candidados. Basta clicar no botão que encontrará ao final da página!""" )

st.title('')

# List of uniques values to buttons
cargos_disponiveis = data_transformed['Cargo Pretendido'].unique()
paises_disponiveis = data_transformed['País'].unique()
paises_disponiveis = ['Selecione um País'] + list(paises_disponiveis)
estados_disponiveis = data_transformed['Estado'].unique()
cidades_disponiveis = data_transformed['Cidade'].unique()
modalidades_disponiveis = data_transformed['Regime de Trabalho'].unique()
senioridade_disponiveis = data_transformed['Senioridade'].unique()
ferramentas_disponiveis = sorted(set(
    ferramenta.strip()
    for ferramentas in data_transformed['Skills Dominadas'].dropna().str.split(',')
    for ferramenta in ferramentas
))


# User interface: filters
cargo_selecionado = st.sidebar.multiselect('Selecione o cargo pretendido', cargos_disponiveis)
pais_selecionado = st.sidebar.selectbox('Selecione um País', paises_disponiveis)
estado_selecionado = st.sidebar.multiselect('Selecione o Estado desejado (Opcional)', estados_disponiveis)
cidade_selecionada = st.sidebar.multiselect('Selecione a cidade desejada (Opcional)', cidades_disponiveis)
modalidade_selecionada = st.sidebar.multiselect('Selecione a modalidade de trabalho (opcional)', modalidades_disponiveis)
ferramentas_selecionadas = st.sidebar.multiselect('Selecione as ferramentas dominadas (opcional)', ferramentas_disponiveis)
senioridade_selecionadas = st.sidebar.multiselect('Selecione o nível de senioridade', senioridade_disponiveis)


if cargo_selecionado:
    
    df_filtrado = data_transformed[
        data_transformed['Cargo Pretendido'].isin(cargo_selecionado)]

    if pais_selecionado != 'Selecione um País':
        df_filtrado = df_filtrado[
    (df_filtrado['País'] == pais_selecionado) |
    (df_filtrado['Disponibilidade de Mudança'] == 'Sim - para outra cidade/estado ou país')]
    else:
        df_filtrado 
    

    if estado_selecionado:
        df_filtrado = df_filtrado[
            (df_filtrado['Estado'].isin(estado_selecionado)) |
            (df_filtrado['Disponibilidade de Mudança'] == 'Sim - para outra cidade/estado')
        ]
    if cidade_selecionada:
        df_filtrado = df_filtrado[
            (df_filtrado['Cidade'].isin(cidade_selecionada)) |
            (df_filtrado['Disponibilidade de Mudança'] == 'Sim - para outra cidade')
        ]
   
    if modalidade_selecionada:
        df_filtrado = df_filtrado[df_filtrado['Regime de Trabalho'].isin(modalidade_selecionada)]

    if ferramentas_selecionadas:
        def count_ferramentas(ferramentas_row, ferramentas_selecionadas):
            ferramentas_row = [f.strip() for f in ferramentas_row.split(',')]
            return sum(f in ferramentas_selecionadas for f in ferramentas_row)
        
        df_filtrado['Contagem Ferramentas Selecionadas'] = df_filtrado['Skills Dominadas'].apply(lambda x: count_ferramentas(x, ferramentas_selecionadas))
        df_filtrado = df_filtrado[df_filtrado['Contagem Ferramentas Selecionadas']>0]
        df_filtrado = df_filtrado.sort_values(by='Contagem Ferramentas Selecionadas', ascending =False)
        # removing the count column before displaying
        df_final = df_filtrado.drop(columns=['Contagem Ferramentas Selecionadas'])
        
        #resettting the index of the dataframe
        df_final = df_final.reset_index(drop =True)
    else:
        df_final = df_filtrado.reset_index(drop=True)
        
    if senioridade_selecionadas:
        df_final = df_final[df_final['Senioridade'].isin(senioridade_selecionadas)]
    
    st.write("**Resultados Filtrados**")
    st.dataframe(df_final.reset_index(drop=True))

else:
    st.write("**Por favor, selecione pelo menos um cargo pretendido.**")

# Function to convert DataFrame to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Candidatos')
    processed_data = output.getvalue()
    return processed_data

# Download button
if 'df_filtrado' in locals() and not df_final.empty:
    excel_data = to_excel(df_final)
    st.download_button(label='Baixar dados em Excel',
                       data=excel_data,
                       file_name='candidatos.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

st.title("")
st.markdown("""
**NOTA IMPORTANTE:** É possível que um mesmo candidato apareça mais de uma vez. Como mencionado anteriormente, o mesmo candidato pode concorrer a vagas em diferentes cargos e níveis de senioridade.""")
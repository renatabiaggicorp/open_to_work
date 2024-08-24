import streamlit as st
import pandas as pd
from io import BytesIO

# Load the data from session state
data = st.session_state["data"]
data_transformed = data[['Nome_Completo',
                         'Email',
                         'Telefone',
                         'LinkedIn',
                         'Localização',
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
                         'Cidade',
                         'Estado']]

# Title of the page
st.title('Our Talents')
st.markdown("""
            Chegou a hora de encontrar o seu candidato. Use os filtros que encontrará do lado esquerdo para selecionar a sua listagem de candidatos de acordo com os requisitos da vaga.\n
            
            Os filtros foram projetados para permitir que você classifique os candidatos com base na quantidade de ferramentas que eles dominam. Quanto mais ferramentas você selecionar e o candidato dominar, mais alta será a posição dele na lista de candidatos.\n
            
            Ao final, você poderá fazer o download da listagem dos candidados. Basta clicar no botão que encontrará ao final da página!""" )

st.title('')
# List of available positions and work modalities
cargos_disponiveis = data_transformed['Cargo Pretendido'].unique()
modalidades_disponiveis = data_transformed['Regime de Trabalho'].unique()
ferramentas_disponiveis = sorted(set(
    ferramenta.strip()
    for ferramentas in data_transformed['Skills Dominadas'].dropna().str.split(',')
    for ferramenta in ferramentas
))

# User interface
cargo_selecionado = st.sidebar.multiselect('Selecione o cargo pretendido', cargos_disponiveis)
modalidade_selecionada = st.sidebar.multiselect('Selecione a modalidade de trabalho (opcional)', modalidades_disponiveis)
ferramentas_selecionadas = st.sidebar.multiselect('Selecione as ferramentas dominadas (opcional)', ferramentas_disponiveis)

# Creating a new dataframe with the filtered values
if not cargo_selecionado:
    st.write("**Nenhum cargo selecionado. Por favor, selecione pelo menos um cargo.**")
else:
    df_cargos = data_transformed[data_transformed['Cargo Pretendido'].isin(cargo_selecionado)]

    if modalidade_selecionada:
        df_modalidade = df_cargos[df_cargos['Regime de Trabalho'].isin(modalidade_selecionada)]
    else:
        df_modalidade = df_cargos

    if ferramentas_selecionadas:
        def count_ferramentas(ferramentas_row, ferramentas_selecionadas):
            ferramentas_row = [f.strip() for f in ferramentas_row.split(',')]
            return sum(f in ferramentas_selecionadas for f in ferramentas_row)

        df_modalidade['Contagem Ferramentas Selecionadas'] = df_modalidade['Skills Dominadas'].apply(lambda x: count_ferramentas(x, ferramentas_selecionadas))
        df_modalidade = df_modalidade[df_modalidade['Contagem Ferramentas Selecionadas'] > 0]
        df_modalidade = df_modalidade.sort_values(by='Contagem Ferramentas Selecionadas', ascending=False)
        # Remove the count column before displaying
        df_final = df_modalidade.drop(columns=['Contagem Ferramentas Selecionadas'])

        # Resetting the index of the DataFrame
        df_final = df_final.reset_index(drop=True)
    else:
        df_final = df_modalidade

    st.dataframe(df_final)

    # Function to convert DataFrame to Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Candidatos')
        processed_data = output.getvalue()
        return processed_data

    # Download button
    excel_data = to_excel(df_final)
    st.download_button(label='Baixar dados em Excel',
                        data=excel_data,
                        file_name='candidatos.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

st.title("")
st.markdown("""
**NOTA IMPORTANTE:** É possível que um mesmo candidato apareça mais de uma vez. Como mencionado anteriormente, o mesmo candidato pode concorrer a vagas em diferentes cargos e níveis de senioridade.""")
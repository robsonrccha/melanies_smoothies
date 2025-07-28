# # Import python packages
# import streamlit as st
# #from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col

# # Write directly to the app
# st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
# st.write(
#   """Choose the fruits you want in your custom Smoothie!.
#   """
# )


# title = st.text_input('Name on Smoothie:')
# st.write("The name on your Smoothie will be: ", title)

# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# #st.dataframe(data = my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     my_dataframe,
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen+' '

#     #st.write(ingredients_string)

#     my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('"""+ingredients_string+"""','"""+title+"""')"""

#     #st.write(my_insert_stmt)
#     #st.stop()
    
# time_to_insert = st.button('Submit Order')

# if time_to_insert:
#     session.sql(my_insert_stmt).collect()
        
#     st.success('Your Smoothie is ordered, ' + title + '', icon="✅")
# 1. Importações limpas (sem duplicatas)


import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Título e descrição do app
st.title("Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Campo para o nome do cliente no pedido
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Conexão com o Snowflake
cnx = st.connection('snowflake')
session = cnx.session()

# Busca as colunas FRUIT_NAME e a nova SEARCH_ON da tabela de opções de frutas
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Converte o DataFrame do Snowpark para um DataFrame do Pandas
pd_df = my_dataframe.to_pandas()

# Cria a lista de frutas que será exibida ao usuário
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Componente de seleção múltipla para o usuário escolher os ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5  # 2. Corrigido de volta para 5, conforme as instruções
)

# Bloco de código que só é executado se o usuário escolher algum ingrediente
if ingredients_list:
    ingredients_string = ''

    # Loop para cada fruta escolhida pelo usuário
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Usa o Pandas para encontrar o valor de busca correto
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Faz a chamada para a API Fruityvice usando o valor de busca correto
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on )
        
        # Exibe as informações nutricionais
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # Cria a declaração SQL para inserir o pedido
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{}', '{}')
    """.format(ingredients_string, name_on_order)

    # Cria o botão para submeter o pedido
    time_to_insert = st.button('Submit Order')

    # Se o botão for clicado, executa o SQL e mostra uma mensagem de sucesso
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅") # 3. Vírgula final removida


        

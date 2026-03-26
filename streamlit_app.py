  # Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
cnx = st.connection("snowflake")
#session = cnx.session()

# Write directly to the app
st.title ("Customise your Smoothie!:cup_with_straw:")
st.write("""Choose the fruits you want in your Smoothie .""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose Upto 5 Ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    ingredients_string = ''

for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

   
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered!', icon="✅")

df = cnx.query("SELECT * FROM smoothies.public.orders")
for row in df.itertuples():
 st.write(f"Order ID: {row.ORDER_ID}, Name on Order: {row.NAME_ON_ORDER}, Ingredients: {row.INGREDIENTS}")
   

    
   

    

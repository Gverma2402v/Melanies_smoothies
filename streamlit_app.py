# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose you fruits you want in your Smoothie!
    """
)

name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on your smoothie will be ',name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))

pd_df=my_dataframe.to_pandas()


ingredient_list= st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredient_string = ''

    for fruit_choosen in ingredient_list:
        ingredient_string += fruit_choosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME']==fruit_choosen,'SEARCH_ON'].iloc[0]
       # st.write('The Search value for ',fruit_choosen,' is ', search_on,'.')
                 
        st.subheader(fruit_choosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        fv_df=st.dataframe(data =fruityvice_response.json(),use_container_width=True)


    
    #st.write(ingredient_string)
 

    my_insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order)
                  values('"""+ingredient_string+"""','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)

  

    time_to_insert= st.button('Submit Order')
  
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!,'""+name_on_order+""'', icon="✅")




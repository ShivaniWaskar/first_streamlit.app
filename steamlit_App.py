import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents new healty Dinner')
streamlit.header('🍞Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('avacado')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    # streamlit.text(fruityvice_response.json())
    # write your own comment -what does the next line do? 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
    
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function=get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()




streamlit.header("fruit load list contains:")
# snowflake related function
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()
# add button to te list
if streamlit.button('get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_row=get_fruit_load_list()
   streamlit.dataframe(my_data_row)
# allow user to add fruit 
def insert_row_snowfalke(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into FRUIT_LOAD_LIST values ('kiwi')")
      return "Thanks for adding" + new_fruit
add_my_fruit=streamlit.text_input("what fruit would you like to add")
if streamlit.button('add fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowfalke(add_my_fruit)
   streamlit.text(back_from_function)
streamlit.stop()


# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# # my_data_row = my_cur.fetchone()
# # streamlit.text("Hello from Snowflake:")
# # streamlit.text(my_data_row)
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchall()
# streamlit.header("fruit load list contains:")
# streamlit.dataframe(my_data_row)
add_my_fruit=streamlit.text_input("what fruit would you like to add",'jackfruit')
streamlit.write('thanks for addding', add_my_fruit)
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
# my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")

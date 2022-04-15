# streamlit_app.py

import streamlit as st
import psycopg2
from psycopg2 import Error

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


try:
  connection = init_connection()
  #Creamos el cursor para las operaciones de la base de datos
  cursor = connection.cursor()
  #Creamos una variable con el codigo sql que queremos que se ejecute
  select_query = ''' SELECT * 
  FROM PUBLIC.landlords
  WHERE id > 500;'''
  #Executamos el comando
  cursor.execute(select_query)
  connection.commit()
  #con la funcion fetchall() podemos ver lo que retornaria la base de datos 
  st.write("Result ", cursor.fetchall())

#Por si la conexion no fue exitosa
except (Exception, Error) as error:
  print("Error while connecting to PostgreSQL", error)
finally:
  if (connection):
#     cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

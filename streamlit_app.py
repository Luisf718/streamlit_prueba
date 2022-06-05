# streamlit_app.py

import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Booking Visualization",
                   page_icon=":bar_chart:",
                   layout="wide"
                  )

#Global Constants
PSQL_HOST = "ec2-54-165-184-219.compute-1.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "xouugvjvpdqxzl"
PSQL_PASS = "0cfc12f2ea32b36baffa66379813f12ea2e1a18b65b01224249f90875ce63137"
PSQL_DB = "duminr7s43tjt"

#Connection
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
""" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
connection = psycopg2.connect(connection_address)

#Query
query_users = """SELECT
                public.users.first_name as "Primer Nombre",
                public.users.last_name as "Apellido",
                public.users.gender as "Genero",
                public.users.birth_day as "Cumpleaños",
                public.countries.country as "País",
                public.states.states as "Estado",
                public.property_types.property_type as "Propiedad Preferida"
            FROM public.users
                LEFT JOIN
                    public.countries
                ON
                    public.users.country = public.countries.id
                
                LEFT JOIN
                    public.states
                ON
                    public.users.states = public.states.id
                
                LEFT JOIN
                    public.property_types
                ON
                    public.users.property_preference = public.property_types.id
                
            ORDER BY public.users.id ASC LIMIT 100;"""

#Total reservations by confirmed----------------------------------------------------------------------------
quey_total_reservations_by_confirmed ="""SELECT public.booking.confirmed as "Confirmación", COUNT(*) As Total
                                         FROM public.booking
                                         GROUP BY public.booking.confirmed;"""

total_reservations_by_confirmed = pd.read_sql_query(quey_total_reservations_by_confirmed, con=connection)

total_reservations = int(total_reservations_by_confirmed["total"].sum())

#Reservations by Month confirmed --------------------------------------------------------------------------------------------

query_total_reservations_by_month_confirmed ="""SELECT TO_CHAR(public.booking.reservation_date, 'Month') as "mes", COUNT(*) As "reserva confirmada"
                                                FROM public.booking
                                                WHERE public.booking.confirmed = true
                                                GROUP BY "mes";"""

total_reservations_by_month_confirmed = pd.read_sql_query(query_total_reservations_by_month_confirmed, con=connection)

#Reservations by Month unconfirmed --------------------------------------------------------------------------------------------

query_total_reservations_by_month_unconfirmed ="""SELECT TO_CHAR(public.booking.reservation_date, 'Month') as "mes", COUNT(*) As "reserva no confirmada"
                                                FROM public.booking
                                                WHERE public.booking.confirmed = false
                                                GROUP BY "mes";"""

total_reservations_by_month_unconfirmed = pd.read_sql_query(query_total_reservations_by_month_unconfirmed, con=connection)

#Preference property--------------------------------------------------------------------------------------------

#prueba = pd.read_sql_query(query_users, con=connection)

# ---- MAINPAGE ----
st.title(":bar_chart: Bookng visualization")

st.markdown("##")

column_1, column_2 = st.columns(2)

with column_1:
    st.subheader("Total reservatios: ")
    st.subheader(f"{total_reservations}")

with column_2:
    st.subheader("Reservatios average by confirm: ")
    st.subheader(round(total_reservations_by_confirmed['total'].mean(),2))

st.markdown("---")

#Graph reservations by confirmation
fig_total_reservations_by_confirmed = px.bar(
    total_reservations_by_confirmed,
    x = "total",
    y = "Confirmación",
    orientation = "h",
    title = "<b>Total Places by country</b>",
    color_discrete_sequence = ["#0083B8"] * len(total_reservations_by_confirmed),
    template = "plotly_white",
)

fig_total_reservations_confirmed = px.line(
    total_reservations_by_month_confirmed,
    x = "mes",
    y = "reserva confirmada",
    markers = True
)

fig_total_reservations_confirmed.update_layout(plot_bgcolor = "rgba(229,236,246,255)")

fig_total_reservations_unconfirmed = px.line(
    total_reservations_by_month_unconfirmed,
    x = "mes",
    y = "reserva no confirmada",
    markers = True
)

fig_total_reservations_unconfirmed.update_layout(plot_bgcolor = "rgba(229,236,246,255)")

st.plotly_chart(fig_total_reservations_by_confirmed)

column_graph_1, column_graph_2 = st.columns(2)

with column_graph_1:
    st.subheader("Rerservas confirmadas por mes")

with column_graph_2:
    st.subheader("Rerservas sin confirmar por mes")

column_graph_1.plotly_chart(fig_total_reservations_confirmed, use_container_width = True)
column_graph_2.plotly_chart(fig_total_reservations_unconfirmed, use_container_width = True)

import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

#Global Constants
PSQL_HOST = "ec2-54-165-184-219.compute-1.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "xouugvjvpdqxzl"
PSQL_PASS = "0cfc12f2ea32b36baffa66379813f12ea2e1a18b65b01224249f90875ce63137"
PSQL_DB = "duminr7s43tjt"

#Connection
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
""" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
connection = psycopg2.connect(connection_address)

#Query
query_users = """SELECT
                public.users.first_name as "Primer Nombre",
                public.users.last_name as "Apellido",
                public.users.gender as "Genero",
                public.users.birth_day as "Cumpleaños",
                public.countries.country as "País",
                public.states.states as "Estado",
                public.property_types.property_type as "Propiedad Preferida"
            FROM public.users
                LEFT JOIN
                    public.countries
                ON
                    public.users.country = public.countries.id
                
                LEFT JOIN
                    public.states
                ON
                    public.users.states = public.states.id
                
                LEFT JOIN
                    public.property_types
                ON
                    public.users.property_preference = public.property_types.id
                
            ORDER BY public.users.id ASC LIMIT 100;"""

#Total Places----------------------------------------------------------------------------
quey_total_places_by_country ="""SELECT
                                    public.countries.country as País,  COUNT(*) As Total
                                FROM public.places
                                    LEFT JOIN
                                        public.countries
                                    ON
                                        public.places.country = public.countries.id
                                GROUP BY public.countries.country;"""

total_places_by_country = pd.read_sql_query(quey_total_places_by_country, con=connection)

total_places = int(total_places_by_country["total"].sum())

#Places by property type--------------------------------------------------------------------------------------------

query_total_places_by_property_type ="""SELECT
                                    public.property_types.property_type as "Tipo de Propiedad",  COUNT(*) As Total
                                FROM public.places
                                    LEFT JOIN
                                        public.property_types
                                    ON
                                        public.places.property_type = public.property_types.id
                                GROUP BY public.property_types.property_type;"""

total_places_by_property_type = pd.read_sql_query(query_total_places_by_property_type, con=connection)

#property rating--------------------------------------------------------------------------------------------
quey_property_rating =  """SELECT public.places.stars as "Calificación", COUNT(*) As Total
                            FROM public.places
                            GROUP BY public.places.stars;"""

property_rating = pd.read_sql_query(quey_property_rating, con=connection)

#--------------------------------------------------------------------------------------------

#prueba = pd.read_sql_query(query_users, con=connection)


st.title(":bar_chart: Places visualization")
st.markdown("##")

column_1, column_2 = st.columns(2)

with column_1:
    st.subheader("Total Places: ")
    st.subheader(f"{total_places}")

with column_2:
    st.subheader("Places average by country: ")
    st.subheader(round(total_places_by_country['total'].mean(),2))

st.markdown("---")

column_graph_1, column_graph_2 = st.columns(2)

#Graph Places by country
fig_users_by_country = px.bar(
    total_places_by_country,
    x = "total",
    y = "país",
    orientation = "h",
    title = "<b>Total Places by country</b>",
    color_discrete_sequence = ["#0083B8"] * len(total_places_by_country),
    template = "plotly_white",
)

#Graph Places Type
fig_property_type = px.bar(
    total_places_by_property_type,
    x = "Tipo de Propiedad",
    y = "total",
    orientation = "v",
    title = "<b>Property Types</b>",
    color_discrete_sequence = ["#0083B8"] * len(total_places_by_property_type),
    template = "plotly_white",
)

fig_property_rating = go.Figure(data=go.Scatter(
    x=property_rating["Calificación"],
    y=property_rating["total"],
    mode='markers',
    marker=dict(size=[20, 40, 60, 80, 100],
                color=[0, 1, 2, 3, 4])
))

column_graph_1.plotly_chart(fig_users_by_country, use_container_width = True)
column_graph_2.plotly_chart(fig_property_type, use_container_width = True)
st.markdown("---")
st.subheader("Stars Number ")
st.plotly_chart(fig_property_rating, use_container_width = True)

import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st


#Global Constants
PSQL_HOST = "ec2-54-165-184-219.compute-1.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "xouugvjvpdqxzl"
PSQL_PASS = "0cfc12f2ea32b36baffa66379813f12ea2e1a18b65b01224249f90875ce63137"
PSQL_DB = "duminr7s43tjt"

#Connection
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
""" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
connection = psycopg2.connect(connection_address)

#Query
query_users = """SELECT
                public.users.first_name as "Primer Nombre",
                public.users.last_name as "Apellido",
                public.users.gender as "Genero",
                public.users.birth_day as "Cumpleaños",
                public.countries.country as "País",
                public.states.states as "Estado",
                public.property_types.property_type as "Propiedad Preferida"
            FROM public.users
                LEFT JOIN
                    public.countries
                ON
                    public.users.country = public.countries.id
                
                LEFT JOIN
                    public.states
                ON
                    public.users.states = public.states.id
                
                LEFT JOIN
                    public.property_types
                ON
                    public.users.property_preference = public.property_types.id
                
            ORDER BY public.users.id ASC LIMIT 100;"""

#Total Users----------------------------------------------------------------------------
quey_total_users_by_country ="""SELECT
                                    public.countries.country as País,  COUNT(*) As Total
                                FROM public.users
                                    LEFT JOIN
                                        public.countries
                                    ON
                                        public.users.country = public.countries.id
                                GROUP BY public.countries.country;"""

total_users_by_country = pd.read_sql_query(quey_total_users_by_country, con=connection)

total_users = int(total_users_by_country["total"].sum())

#Users by gender--------------------------------------------------------------------------------------------

query_total_users_by_gender ="""SELECT public.users.gender as Género, COUNT(*) As Total
                                FROM public.users
                                GROUP BY public.users.gender;"""

total_users_by_gender = pd.read_sql_query(query_total_users_by_gender, con=connection)

#Preference property--------------------------------------------------------------------------------------------
quey_property_preference ="""SELECT
                                public.property_types.property_type as "Propiedad Preferida",  COUNT(*) As Total
                            FROM public.users
                                LEFT JOIN
                                    public.property_types
                                ON
                                    public.users.property_preference = public.property_types.id
                            GROUP BY public.property_types.property_type;"""

property_preference = pd.read_sql_query(quey_property_preference, con=connection)

#User age range--------------------------------------------------------------------------------------------
quey_user_by_age_range ="""SELECT t.rango, COUNT(*) as Cantidad
                             FROM(
                                 SELECT CASE
                                     WHEN tabla.edad between 20 and 29 then '20 - 29'
                                     WHEN tabla.edad between 30 and 39 then '30 - 39'
                                     WHEN tabla.edad between 40 and 49 then '40 - 49'
                                     WHEN tabla.edad between 50 and 59 then '50 - 59'
                                     WHEN tabla.edad >= 60 then '> 60' end as rango
                                 FROM (
                                         SELECT ((CURRENT_DATE - public.users.birth_day)/365) as edad, COUNT(*)
                                         FROM public.users
                                         GROUP BY edad
                                 ) as tabla
                                 GROUP BY tabla.edad
                             ) as t
                             GROUP BY t.rango"""

user_by_age_range = pd.read_sql_query(quey_user_by_age_range, con=connection)

#--------------------------------------------------------------------------------------------
#prueba = pd.read_sql_query(query_users, con=connection)

# ---- MAINPAGE ----
st.title(":bar_chart: Users visualization")
st.markdown("##")

column_1, column_2 = st.columns(2)

with column_1:
    st.subheader("Total Users: ")
    st.subheader(f"{total_users}")

with column_2:
    st.subheader("Users average by country: ")
    st.subheader(round(total_users_by_country['total'].mean(),2))

st.markdown("---")

#Graph Users by country
fig_users_by_country = px.bar(
    total_users_by_country,
    x = "total",
    y = "país",
    orientation = "h",
    title = "<b>Total Users by country</b>",
    color_discrete_sequence = ["#0083B8"] * len(total_users_by_country),
    template = "plotly_white",
)

#Graph users by gender
fig_users_by_gender = px.bar(
    total_users_by_gender,
    x = "género",
    y = "total",
    orientation = "v",
    title = "<b>Total Users by gender</b>",
    color_discrete_sequence = ["#0083B8"] * len(total_users_by_country),
    template = "plotly_white",
)

#Graph property prefer
fig_property_prefer = px.pie(
    property_preference,
    values = "total",
    names = "Propiedad Preferida",
    title = "<b>Property prefer</b>",
)

st.plotly_chart(fig_users_by_country)
st.plotly_chart(fig_users_by_gender)
st.plotly_chart(fig_property_prefer)

#st.dataframe(prueba)

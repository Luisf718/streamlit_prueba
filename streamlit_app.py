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

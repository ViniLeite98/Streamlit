import streamlit as st
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Título do Dashboard
st.title('DASHBOARD DE VENDAS 🛒')

# Caixa de Texto
texto = st.text_area("Digite alguma informação")

# Exibindo o texto
st.write("Você digitou:", texto)

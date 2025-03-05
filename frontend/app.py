# frontend/app.py
import streamlit as st

st.set_page_config(
    page_title="Dashboard Principal",
    page_icon="📊",
    layout="centered", 
)

st.title("📊 App A3DATA Insights")

st.markdown("""
Bem-vindo(a) ao **App A3DATA Insights**, um aplicativo desenvolvido para facilitar a análise de dados de livros e avaliações.

---

### O que você pode fazer por aqui?
            
1. **Análise Exploratória dos Dados**  
   - Faça a Análise Exploratória dos Dados, e em `minutos` você terá os insights.

2. **Upload de CSV**  
   - Faça o upload dos arquivos contendo dados de livros ou avaliações.

3. **Chatbot**  
   - Interaja com o nosso agente de perguntas e respostas.

---

Para navegar, utilize o **menu lateral** à esquerda, onde você encontra as diferentes páginas do aplicativo.
""")


st.info("Dúvidas? Entre em contato com o suporte.")

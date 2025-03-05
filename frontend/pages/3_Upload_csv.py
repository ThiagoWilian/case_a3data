# frontend/pages/upload_csv.py
from core.settings import settings
import streamlit as st
import requests
import time 

st.title("📤 Upload de Arquivos CSV")

# Upload do books_data.csv
st.subheader("books_data.csv")
st.warning("Envio de arquivos CSV está desabilitado no momento, para evitar sobrecarga do servidor.")

books_data_file = st.file_uploader(
    "Arraste e solte o arquivo books_data.csv",
    type=["csv"],
    key="books_data",
    disabled=True # Desabilitado para evitar sobrecarga do servidor
)

if books_data_file is not None:
    st.info("Envio de books_data.csv está desabilitado no momento.")
    if st.button("Enviar books_data.csv", disabled=True): # Desabilitado para evitar sobrecarga do servidor
        st.toast("Enviando books_data.csv...")
        files = {
            "file": (books_data_file.name, books_data_file.getvalue(), "text/csv")
        }
        start_transfer = time.time()
        response = requests.post(f"{settings.API_URL}/process_books_data", files=files)
        end_transfer = time.time()
        transfer_time = end_transfer - start_transfer
        
        if response.ok:
            st.success("books_data.csv foi processado com sucesso!")
            resultado = response.json()
            st.success(f"Tempo de transferência: {transfer_time:.2f} segundos")
            st.success(f"Tempo de processamento (servidor): {resultado['tempo_processamento']:.2f} segundos")
            st.info(f"Total de registros no csv books_data.csv: {resultado['books_data_rows']}")
        else:
            st.error("Erro ao processar books_data.csv.")

# Upload do books_rating.csv
st.subheader("books_rating.csv")
books_rating_file = st.file_uploader(
    "Arraste e solte o arquivo books_rating.csv",
    type=["csv"],
    key="books_rating",
    disabled=True # Desabilitado para evitar sobrecarga do servidor
)

if books_rating_file is not None:
    st.info("Envio de books_rating.csv está desabilitado no momento.")
    if st.button("Enviar books_rating.csv", disabled=True):
        st.toast("Enviando books_rating.csv...")
        files = {
            "file": (books_rating_file.name, books_rating_file.getvalue(), "text/csv")
        }
        start_transfer = time.time()
        response = requests.post(f"{settings.API_URL}/process_books_rating", files=files)
        end_transfer = time.time()
        transfer_time = end_transfer - start_transfer

        if response.ok:
            st.success("books_rating.csv foi processado com sucesso!")
            resultado = response.json()
            st.success(f"Tempo de transferência: {transfer_time:.2f} segundos")
            st.success(f"Tempo de processamento (servidor): {resultado['tempo_processamento']:.2f} segundos")
            st.info(f"Total de registros no csv books_rating.csv: {resultado['books_rating_rows']}")
        else:
            st.error("Erro ao processar books_rating.csv.")

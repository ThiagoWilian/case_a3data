from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io, os
from time import time

router = APIRouter()


@router.post("/process_books_data")
async def process_books_data(file: UploadFile = File(...)):
    # Lê o conteúdo do arquivo books_data
    start_time_data = time()
    data_content = await file.read()
    df_data = pd.read_csv(io.StringIO(data_content.decode("utf-8")))
    rows_data = len(df_data)
    print(f"books_data: {rows_data} registros")
    end_time_data = time()
    tempo_processamento_data = end_time_data - start_time_data
    print(f"Tempo de execução: {tempo_processamento_data} segundos")
    
    return {
        "message": "books_data.csv processado com sucesso!",
        "books_data_rows": rows_data,
        "tempo_processamento": tempo_processamento_data,
        "tempo_final_data": end_time_data
    }


@router.post("/process_books_rating")
async def process_books_rating(file: UploadFile = File(...)):
    # Lê o conteúdo do arquivo books_rating
    start_time_rating = time()
    rating_content = await file.read()
    df_rating = pd.read_csv(io.StringIO(rating_content.decode("utf-8")))
    rows_rating = len(df_rating)
    print(f"books_rating: {rows_rating} registros")
    end_time_rating = time()
    tempo_processamento_rating = end_time_rating - start_time_rating
    print(f"Tempo de execução: {tempo_processamento_rating} segundos")
    
    return {
        "message": "books_rating.csv processado com sucesso!",
        "books_rating_rows": rows_rating,
        "tempo_processamento": tempo_processamento_rating,
        "tempo_final_rating": end_time_rating
    }



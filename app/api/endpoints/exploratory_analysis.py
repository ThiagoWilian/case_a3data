from app.utils.utils import limpar_lista
from fastapi import APIRouter
import pandas as pd
import io, os
from time import time

router = APIRouter()



@router.get("/exploratory_analysis")
def exploratory_analysis():

    start_time_analysis = time()
    # Carrega o dataset final (merged)
    path_merged = os.path.join("app", "data", "books_final_merged_tratado.csv")
    df_merged = pd.read_csv(path_merged)

    # Remove duplicatas
    df_merged = df_merged.drop_duplicates(subset=['Id', 'User_id'])

    ## 1 - ANÁLISE DE NOTAS
    # Distribuição percentual de cada pontuação
    score_percent_series = df_merged['score'].value_counts(normalize=True).sort_index() * 100
    score_percent_dict = score_percent_series.to_dict()

    # Contagem exata de cada score (para plot de barras)
    score_counts_series = df_merged['score'].value_counts().sort_index()
    score_counts_dict = score_counts_series.to_dict()

    
    
    ## 2 - ANÁLISE DE LIVROS
    # Top 10 livros com mais avaliações
    top_books_count_series = (
        df_merged.groupby("Title")["Id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )
    top_books_count_dict = top_books_count_series.to_dict()

    ## 2 - ANÁLISE DE LIVROS
    # Top 10 livros com melhor avaliação média (mínimo de X avaliações)
    minimo_avaliacoes = 1000
    avg_score_books = (
        df_merged.groupby("Title")["score"]
        .mean()
        .sort_values(ascending=False)
    )

    # Filtra usando uma máscara booleana para manter a ordem correta
    counts = df_merged.groupby("Title")["Id"].count()
    mask = counts > minimo_avaliacoes
    avg_score_books_filtered = avg_score_books[mask].head(10).to_dict()

    ## 3 - ANÁLISE DE AUTORES
    # Top 10 autores com mais avaliações
    df_merged_exploded = df_merged.explode("authors")

    # Filtra autores 'Not informed'
    df_valid_authors = df_merged_exploded[df_merged_exploded["authors"] != "['Not informed']"]

    top_authors_series = (
        df_valid_authors.groupby("authors")["Id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )
    top_authors_dict = {limpar_lista(author): val for author, val in top_authors_series.items()}

    # Mantém autores 'Not informed'
    top_authors_with_not_informed = (
        df_merged_exploded.groupby("authors")["Id"]
        .count()
        .sort_values(ascending=False)
        .head(11))
    top_authors_with_not_informed_dict = {limpar_lista(author): val for author, val in top_authors_with_not_informed.items()}

    # Top Autores por Avaliação Média
    avg_score_authors = (
        df_valid_authors.groupby("authors")["score"]
        .mean()
        .sort_values(ascending=False)
    )

    # Filtrando autores com pelo menos X avaliações para evitar outliers
    counts_by_author = df_valid_authors.groupby("authors")["Id"].count()
    authors_with_min_reviews = counts_by_author[counts_by_author > minimo_avaliacoes].index

    avg_score_authors_filtered = avg_score_authors.loc[authors_with_min_reviews].head(10)
    top_authors_avg_score_dict = {limpar_lista(author): val for author, val in avg_score_authors_filtered.items()}



    ## 4 - ANÁLISE DE GÊNEROS
    df_merged_exploded_cat = df_merged.explode("categories")

    # Análise com todas as categorias (incluindo 'Not informed')
    top_categories_with_not_informed = (
        df_merged_exploded_cat
        .groupby("categories")["Id"]
        .count()
        .sort_values(ascending=False)
        .head(11)  # Peguei 11 pois conto que 'Not informed' aparecerá
    )
    top_categories_with_not_informed_dict = {limpar_lista(cat): val for cat, val in top_categories_with_not_informed.items()}
    
    
    # Cálculo da média de avaliação por categoria
    df_valid_categories = df_merged_exploded_cat[df_merged_exploded_cat["categories"] != "['Not informed']"]

    avg_score_categories = (
        df_valid_categories.groupby("categories")["score"]
        .mean()
        .sort_values(ascending=False)
    )

    counts_by_category = df_valid_categories.groupby("categories")["Id"].count()
    categories_with_min_reviews = counts_by_category[counts_by_category > minimo_avaliacoes].index

    avg_score_categories_filtered = avg_score_categories.loc[categories_with_min_reviews].head(10)
    top_categories_avg_score_dict = {limpar_lista(cat): val for cat, val in avg_score_categories_filtered.items()}


    ## 5 - ANÁLISE DE USUÁRIOS
    # Top 10 usuários com mais reviews
    user_reviews_count_series = df_merged.groupby("User_id")["Id"].count().sort_values(ascending=False).head(10)
    user_profile_map = df_merged[['User_id', 'profileName']].drop_duplicates(subset=['User_id']).set_index('User_id')['profileName'].to_dict()

    top_users_list = []
    for user_id, count_val in user_reviews_count_series.items():
        name = user_profile_map.get(user_id, user_id)
        top_users_list.append({
            "User_id": user_id,
            "profileName": str(name),
            "count_reviews": int(count_val)
        })

    # TOP 10 usuários (RELEVÂNCIA)
    df_merged["text_length"] = df_merged["text_concat"].apply(lambda x: len(str(x)))

    user_stats = df_merged.groupby("User_id").agg(
        num_reviews=("Id", "count"),
        mean_score=("score", "mean"),
        std_score=("score", "std")
    ).reset_index()

    text_stats = df_merged.groupby("User_id")["text_length"].mean().reset_index(name="mean_text_length")
    user_stats = pd.merge(user_stats, text_stats, on="User_id", how="left")

    user_stats["std_score"] = user_stats["std_score"].fillna(0)

    # Parâmetros para relevance_score
    min_reviews_required = 100
    peso_reviews = 0.4
    peso_text_length = 0.4
    peso_std_score = 0.2

    user_stats["relevance_score"] = (
        (user_stats["num_reviews"] / user_stats["num_reviews"].max()) * peso_reviews
      + (user_stats["mean_text_length"] / user_stats["mean_text_length"].max()) * peso_text_length
      + (user_stats["std_score"] / user_stats["std_score"].max()) * peso_std_score
    )

    user_stats = user_stats[user_stats["num_reviews"] >= min_reviews_required].copy()
    
    # Calcula os valores máximos APÓS o filtro
    max_num_reviews = user_stats['num_reviews'].max()
    max_mean_text_length = user_stats['mean_text_length'].max()
    max_std_score = user_stats['std_score'].max()

    user_stats.sort_values("relevance_score", ascending=False, inplace=True)
    user_stats["profileName"] = user_stats["User_id"].map(user_profile_map)

    top_relevant_users = user_stats.head(10).copy()
    top_relevant_users['num_reviews_component'] = (top_relevant_users['num_reviews'] / max_num_reviews) * peso_reviews
    top_relevant_users['text_length_component'] = (top_relevant_users['mean_text_length'] / max_mean_text_length) * peso_text_length
    top_relevant_users['std_score_component'] = (top_relevant_users['std_score'] / max_std_score * peso_std_score).fillna(0)
    top_relevant_users_dict = top_relevant_users.to_dict(orient="records")
    

    end_time_analysis = time()
    tempo_processamento_analysis = end_time_analysis - start_time_analysis


    result = {
        "score_percent": score_percent_dict,        
        "score_counts": score_counts_dict,          
        "top_books_count": top_books_count_dict,    
        "avg_score_books_filtered": avg_score_books_filtered,  
        "top_authors": top_authors_dict,            
        "top_authors_with_not_informed": top_authors_with_not_informed_dict,
        "top_authors_avg_score": top_authors_avg_score_dict,
        "top_categories_with_not_informed": top_categories_with_not_informed_dict,      
        "top_categories_avg_score": top_categories_avg_score_dict,
        "top_users": top_users_list,                
        "top_relevant_users": top_relevant_users_dict,
        "tempo_execucao": tempo_processamento_analysis
    }
    
    return result
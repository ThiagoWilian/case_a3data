# frontend/pages/1_Exploration_Analysis.py
from core.settings import settings
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🔎 Exploratory Analysis - Insights")

st.write("""
Faça a `Análise Exploratória dos Dados`, e em `minutos` você terá os insights.
Tenha insights sobre **Distribuição de Notas**, **Top 10 Livros com Mais Avaliações**, **Top 10 Livros com Melhor Avaliação Média**, **Top Autores**, **Top Categorias**, **Top Usuários (Quantidade)** e **Top Usuários (Relevância)**.
Clique no botão abaixo para gerar os gráficos.
""")

if st.button("Executar Análises"):
    with st.spinner("Carregando dados e gerando insights..."):
        resp = requests.get(f"{settings.API_URL}/exploratory_analysis")
        if resp.ok:
            data = resp.json()
            st.success("Análises concluídas com sucesso!")

            if "tempo_execucao" in data:
                st.info(f"⏱️ Tempo para gerar análises: {data['tempo_execucao']:.2f} segundos")


            # Abas
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Distribuição de Notas",
                "Performance dos Livros",
                "Performance dos Autores",
                "Performance das Categorias",
                "Top Usuários",
                "Análise de sentimento (em desenvolvimento)"
            ])

            # Distribuição de Notas
            with tab1:
                st.subheader("Distribuição do Score")

                subtab1, subtab2 = st.tabs([
                    "Distribuição Exata",
                    "Distribuição Percentual"
                ])

                with subtab1:
                    if "score_counts" in data:
                        
                        score_colors = ['#FF5A5A', '#FFA55A', '#FFFF5A', '#5AFF5A', '#5AAFFF']
                        score_colors_dict = {
                            '1.0': score_colors[0],
                            '2.0': score_colors[1],
                            '3.0': score_colors[2],
                            '4.0': score_colors[3],
                            '5.0': score_colors[4]
                        }
                        
                        scores = sorted(data['score_counts'].keys())
                        counts = [data['score_counts'][k] for k in scores]
                        cores = [score_colors_dict[k] for k in scores]

                        plt.figure(figsize=(8, 5))
                        ax = sns.barplot(x=scores, y=counts, hue=scores, palette=cores, legend=False)
                        
                        for i, v in enumerate(counts):
                            ax.text(i, v + 0.1*v, f'{v:,}', ha='center', fontsize=10)
                        
                        plt.title('Distribuição das Pontuações', fontsize=14, fontweight='bold')
                        plt.xlabel('Pontuação', fontsize=12)
                        plt.ylabel('Frequência de notas', fontsize=12)
                        plt.xticks([0, 1, 2, 3, 4], ['1', '2', '3', '4', '5'])
                        plt.grid(True, axis='y', linestyle='--', alpha=0.4)
                        
                        y_max = max(counts) * 1.15
                        plt.ylim(0, y_max)
                        
                        plt.tight_layout()
                        st.pyplot(plt)

                with subtab2:
                    if "score_percent" in data:
                        st.write("**Percentual das Pontuações:**")
                        score_percent = data["score_percent"]
                        df_score_percent = pd.DataFrame(
                            list(score_percent.items()), columns=["score", "percent"]
                        )

                        score_colors = ['#FF5A5A', '#FFA55A', '#FFFF5A', '#5AFF5A', '#5AAFFF']
                        
                        plt.figure(figsize=(8, 8))
                        explode = (0, 0, 0, 0, 0.1)  # Destaca a fatia de 5 estrelas
                        wedges, texts, autotexts = plt.pie(
                            df_score_percent["percent"],
                            labels=df_score_percent["score"],
                            colors=score_colors,
                            autopct='%1.1f%%',
                            startangle=90,
                            explode=explode,
                            shadow=True,
                            textprops={'fontsize': 12, 'color': 'black', 'weight': 'bold'},
                            wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
                        )

                        for autotext in autotexts:
                            autotext.set_size(12)
                            autotext.set_color('white')
                            autotext.set_bbox(dict(facecolor='black', alpha=0.7, edgecolor='none'))

                        plt.title(
                            "Distribuição Percentual das Avaliações\n", 
                            fontsize=16, 
                            fontweight='bold', 
                            pad=20
                        )

                        plt.legend(
                            wedges,
                            [f'Nota {score} ({percent:.2f}%)' for score, percent in zip(df_score_percent["score"], df_score_percent["percent"])],
                            title="Legenda:",
                            loc="center left",
                            bbox_to_anchor=(1, 0, 0.5, 1),
                            fontsize=10
                        )

                        plt.tight_layout()
                        st.pyplot(plt)

            # Performance dos Livros
            with tab2:
                st.subheader("Performance dos Livros")

                subtab1, subtab2 = st.tabs([
                    "Top 10 Livros com Maior Quantidade de Avaliações",
                    "Top 10 Livros com Melhor Avaliação Média"
                ])

                with subtab1:

                    if "top_books_count" in data:
                        top_books_count = data["top_books_count"]
                        
                        df_top_books = pd.DataFrame(
                            list(top_books_count.items()), 
                            columns=["Title", "count"]
                        )
                        
                        df_top_books["Title_short"] = df_top_books["Title"].apply(
                            lambda x: x[:30] + '...' if len(x) > 30 else x
                        )

                        plt.figure(figsize=(12, 6))
                        ax = sns.barplot(
                            x="count", 
                            y="Title_short", 
                            data=df_top_books,
                            hue="Title_short",
                            palette="viridis",
                            legend=False
                        )

                        for i, v in enumerate(df_top_books["count"]):
                            ax.text(v + v*0.01, i, f' {v:,}', va='center', fontsize=10)

                        plt.title('Top 10 Livros com Maior Quantidade de Avaliações', 
                                fontsize=16, fontweight='bold')
                        plt.xlabel('Quantidade de Avaliações', fontsize=12)
                        plt.ylabel('Título do Livro', fontsize=12)
                        plt.grid(True, axis='x', linestyle='--', alpha=0.7)
                        plt.xlim(0, df_top_books["count"].max() * 1.1)
                        
                        st.pyplot(plt)

                with subtab2:
                    if "avg_score_books_filtered" in data:
                        minimo_avaliacoes = 1000

                    avg_series = pd.Series(data["avg_score_books_filtered"]).sort_values(ascending=False)

                    df_avg = pd.DataFrame({
                        'Title': avg_series.index,
                        'Score': avg_series.values
                    })

                    df_avg['Title_short'] = df_avg['Title'].apply(
                        lambda x: (x[:30] + '...') if len(x) > 30 else x
                    )

                    plt.figure(figsize=(12, 6))
                    ax = sns.barplot(
                        x='Score', 
                        y='Title_short',
                        data=df_avg,
                        hue='Title_short',  
                        palette='coolwarm',  
                        dodge=False,
                        legend=False  
                    )

                    for i, v in enumerate(df_avg['Score']):
                        ax.text(v + 0.01, i, f' {v:.2f}', va='center', fontsize=12)

                    plt.xticks(fontsize=12)
                    plt.yticks(fontsize=12)
                    plt.xlabel('Pontuação Média', fontsize=14)
                    plt.ylabel('Título do Livro', fontsize=14)
                    plt.title(f'Top 10 Livros com Melhor Avaliação Média (mínimo {minimo_avaliacoes} avaliações)', fontsize=16, fontweight='bold')
                    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
                    plt.xlim(4.5, 5.05)  
                    plt.tight_layout()  

                    st.pyplot(plt)
            
            # Performance dos Autores
            with tab3:
                st.subheader("Top Autores por Número de Avaliações")
                
                subtab1, subtab2 = st.tabs([
                    "Excluindo 'Not Informed'",
                    "Incluindo 'Not Informed'"
                ])
                
                # Gráfico 1: Excluindo 'Not Informed'
                with subtab1:
                    if "top_authors" in data:
                        df = pd.DataFrame(
                            list(data["top_authors"].items()),
                            columns=["Autor", "Avaliações"]
                        )
                        
                        plt.figure(figsize=(12,6))
                        
                        # Plot das barras VERTICAIS
                        bars = plt.bar(
                            range(len(df)),
                            df["Avaliações"],
                            color='#3498db',  # Azul 
                            width=0.7
                        )
                        
                        for i, v in enumerate(df["Avaliações"]):
                            plt.text(
                                i,  
                                v + 0.03*max(df["Avaliações"]),  
                                f'{v:,}',
                                ha='center',
                                va='bottom',
                                fontsize=10,
                                fontweight='bold'
                            )
                        
                        plt.title("Top 10 Autores por número de avaliações (Excluindo 'Not Informed')", fontsize=16, fontweight='bold')
                        plt.ylabel("Quantidade de Avaliações", fontsize=12)
                        plt.xlabel("Autor", fontsize=12)
                        plt.xticks(range(len(df)), df["Autor"], rotation=45, ha="right")
                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                        plt.ylim(0, max(df["Avaliações"]) * 1.1)
                        plt.tight_layout()
                        
                        st.pyplot(plt)
                
                # Gráfico 2: Incluindo 'Not Informed'
                with subtab2:
                    if "top_authors_with_not_informed" in data:
                        df = pd.DataFrame(
                            list(data["top_authors_with_not_informed"].items()),
                            columns=["Autor", "Avaliações"]
                        )
                        
                        plt.figure(figsize=(12,6))
                        
                        colors = []
                        for autor in df["Autor"]:
                            if autor == "Not informed":
                                colors.append('#FF6666')  # Vermelho
                            else:
                                colors.append('#3498db')  # Azul
                        
                        bars = plt.bar(
                            range(len(df)),
                            df["Avaliações"],
                            color=colors,
                            width=0.7
                        )
                        
                        for i, v in enumerate(df["Avaliações"]):
                            plt.text(
                                i,  
                                v + 0.03*max(df["Avaliações"]),  
                                f'{v:,}',
                                ha='center',
                                va='bottom',
                                fontsize=10,
                                fontweight='bold'
                            )
                        
                        from matplotlib.patches import Patch
                        legend_elements = [
                            Patch(facecolor='#FF6666', label='Autores não avaliados'),
                            Patch(facecolor='#3498db', label='Autores avaliados')
                        ]
                        plt.legend(
                            handles=legend_elements,
                            loc='upper right',
                            frameon=True,
                            framealpha=0.9
                        )
                        
                        plt.title("Top Autores por número de avaliações (Incluindo 'Not Informed')", fontsize=16, fontweight='bold')
                        plt.ylabel("Quantidade de Avaliações", fontsize=12)
                        plt.xlabel("Autor", fontsize=12)
                        plt.xticks(range(len(df)), df["Autor"], rotation=45, ha="right")
                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                        plt.ylim(0, max(df["Avaliações"]) * 1.1)
                        plt.tight_layout()
                        
                        st.pyplot(plt)


                st.subheader("Top 10 Autores por avaliação média (mínimo 1000 avaliações)")
                if "top_authors_avg_score" in data:
                    df = pd.DataFrame(
                        list(data["top_authors_avg_score"].items()),
                        columns=["Autor", "Avaliação Média"]
                    ).sort_values("Avaliação Média", ascending=False)
                    
                    plt.figure(figsize=(12, 6))
                    
                    # barplot horizontal
                    ax = sns.barplot(
                        x=df["Avaliação Média"],
                        y=df["Autor"],
                        hue=df["Autor"],
                        palette="Oranges_r",
                        legend=False
                    )
                    
                    for i, v in enumerate(df["Avaliação Média"]):
                        ax.text(v + 0.01, i, f" {v:.2f}", va="center")
                    
                    plt.title(f"Top 10 Autores com Melhor Avaliação Média (mínimo 1000 avaliações)", 
                              fontsize=16, fontweight="bold")
                    plt.xlabel("Pontuação Média", fontsize=12)
                    plt.ylabel("Autor", fontsize=12)
                    plt.grid(True, axis="x", linestyle="--", alpha=0.7)
                    
                    plt.xlim(min(df["Avaliação Média"]) - 0.1, max(df["Avaliação Média"]) + 0.1)
                    
                    plt.tight_layout()
                    st.pyplot(plt)
                else:
                    st.info("Dados de avaliação média de autores não disponíveis.")

            # Performance das Categorias
            with tab4:
                subtab1, subtab2 = st.tabs([
                    "Top Categorias/Gêneros Mais Avaliados",
                    "Top Generos/categoria por Avaliação Média"
                ])

                with subtab1:
                    st.subheader("Top Categorias/Gêneros Mais Avaliados")
                
                    if "top_categories_with_not_informed" in data:
                        df = pd.DataFrame(
                            list(data["top_categories_with_not_informed"].items()),
                            columns=["Categoria", "Avaliações"]
                        )
                        
                        df = df.sort_values("Avaliações", ascending=True)  # Ordem crescente para barh
                        
                        colors = []
                        for cat in df["Categoria"]:
                            if cat.strip().lower() == "not informed":  
                                colors.append('#FF6666')  # Vermelho
                            else:
                                colors.append('#3498db')  # Azul
                        
                        plt.figure(figsize=(12, 6))
                        
                        # barras horizontais
                        bars = plt.barh(
                            df["Categoria"],
                            df["Avaliações"],
                            color=colors
                        )
                        
                        max_val = df["Avaliações"].max()
                        for i, (cat, val) in enumerate(zip(df["Categoria"], df["Avaliações"])):
                            plt.text(
                                val + 0.01 * max_val, 
                                i,
                                f"{val:,}",
                                ha="left",
                                va="center",
                                fontsize=10
                            )
                        
                        from matplotlib.patches import Patch
                        legend_elements = [
                            Patch(facecolor='#FF6666', label='Categoria não informada'),
                            Patch(facecolor='#3498db', label='Categorias identificadas')
                        ]
                        plt.legend(
                            handles=legend_elements,
                            loc='lower right',
                            frameon=True,
                            framealpha=0.9
                        )
                        
                        plt.title("Top Categorias/Gêneros Mais Avaliados", fontsize=16, fontweight="bold")
                        plt.xlabel("Quantidade de Avaliações", fontsize=12)
                        plt.ylabel("Categoria/Gênero", fontsize=12)
                        plt.grid(True, axis="x", linestyle="--", alpha=0.7)
                        plt.xlim(0, max_val * 1.1)
                        plt.tight_layout()
                        
                        st.pyplot(plt)

                with subtab2:
                    st.subheader("Top Generos/categoria por Avaliação Média")
                    
                    if "top_categories_avg_score" in data:

                        df = pd.DataFrame(
                            list(data["top_categories_avg_score"].items()),
                            columns=["Categoria", "Pontuação Média"]
                        ).sort_values("Pontuação Média", ascending=False)
                        
                        plt.figure(figsize=(12, 6))
                        
                        ax = sns.barplot(
                            x="Pontuação Média",
                            y="Categoria",
                            data=df,
                            hue="Categoria",
                            palette="viridis",
                            legend=False
                        )
                        
                        max_val = df["Pontuação Média"].max()
                        for i, (cat, score) in enumerate(zip(df["Categoria"], df["Pontuação Média"])):
                            ax.text(
                                score + 0.01, 
                                i,
                                f"{score:.2f}",
                                va="center",
                                fontsize=10
                            )
                        
                        plt.title(f"Top Categorias por Avaliação Média (mínimo 1000 avaliações)", 
                                fontsize=16, fontweight="bold")
                        plt.xlabel("Pontuação Média", fontsize=12)
                        plt.ylabel("Categoria", fontsize=12)
                        plt.grid(True, axis="x", linestyle="--", alpha=0.7)
                        plt.xlim(
                            max(0, df["Pontuação Média"].min() - 0.1),  
                            df["Pontuação Média"].max() + 0.1
                        )
                        plt.tight_layout()
                        
                        st.pyplot(plt)
                    else:
                        st.info("Dados de avaliação média por categoria não disponíveis.")


            # Top Usuários
            with tab5:

                subtab1, subtab2 = st.tabs([
                    "Top 10 Usuários (Quantidade de Avaliações)",
                    "Top 10 Usuários (Relevância)"
                ])

                with subtab1:
                    st.subheader("Top 10 Usuários (Quantidade de Avaliações)")
                    if "top_users" in data:
                        top_users = data["top_users"]
                        
                        profile_names = [user["profileName"] for user in top_users]
                        counts = [user["count_reviews"] for user in top_users]
                        
                        profile_names_short = [name[:20] + '...' if len(name) > 20 else name for name in profile_names]
                        
                        plt.figure(figsize=(12, 6))
                        
                        ax = sns.barplot(
                            x=range(len(top_users)),
                            y=counts,
                            hue=range(len(top_users)),
                            palette="Blues_d",
                            legend=False
                        )
                        
                        max_count = max(counts)
                        for i, v in enumerate(counts):
                            ax.text(
                                i, 
                                v + max_count * 0.01,  # Posiciona acima da barra
                                f"{v:,}",
                                ha="center",
                                fontsize=10,
                                fontweight="bold"
                            )
                        
                        plt.xticks(
                            range(len(top_users)),
                            profile_names_short,
                            rotation=45,
                            ha="right"
                        )
                        plt.title("Top 10 Usuários com Mais Avaliações", fontsize=16, fontweight="bold")
                        plt.xlabel("Nome do Usuário", fontsize=12)
                        plt.ylabel("Quantidade de Avaliações", fontsize=12)
                        plt.ylim(0, max(counts) * 1.1)
                        plt.grid(axis="y", linestyle="--", alpha=0.7)
                        plt.tight_layout()
                        
                        st.pyplot(plt)

                with subtab2:
                    st.subheader("Top 10 Usuários (Relevância)")
                    if "top_relevant_users" in data:
                        df_rel = pd.DataFrame(data["top_relevant_users"])
                        
                        df_rel['display_name'] = df_rel['profileName'].apply(
                            lambda x: str(x)[:15] + '...' if len(str(x)) > 15 else str(x)
                        )
                        
                        df_rel = df_rel.sort_values('relevance_score', ascending=False)
                        
                        plt.figure(figsize=(12, 6))
                        
                        # Cria as barras stackeds
                        bar1 = plt.barh(df_rel['display_name'], 
                                    df_rel['num_reviews_component'], 
                                    color='#3498db', 
                                    alpha=0.8)
                        
                        bar2 = plt.barh(df_rel['display_name'], 
                                    df_rel['text_length_component'],
                                    left=df_rel['num_reviews_component'],
                                    color='#2ecc71',
                                    alpha=0.8)
                        
                        bar3 = plt.barh(df_rel['display_name'], 
                                    df_rel['std_score_component'],
                                    left=df_rel['num_reviews_component'] + df_rel['text_length_component'],
                                    color='#e74c3c',
                                    alpha=0.8)
                        
                        for i, score in enumerate(df_rel['relevance_score']):
                            plt.text(score + 0.01, i, f'{score:.2f}', 
                                    va='center', 
                                    fontweight='bold')
                        
                        plt.xlabel('Score de Relevância', fontsize=12)
                        plt.ylabel('Usuário', fontsize=12)
                        plt.title('Top 10 Usuários por Score de Relevância', 
                                fontsize=16, 
                                fontweight='bold')
                        
                        plt.legend([bar1, bar2, bar3],
                                ['Quantidade de Reviews (40%)', 
                                'Tamanho dos Textos (40%)', 
                                'Variação nas Notas (20%)'],
                                loc='lower right')
                        
                        plt.grid(axis='x', linestyle='--', alpha=0.3)
                        plt.gca().invert_yaxis()
                        plt.tight_layout()
                        
                        st.pyplot(plt)
                                    

            with tab6:
                st.subheader("Análise de sentimento")
                st.info("Em processo de desenvolvimento...")
        else:
            st.error(f"Falha na requisição: {resp.status_code} - {resp.text}")

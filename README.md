# Case A3Data - Sistema de Análise de Dados de Livros

Bem-vindo(a) ao **Case A3Data**, um projeto desenvolvido para **explorar** e **analisar** avaliações de livros de maneira ágil e automatizada. A solução conta com um **frontend** em **Streamlit** e um **backend** em **FastAPI**, ambos **dockerizados** para facilitar a implantação e a escalabilidade.

---

## 1. Sobre o Projeto

Este sistema foi criado para **automatizar** o processo de análise de dados que, antes, levava até 3 dias e envolvia 5 analistas, gerando um custo de cerca de R$5.000 por ciclo de análise. Com a ferramenta, é possível:

- **Economizar tempo e custo** (de dias para poucas horas).
- **Visualizar** informações importantes sobre livros, autores, gêneros e usuários.
- **Carregar** dados próprios (CSV) e obter **insights** rapidamente.

---

## 2. Funcionalidades Principais

1. **Análise Exploratória**
   - Distribuição de notas (1 a 5).
   - Top 10 livros com mais avaliações.
   - Top 10 livros com melhor média de avaliação.
   - Top autores por número de avaliações.
   - Categorias/Gêneros mais populares e melhor avaliados.
   - Usuários mais ativos e usuários “especialistas” (score de relevância).

2. **Upload de Arquivos CSV**
   - Processamento dos arquivos `books_data.csv` e `books_rating.csv`.
   - Flexibilidade para inserir outros CSVs compatíveis.

3. **AI Agent SQL (Q&A)**
   - Interaja com um agente de perguntas e respostas sobre os dados (em desenvolvimento).

4. **Análise de Sentimento (Em Desenvolvimento)**
   - Uso de modelos de NLP (Transformers) para detectar sentimento nos comentários.

---

## 3. Tecnologias Utilizadas

### **Backend**
- **Python 3.12**
- **FastAPI** para criação de API.
- **Pandas** para manipulação de dados.
- **Transformers** (Hugging Face) para análises de NLP.
- **Docker** para containerização.

### **Frontend**
- **Streamlit** para criação de dashboards e interface web.
- **Matplotlib** e **Seaborn** para visualizações.
- **Requests** para comunicação com a API.

### **Outras Dependências**
- **AST** e bibliotecas auxiliares para tratamento de dados.
- **Docker Compose** para orquestrar múltiplos serviços.


---

## 4. Como Executar

Antes de iniciar o sistema, é **necessário processar** os seguintes arquivos CSV:
- `books_data.csv`: contém informações sobre os livros (título, autor, gênero, etc.).
- `books_rating.csv`: contém as avaliações dos usuários para os livros.

Estes arquivos devem ser processados através da funcionalidade de upload no frontend **antes de utilizar as análises**. Sem este processamento inicial, o sistema não terá dados para analisar.


### 4.1 Usando Docker (Recomendado)

1. **Clone** este repositório:
   ```bash
   git clone https://github.com/ThiagoWilian/case_a3data.git
   cd case_a3data
   ```
2. **Execute** com Docker Compose:
   ```bash
   docker compose up --build
   ```
3. **Acesse** as aplicações:
   - **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
   - **API (FastAPI):** [http://localhost:3000/docs](http://localhost:3000/docs) (documentação automática)

### 4.2 Execução Local (Sem Docker)

1. **Instale** as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. **Inicie o backend** (FastAPI):
   ```bash
   uvicorn app.main:app --reload --port 3000
   ```
3. **Inicie o frontend** (Streamlit):
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

---

## 5. Exemplos de Análises

- **Distribuição das notas:** veja quantos reviews são 1, 2, 3, 4 e 5.
- **Livros mais populares:** descubra quais títulos têm mais avaliações.
- **Melhores livros:** identifique os livros com melhor pontuação média.
- **Top Autores:** veja quem recebe mais reviews e quem tem as melhores notas.

---

## 6. Em Desenvolvimento

- **Análise de Sentimento** dos comentários usando Transformers/LLM.
- **Classificação de Tópicos** (topic modeling) para agrupar opiniões similares.

---

## 7. Autor

Desenvolvido por **Thiago Wilian**  
Para mais informações, entre em contato via [LinkedIn](https://www.linkedin.com/in/thiago-wilian/).

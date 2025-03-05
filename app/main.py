#app/main.py
from fastapi import FastAPI
from app.api.routes import routers as api_routers


app = FastAPI(
    title='A3DATA Book Analysis',
    docs_url='/docs',
    redoc_url='/redoc',
)


@app.get('/', include_in_schema=False)
def get_root():
    return {'message': 'A3DATA Book Analysis is working!'}


app.include_router(api_routers)
# uvicorn app.main:app --reload --port 3000
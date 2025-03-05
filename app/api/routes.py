#app/api/routes.py
from fastapi import APIRouter
import sys
from pathlib import Path
import os

# Adiciona o diretório pai ao sys.path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[2]
sys.path.append(str(root))

from app.api.endpoints.agent_sql import router as agent_sql_router
from app.api.endpoints.exploratory_analysis import router as exploratory_analysis_router
from app.api.endpoints.process_csv import router as process_csv_router


routers = APIRouter()
router_list = [agent_sql_router, exploratory_analysis_router, process_csv_router]

for router in router_list:
    routers.include_router(router)

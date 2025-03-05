from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import List, Annotated
from operator import add

class queryChat(BaseModel):
    question: str


class AgentState(TypedDict):
    question: str
    table_schemas: str
    database: str
    sql: str
    reflect: Annotated[List[str], add]
    accepted: bool
    revision: int
    max_revision: int
    results: List[tuple]
    interpretation: str
    plot_needed: bool
    plot_html: str
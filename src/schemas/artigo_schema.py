from pydantic import BaseModel as SCBaseModel, HttpUrl
from typing import Optional


class ArtigoSchema(SCBaseModel):
    id: Optional[int] = None 
    titulo: str 
    descricao: str
    url_fonte: HttpUrl 
    usuario_id: Optional[int]
    
    class Config:
        orm_mode = True
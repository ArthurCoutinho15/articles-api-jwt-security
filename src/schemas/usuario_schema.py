from pydantic import BaseModel as SCBaseModel, EmailStr
from typing import Optional, List

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int] = None 
    nome: str 
    sobrenome: str 
    email: EmailStr
    is_admin: bool
     
    class Config:
        orm_mode = True
        
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str
    
class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]
    
class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    is_admin: Optional[bool]
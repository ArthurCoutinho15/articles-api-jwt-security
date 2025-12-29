from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.__usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaArtigos, UsuarioSchemaCreate, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import Security
from core.auth import autenticar, _criar_token_acesso

security = Security()
router = APIRouter()

@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_signup(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome = usuario.sobrenome,
        email=usuario.email,
        senha=security.gerar_hash_senha(),
        is_admin=usuario.is_admin
    )
    
    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        
        return novo_usuario
    
@router.get('/usuarios', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios
        
@router.get('/usuarios/{usuario_id}', response_model=UsuarioSchemaArtigos)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().all()
        
        if usuario:
            return usuario
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{usuario_id}', response_model=UsuarioSchemaBase)
async def put_usuario(usuario: UsuarioSchemaUp, usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        
        if usuario_up:
            if usuario.nome:
                usuario.nome = usuario_up.nome
            if usuario.sobrenome:
                usuario.sobrenome = usuario_up.sobrenome 
            if usuario.email:
                usuario.email = usuario_up.email
            if usuario.is_admin:
                usuario.is_admin = usuario_up.is_admin
            if usuario.senha:
                usuario.senha = security.gerar_hash_senha(usuario.senha)
                
            await session.commit()
            
            return usuario_up
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).fiter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none() 
        
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de acesso incorretos.")
    
    return JSONResponse(
        content={
            "access_token": _criar_token_acesso(sub=usuario.id),
            "token_type": "bearer"
        },
        status_code=status.HTTP_200_OK
    )
    
            
from passlib.context import CryptContext


class Security:
    def __init__(self):
        self.CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verificar_senha(self, senha: str, hash_senha: str) -> bool:
        """
        Função para verificar se a senha está correta, comparando 
        a senha em texto puro, informada pelo usuário e o hash da senha que estará 
        salvo no banco de dados durante a criação da conta.
        """
        
        return self.CRIPTO.verify(senha, hash_senha)
    
    def gerar_hash_senha(self, senha: str) -> str:
        """
        Função que gera e retorna o hash da senha
        """
        
        return self.CRIPTO.hash(secret=senha)
    
security: Security = Security()
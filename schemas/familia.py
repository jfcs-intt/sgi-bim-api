from pydantic import BaseModel
from typing import Optional, List
from model.familia import Familia


class FamiliaSchema(BaseModel):
    """ Define como uma nova família a ser cadastrada deve ser representada
    """
    codigo_familia: str = "TUB-PVC"
    nome_familia: str = "Tubulações e Conexões PVC"
    descricao: Optional[str] = "Família de tubulações e conexões em PVC para sistemas hidrossanitários"


class FamiliaBuscaSchema(BaseModel):
    """ Define a estrutura de busca de família pelo código
    """
    codigo_familia: str = "TUB-PVC"


class FamiliaViewSchema(BaseModel):
    """ Define como uma família será retornada com total de componentes
    """
    id: int = 1
    codigo_familia: str = "TUB-PVC"
    nome_familia: str = "Tubulações e Conexões PVC"
    descricao: Optional[str] = None
    total_componentes: int = 0


class ListagemFamiliasSchema(BaseModel):
    """ Define como a listagem de famílias será retornada
    """
    familias: List[FamiliaSchema]


class FamiliaDelSchema(BaseModel):
    """ Define o retorno após remoção de uma família
    """
    mesage: str
    codigo_familia: str


def apresenta_familia(familia: Familia):
    """ Retorna a representação de uma família conforme FamiliaViewSchema
    """
    return {
        "id": familia.id,
        "codigo_familia": familia.codigo_familia,
        "nome_familia": familia.nome_familia,
        "descricao": familia.descricao,
        "total_componentes": len(familia.componentes)
    }


def apresenta_familias(familias: List[Familia]):
    """ Retorna a representação da listagem de famílias
    """
    result = []
    for familia in familias:
        result.append({
            "id": familia.id,
            "codigo_familia": familia.codigo_familia,
            "nome_familia": familia.nome_familia,
            "descricao": familia.descricao,
            "total_componentes": len(familia.componentes)
        })
    return {"familias": result}

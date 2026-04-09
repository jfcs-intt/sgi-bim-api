from pydantic import BaseModel
from typing import Optional, List
from model.componente import Componente


class ComponenteSchema(BaseModel):
    """ Define como um novo componente BIM a ser cadastrado deve ser representado
    """
    codigo_familia: str = "TUB-PVC"
    codigo_item: str = "TUB-PVC-001"
    nome_item: str = "Tubo PVC Rígido Água Fria DN 25mm"
    tipo: Optional[str] = "Tubulação"
    funcao: Optional[str] = "Condução de Fluidos"
    sistema: Optional[str] = "Hidrossanitário"
    subsistema: Optional[str] = "Água Fria"
    fabricante: Optional[str] = "Tigre"
    referencia_tecnica: Optional[str] = "Série Normal PN15"
    norma_tecnica: Optional[str] = "ABNT NBR 5648:2010"
    lod: Optional[str] = "LOD 300"
    fase_projeto: Optional[str] = "Projeto Executivo"
    cod_ifc: Optional[str] = "IfcPipeSegment"
    cod_omniclass: Optional[str] = "23-13 11 11"
    cod_ativo: Optional[str] = "HID-TUB-001"
    vida_util_anos: Optional[int] = 30
    orgao_regulador: Optional[str] = "INMETRO"
    norma_reguladora: Optional[str] = "Portaria INMETRO 455/2013"
    descricao_completa: Optional[str] = ""


class ComponenteBuscaSchema(BaseModel):
    """ Define a estrutura de busca de componente pelo código do item
    """
    codigo_item: str = "TUB-PVC-001"


class ComponenteFamiliaBuscaSchema(BaseModel):
    """ Define a estrutura de busca de componentes pelo código da família
    """
    codigo_familia: str = "TUB-PVC"


class ComponenteViewSchema(BaseModel):
    """ Define como um componente BIM será retornado
    """
    id: int = 1
    codigo_familia: str = "TUB-PVC"
    codigo_item: str = "TUB-PVC-001"
    nome_item: str = "Tubo PVC Rígido Água Fria DN 25mm"
    tipo: Optional[str] = None
    funcao: Optional[str] = None
    sistema: Optional[str] = None
    subsistema: Optional[str] = None
    fabricante: Optional[str] = None
    referencia_tecnica: Optional[str] = None
    norma_tecnica: Optional[str] = None
    lod: Optional[str] = None
    fase_projeto: Optional[str] = None
    cod_ifc: Optional[str] = None
    cod_omniclass: Optional[str] = None
    cod_ativo: Optional[str] = None
    vida_util_anos: Optional[int] = None
    orgao_regulador: Optional[str] = None
    norma_reguladora: Optional[str] = None
    descricao_completa: Optional[str] = None


class ListagemComponentesSchema(BaseModel):
    """ Define como a listagem de componentes será retornada
    """
    componentes: List[ComponenteSchema]


class ComponenteAtualizaSchema(BaseModel):
    """ Define os campos que podem ser atualizados em um componente BIM existente
    """
    nome_item: Optional[str] = None
    tipo: Optional[str] = None
    funcao: Optional[str] = None
    sistema: Optional[str] = None
    subsistema: Optional[str] = None
    fabricante: Optional[str] = None
    referencia_tecnica: Optional[str] = None
    norma_tecnica: Optional[str] = None
    lod: Optional[str] = None
    fase_projeto: Optional[str] = None
    cod_ifc: Optional[str] = None
    cod_omniclass: Optional[str] = None
    cod_ativo: Optional[str] = None
    vida_util_anos: Optional[int] = None
    orgao_regulador: Optional[str] = None
    norma_reguladora: Optional[str] = None
    descricao_completa: Optional[str] = None


class ComponenteDelSchema(BaseModel):
    """ Define o retorno após remoção de um componente
    """
    mesage: str
    codigo_item: str


def apresenta_componente(componente: Componente):
    """ Retorna a representação de um componente conforme ComponenteViewSchema
    """
    return {
        "id": componente.id,
        "codigo_familia": componente.familia.codigo_familia if componente.familia else None,
        "codigo_item": componente.codigo_item,
        "nome_item": componente.nome_item,
        "tipo": componente.tipo,
        "funcao": componente.funcao,
        "sistema": componente.sistema,
        "subsistema": componente.subsistema,
        "fabricante": componente.fabricante,
        "referencia_tecnica": componente.referencia_tecnica,
        "norma_tecnica": componente.norma_tecnica,
        "lod": componente.lod,
        "fase_projeto": componente.fase_projeto,
        "cod_ifc": componente.cod_ifc,
        "cod_omniclass": componente.cod_omniclass,
        "cod_ativo": componente.cod_ativo,
        "vida_util_anos": componente.vida_util_anos,
        "orgao_regulador": componente.orgao_regulador,
        "norma_reguladora": componente.norma_reguladora,
        "descricao_completa": componente.descricao_completa
    }


def apresenta_componentes(componentes: List[Componente]):
    """ Retorna a representação da listagem de componentes
    """
    result = []
    for componente in componentes:
        result.append({
            "id": componente.id,
            "codigo_familia": componente.familia.codigo_familia if componente.familia else None,
            "codigo_item": componente.codigo_item,
            "nome_item": componente.nome_item,
            "tipo": componente.tipo,
            "funcao": componente.funcao,
            "sistema": componente.sistema,
            "subsistema": componente.subsistema,
            "fabricante": componente.fabricante,
            "referencia_tecnica": componente.referencia_tecnica,
            "norma_tecnica": componente.norma_tecnica,
            "lod": componente.lod,
            "fase_projeto": componente.fase_projeto,
            "cod_ifc": componente.cod_ifc,
            "cod_omniclass": componente.cod_omniclass,
            "cod_ativo": componente.cod_ativo,
            "vida_util_anos": componente.vida_util_anos,
            "orgao_regulador": componente.orgao_regulador,
            "norma_reguladora": componente.norma_reguladora,
            "descricao_completa": componente.descricao_completa
        })
    return {"componentes": result}

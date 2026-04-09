from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Componente(Base):
    __tablename__ = 'componente_bim'

    id = Column("pk_componente", Integer, primary_key=True)
    familia_id = Column(Integer, ForeignKey("familia_bim.pk_familia"))
    codigo_item = Column(String(30), unique=True)
    nome_item = Column(String(200))

    # Grupo 1 - Tipo e Função
    tipo = Column(String(100))
    funcao = Column(String(100))
    sistema = Column(String(100))
    subsistema = Column(String(100))

    # Grupo 2 - Dados Técnicos
    fabricante = Column(String(100))
    referencia_tecnica = Column(String(200))
    norma_tecnica = Column(String(100))

    # Grupo 3 - Dados BIM
    lod = Column(String(20))
    fase_projeto = Column(String(50))
    cod_ifc = Column(String(50))
    cod_omniclass = Column(String(30))

    # Grupo 4 - Dados de Ativo
    cod_ativo = Column(String(30))
    vida_util_anos = Column(Integer)

    # Grupo 5 - Dados de Órgãos Reguladores
    orgao_regulador = Column(String(100))
    norma_reguladora = Column(String(100))

    descricao_completa = Column(String(500))
    data_insercao = Column(DateTime, default=datetime.now())

    familia = relationship("Familia", back_populates="componentes")

    def __init__(self, familia_id: int, codigo_item: str, nome_item: str,
                 tipo: str = None, funcao: str = None, sistema: str = None,
                 subsistema: str = None, fabricante: str = None,
                 referencia_tecnica: str = None, norma_tecnica: str = None,
                 lod: str = None, fase_projeto: str = None, cod_ifc: str = None,
                 cod_omniclass: str = None, cod_ativo: str = None,
                 vida_util_anos: int = None, orgao_regulador: str = None,
                 norma_reguladora: str = None, descricao_completa: str = None,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Componente BIM

        Arguments:
            familia_id: id da família à qual o componente pertence
            codigo_item: código único do item, ex: TUB-PVC-001
            nome_item: nome descritivo do componente
            (demais campos referentes aos 5 grupos de informação BIM)
            data_insercao: data de cadastro; se não informada, usa a data atual
        """
        self.familia_id = familia_id
        self.codigo_item = codigo_item
        self.nome_item = nome_item
        self.tipo = tipo
        self.funcao = funcao
        self.sistema = sistema
        self.subsistema = subsistema
        self.fabricante = fabricante
        self.referencia_tecnica = referencia_tecnica
        self.norma_tecnica = norma_tecnica
        self.lod = lod
        self.fase_projeto = fase_projeto
        self.cod_ifc = cod_ifc
        self.cod_omniclass = cod_omniclass
        self.cod_ativo = cod_ativo
        self.vida_util_anos = vida_util_anos
        self.orgao_regulador = orgao_regulador
        self.norma_reguladora = norma_reguladora
        self.descricao_completa = descricao_completa

        if data_insercao:
            self.data_insercao = data_insercao

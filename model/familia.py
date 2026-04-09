from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Familia(Base):
    __tablename__ = 'familia_bim'

    id = Column("pk_familia", Integer, primary_key=True)
    codigo_familia = Column(String(20), unique=True)
    nome_familia = Column(String(140))
    descricao = Column(String(500))
    data_insercao = Column(DateTime, default=datetime.now())

    componentes = relationship("Componente", cascade="all, delete-orphan", back_populates="familia")

    def __init__(self, codigo_familia: str, nome_familia: str, descricao: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Família de componentes BIM

        Arguments:
            codigo_familia: código identificador da família, ex: TUB-PVC
            nome_familia: nome descritivo da família
            descricao: descrição geral da família de componentes
            data_insercao: data de cadastro; se não informada, usa a data atual
        """
        self.codigo_familia = codigo_familia
        self.nome_familia = nome_familia
        self.descricao = descricao

        if data_insercao:
            self.data_insercao = data_insercao

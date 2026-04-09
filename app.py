from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Familia, Componente
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="SGI BIM API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
familia_tag = Tag(name="Família", description="Cadastro, consulta e remoção de famílias de componentes BIM")
componente_tag = Tag(name="Componente", description="Cadastro, consulta e remoção de componentes BIM")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela de escolha da documentação.
    """
    return redirect('/openapi')


@app.post('/familia', tags=[familia_tag],
          responses={"200": FamiliaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_familia(form: FamiliaSchema):
    """Cadastra uma nova família de componentes BIM.

    Retorna a representação da família cadastrada com o total de componentes associados.
    """
    familia = Familia(
        codigo_familia=form.codigo_familia,
        nome_familia=form.nome_familia,
        descricao=form.descricao)
    logger.debug(f"Cadastrando família: '{familia.codigo_familia}'")
    try:
        session = Session()
        session.add(familia)
        session.commit()
        logger.debug(f"Família cadastrada: '{familia.codigo_familia}'")
        return apresenta_familia(familia), 200

    except IntegrityError as e:
        error_msg = "Família com este código já cadastrada na base."
        logger.warning(f"Erro ao cadastrar família '{familia.codigo_familia}': {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível cadastrar a família."
        logger.warning(f"Erro ao cadastrar família '{familia.codigo_familia}': {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/familias', tags=[familia_tag],
         responses={"200": ListagemFamiliasSchema, "404": ErrorSchema})
def get_familias():
    """Retorna todas as famílias de componentes BIM cadastradas.
    """
    logger.debug("Buscando todas as famílias")
    session = Session()
    familias = session.query(Familia).all()

    if not familias:
        return {"familias": []}, 200
    else:
        logger.debug(f"{len(familias)} família(s) encontrada(s)")
        return apresenta_familias(familias), 200


@app.get('/familia', tags=[familia_tag],
         responses={"200": FamiliaViewSchema, "404": ErrorSchema})
def get_familia(query: FamiliaBuscaSchema):
    """Busca uma família pelo código informado.

    Retorna a representação da família com o total de componentes associados.
    """
    codigo_familia = query.codigo_familia
    logger.debug(f"Buscando família: '{codigo_familia}'")
    session = Session()
    familia = session.query(Familia).filter(Familia.codigo_familia == codigo_familia).first()

    if not familia:
        error_msg = "Família não encontrada na base."
        logger.warning(f"Família '{codigo_familia}' não encontrada")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Família encontrada: '{familia.codigo_familia}'")
        return apresenta_familia(familia), 200


@app.delete('/familia', tags=[familia_tag],
            responses={"200": FamiliaDelSchema, "404": ErrorSchema})
def del_familia(query: FamiliaBuscaSchema):
    """Remove uma família pelo código informado.

    Todos os componentes associados à família também serão removidos.
    """
    codigo_familia = unquote(unquote(query.codigo_familia))
    logger.debug(f"Removendo família: '{codigo_familia}'")
    session = Session()
    count = session.query(Familia).filter(Familia.codigo_familia == codigo_familia).delete()
    session.commit()

    if count:
        logger.debug(f"Família removida: '{codigo_familia}'")
        return {"mesage": "Família removida", "codigo_familia": codigo_familia}
    else:
        error_msg = "Família não encontrada na base."
        logger.warning(f"Família '{codigo_familia}' não encontrada para remoção")
        return {"mesage": error_msg}, 404


@app.post('/componente', tags=[componente_tag],
          responses={"200": ComponenteViewSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def add_componente(form: ComponenteSchema):
    """Cadastra um novo componente BIM vinculado a uma família existente.

    Retorna a representação completa do componente cadastrado.
    """
    logger.debug(f"Cadastrando componente: '{form.codigo_item}'")
    session = Session()
    familia = session.query(Familia).filter(Familia.codigo_familia == form.codigo_familia).first()

    if not familia:
        error_msg = "Família informada não encontrada na base."
        logger.warning(f"Família '{form.codigo_familia}' não encontrada ao cadastrar componente")
        return {"mesage": error_msg}, 404

    componente = Componente(
        familia_id=familia.id,
        codigo_item=form.codigo_item,
        nome_item=form.nome_item,
        tipo=form.tipo,
        funcao=form.funcao,
        sistema=form.sistema,
        subsistema=form.subsistema,
        fabricante=form.fabricante,
        referencia_tecnica=form.referencia_tecnica,
        norma_tecnica=form.norma_tecnica,
        lod=form.lod,
        fase_projeto=form.fase_projeto,
        cod_ifc=form.cod_ifc,
        cod_omniclass=form.cod_omniclass,
        cod_ativo=form.cod_ativo,
        vida_util_anos=form.vida_util_anos,
        orgao_regulador=form.orgao_regulador,
        norma_reguladora=form.norma_reguladora,
        descricao_completa=form.descricao_completa)

    try:
        session.add(componente)
        session.commit()
        logger.debug(f"Componente cadastrado: '{componente.codigo_item}'")
        return apresenta_componente(componente), 200

    except IntegrityError as e:
        error_msg = "Componente com este código já cadastrado na base."
        logger.warning(f"Erro ao cadastrar componente '{form.codigo_item}': {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível cadastrar o componente."
        logger.warning(f"Erro ao cadastrar componente '{form.codigo_item}': {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/componentes', tags=[componente_tag],
         responses={"200": ListagemComponentesSchema, "404": ErrorSchema})
def get_componentes():
    """Retorna todos os componentes BIM cadastrados na base.
    """
    logger.debug("Buscando todos os componentes")
    session = Session()
    componentes = session.query(Componente).all()

    if not componentes:
        return {"componentes": []}, 200
    else:
        logger.debug(f"{len(componentes)} componente(s) encontrado(s)")
        return apresenta_componentes(componentes), 200


@app.get('/componente', tags=[componente_tag],
         responses={"200": ComponenteViewSchema, "404": ErrorSchema})
def get_componente(query: ComponenteBuscaSchema):
    """Busca um componente BIM pelo código do item.

    Retorna a representação completa do componente com todos os atributos BIM.
    """
    codigo_item = query.codigo_item
    logger.debug(f"Buscando componente: '{codigo_item}'")
    session = Session()
    componente = session.query(Componente).filter(Componente.codigo_item == codigo_item).first()

    if not componente:
        error_msg = "Componente não encontrado na base."
        logger.warning(f"Componente '{codigo_item}' não encontrado")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Componente encontrado: '{componente.codigo_item}'")
        return apresenta_componente(componente), 200


@app.get('/componentes/familia', tags=[componente_tag],
         responses={"200": ListagemComponentesSchema, "404": ErrorSchema})
def get_componentes_por_familia(query: ComponenteFamiliaBuscaSchema):
    """Lista todos os componentes BIM pertencentes a uma família específica.

    Retorna a listagem de componentes filtrados pelo código da família.
    """
    codigo_familia = query.codigo_familia
    logger.debug(f"Buscando componentes da família: '{codigo_familia}'")
    session = Session()
    familia = session.query(Familia).filter(Familia.codigo_familia == codigo_familia).first()

    if not familia:
        error_msg = "Família não encontrada na base."
        logger.warning(f"Família '{codigo_familia}' não encontrada")
        return {"mesage": error_msg}, 404

    componentes = session.query(Componente).filter(Componente.familia_id == familia.id).all()

    if not componentes:
        return {"componentes": []}, 200
    else:
        logger.debug(f"{len(componentes)} componente(s) encontrado(s) para família '{codigo_familia}'")
        return apresenta_componentes(componentes), 200


@app.put('/componente', tags=[componente_tag],
         responses={"200": ComponenteViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def atualiza_componente(query: ComponenteBuscaSchema, form: ComponenteAtualizaSchema):
    """Atualiza os dados de um componente BIM existente pelo código do item.

    Apenas os campos informados serão atualizados. Campos não enviados permanecem inalterados.
    """
    codigo_item = query.codigo_item
    logger.debug(f"Atualizando componente: '{codigo_item}'")
    session = Session()
    componente = session.query(Componente).filter(Componente.codigo_item == codigo_item).first()

    if not componente:
        error_msg = "Componente não encontrado na base."
        logger.warning(f"Componente '{codigo_item}' não encontrado para atualização")
        return {"mesage": error_msg}, 404

    try:
        if form.nome_item is not None: componente.nome_item = form.nome_item
        if form.tipo is not None: componente.tipo = form.tipo
        if form.funcao is not None: componente.funcao = form.funcao
        if form.sistema is not None: componente.sistema = form.sistema
        if form.subsistema is not None: componente.subsistema = form.subsistema
        if form.fabricante is not None: componente.fabricante = form.fabricante
        if form.referencia_tecnica is not None: componente.referencia_tecnica = form.referencia_tecnica
        if form.norma_tecnica is not None: componente.norma_tecnica = form.norma_tecnica
        if form.lod is not None: componente.lod = form.lod
        if form.fase_projeto is not None: componente.fase_projeto = form.fase_projeto
        if form.cod_ifc is not None: componente.cod_ifc = form.cod_ifc
        if form.cod_omniclass is not None: componente.cod_omniclass = form.cod_omniclass
        if form.cod_ativo is not None: componente.cod_ativo = form.cod_ativo
        if form.vida_util_anos is not None: componente.vida_util_anos = form.vida_util_anos
        if form.orgao_regulador is not None: componente.orgao_regulador = form.orgao_regulador
        if form.norma_reguladora is not None: componente.norma_reguladora = form.norma_reguladora
        if form.descricao_completa is not None: componente.descricao_completa = form.descricao_completa

        session.commit()
        logger.debug(f"Componente atualizado: '{codigo_item}'")
        return apresenta_componente(componente), 200

    except Exception as e:
        error_msg = "Não foi possível atualizar o componente."
        logger.warning(f"Erro ao atualizar componente '{codigo_item}': {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/componente', tags=[componente_tag],
            responses={"200": ComponenteDelSchema, "404": ErrorSchema})
def del_componente(query: ComponenteBuscaSchema):
    """Remove um componente BIM pelo código do item informado.
    """
    codigo_item = unquote(unquote(query.codigo_item))
    logger.debug(f"Removendo componente: '{codigo_item}'")
    session = Session()
    count = session.query(Componente).filter(Componente.codigo_item == codigo_item).delete()
    session.commit()

    if count:
        logger.debug(f"Componente removido: '{codigo_item}'")
        return {"mesage": "Componente removido", "codigo_item": codigo_item}
    else:
        error_msg = "Componente não encontrado na base."
        logger.warning(f"Componente '{codigo_item}' não encontrado para remoção")
        return {"mesage": error_msg}, 404

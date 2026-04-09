# SGI BIM — API

**Sistema de Gestão de Informação BIM**
API REST para cadastro e consulta de componentes BIM, baseada na norma ISO 19650 para gestão de LOIN (*Level of Information Need*).

---

## Descrição

O SGI BIM centraliza metadados de materiais e componentes de engenharia em uma biblioteca BIM estruturada. Cada componente é organizado em uma **família** e descrito por cinco grupos de informação: Tipo e Função, Dados Técnicos, Dados BIM, Dados de Ativo e Dados Regulatórios — compatível com os padrões IFC, Omniclass e COBie.

A API fornece endpoints para criação, consulta, atualização e remoção de famílias e componentes, com documentação automática via Swagger (OpenAPI 3.0).

---

## Tecnologias

| Tecnologia | Função |
|------------|--------|
| Python 3.x | Linguagem principal |
| Flask | Framework web |
| flask-openapi3 | Documentação Swagger/OpenAPI automática |
| SQLAlchemy | ORM para acesso ao banco de dados |
| SQLite | Banco de dados relacional local |
| Pydantic | Validação de schemas de entrada e saída |
| Flask-CORS | Habilitar requisições cross-origin do frontend |

---

## Estrutura do Projeto

```
sgi-bim-api/
├── app.py              ← Ponto de entrada, definição das rotas
├── requirements.txt    ← Dependências Python
├── logger.py           ← Configuração de log com rotação de arquivo
├── model/
│   ├── __init__.py     ← Inicializa banco e exporta Session e modelos
│   ├── base.py         ← Configuração da conexão SQLAlchemy
│   ├── familia.py      ← Modelo da tabela familia_bim
│   └── componente.py   ← Modelo da tabela componente_bim
└── schemas/
    ├── __init__.py     ← Exporta todos os schemas e funções
    ├── familia.py      ← Schemas Pydantic para família
    ├── componente.py   ← Schemas Pydantic para componente
    └── error.py        ← Schema de erro padrão
```

O banco de dados SQLite (`database/db.sqlite3`) é criado automaticamente na primeira execução.

---

## Como Instalar e Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd sgi-bim-api
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a API

```bash
flask run --host 0.0.0.0 --port 5000
```

A API estará disponível em: `http://localhost:5000`

---

## Documentação Swagger

Acesse `http://localhost:5000/openapi` no navegador para visualizar e testar todos os endpoints interativamente.

---

## Rotas Disponíveis

### Família

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/familia` | Cadastrar nova família BIM |
| `GET` | `/familias` | Listar todas as famílias |
| `GET` | `/familia` | Buscar família por código |
| `DELETE` | `/familia` | Remover família e seus componentes |

### Componente

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/componente` | Cadastrar novo componente BIM |
| `GET` | `/componentes` | Listar todos os componentes |
| `GET` | `/componente` | Buscar componente por código |
| `GET` | `/componentes/familia` | Listar componentes de uma família |
| `PUT` | `/componente` | Atualizar dados de um componente |
| `DELETE` | `/componente` | Remover componente por código |

---

## Modelo de Dados

O sistema usa duas tabelas com relacionamento um-para-muitos:

```
familia_bim
  └── id, codigo_familia (único), nome_familia, descricao, data_insercao

componente_bim
  └── id, familia_id (FK), codigo_item (único), nome_item
      Grupo 1: tipo, funcao, sistema, subsistema
      Grupo 2: fabricante, referencia_tecnica, norma_tecnica
      Grupo 3: lod, fase_projeto, cod_ifc, cod_omniclass
      Grupo 4: cod_ativo, vida_util_anos
      Grupo 5: orgao_regulador, norma_reguladora
      descricao_completa, data_insercao
```

A remoção de uma família exclui automaticamente todos os componentes associados (cascade delete).

---

## Referências

- ISO 19650 — Organização e digitalização de informações sobre edifícios e obras de engenharia civil
- IFC (Industry Foundation Classes) — buildingSMART International
- Omniclass Construction Classification System
- ABNT NBR 15965 — Sistema de classificação da informação da construção

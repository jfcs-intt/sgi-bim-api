# Plano de Trabalho — SGI BIM MVP
**Pós-Graduação em Engenharia de Software — PUC Rio**
**Sprint 1 — MVP**
**Entrega:** 12/09/2026

---

## 1. Descrição do Projeto

**SGI BIM — Sistema de Gestão de Informação BIM**

Sistema web para cadastro e consulta de componentes BIM (Building Information Modeling), baseado na norma ISO 19650 para gestão de LOIN (*Level of Information Need*). O sistema organiza metadados de materiais e componentes em bibliotecas BIM, estruturados em famílias e subitens, para uso em projetos de engenharia e arquitetura — com capacidade de exportação/consumo por ferramentas como Autodesk Revit.

**Problema resolvido:** centralizar e padronizar as informações de objetos BIM (dados técnicos, dados BIM, dados de ativo e dados regulatórios) em um banco de dados estruturado, permitindo rastreabilidade, consulta e reuso das informações em projetos.

**Contexto de uso:** projetos de engenharia multidisciplinar (elétrica, hidrossanitária, estrutural, etc.), compatível com padrões internacionais (ISO 19650, IFC, Omniclass, COBie).

---

## 2. Ideia da Aplicação

### Qual é o problema?
Projetos BIM exigem que cada objeto/componente modelado contenha um conjunto preciso de informações (LOIN — *Level of Information Need*). Hoje essas informações ficam dispersas em planilhas, catálogos de fabricantes e documentos avulsos. O SGI BIM centraliza tudo isso em uma única base de dados consultável.

### O que o sistema faz?
- Cadastra **famílias de componentes** (ex: Tubulações PVC, Cabos Elétricos BT)
- Cadastra **subitens** de cada família com atributos organizados em 5 grupos
- Monta automaticamente uma **descrição técnica completa** no padrão de lista de materiais
- Permite consultar, filtrar e excluir registros via interface web

### Os 5 grupos de informação por componente:
1. **Tipo e Função** — classificação hierárquica (tipo, função, sistema, subsistema)
2. **Dados Técnicos** — fabricante, referência técnica, norma técnica
3. **Dados BIM** — LOD, fase de projeto, código IFC, código Omniclass
4. **Dados de Ativo** — código de ativo, vida útil (conforme ISO 19650)
5. **Dados de Órgãos Reguladores** — órgão regulador e norma reguladora aplicável

---

## 3. Infraestrutura (Stack Tecnológico)

### Backend (API)
| Tecnologia | Função |
|------------|--------|
| Python 3.x | Linguagem principal |
| Flask | Framework web para a API |
| flask-openapi3 | Documentação automática Swagger/OpenAPI |
| SQLAlchemy | ORM para acesso ao banco de dados |
| SQLite | Banco de dados relacional local |
| Pydantic | Validação de dados e schemas |
| Flask-CORS | Habilitar chamadas cross-origin do frontend |

### Frontend
| Tecnologia | Função |
|------------|--------|
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização própria (tema BIM/engenharia) |
| JavaScript (vanilla) | Lógica da SPA e chamadas à API |

---

## 4. Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR (Cliente)                   │
│  ┌─────────────────────────────────────────────────┐    │
│  │              sgi-bim-front                       │    │
│  │   index.html + styles.css + scripts.js           │    │
│  │   (SPA — abre direto no navegador, sem servidor) │    │
│  └────────────────────┬────────────────────────────┘    │
└───────────────────────┼─────────────────────────────────┘
                        │ HTTP (fetch API)
                        │ porta 5000
┌───────────────────────▼─────────────────────────────────┐
│                  sgi-bim-api (Backend)                   │
│   Flask + flask-openapi3 + SQLAlchemy                    │
│                                                          │
│   /familia    POST, GET, DELETE                          │
│   /familias   GET                                        │
│   /componente POST, GET, DELETE                          │
│   /componentes GET                                       │
│   /componentes/familia  GET                              │
│                         │                               │
│              ┌──────────▼──────────┐                    │
│              │   SQLite (db.sqlite3)│                    │
│              │  familia_bim        │                    │
│              │  componente_bim     │                    │
│              └─────────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Modelo de Banco de Dados

### Tabela: `familia_bim`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Chave primária auto-incremental |
| codigo_familia | String (único) | Ex: `TUB-PVC`, `CAB-BT` |
| nome_familia | String | Ex: `Tubulações e Conexões PVC` |
| descricao | String | Descrição geral da família |
| data_insercao | DateTime | Data e hora do cadastro |

### Tabela: `componente_bim`
| Campo | Tipo | Grupo | Exemplo |
|-------|------|-------|---------|
| id | Integer (PK) | — | Auto |
| familia_id | Integer (FK) | — | Referência à familia_bim |
| codigo_item | String (único) | — | `TUB-PVC-001` |
| nome_item | String | — | `Tubo PVC Rígido DN 25mm` |
| tipo | String | Grupo 1 | `Tubulação` |
| funcao | String | Grupo 1 | `Condução de Fluidos` |
| sistema | String | Grupo 1 | `Hidrossanitário` |
| subsistema | String | Grupo 1 | `Água Fria` |
| fabricante | String | Grupo 2 | `Tigre` |
| referencia_tecnica | String | Grupo 2 | `Série Normal PN15` |
| norma_tecnica | String | Grupo 2 | `ABNT NBR 5648:2010` |
| lod | String | Grupo 3 | `LOD 300` |
| fase_projeto | String | Grupo 3 | `Projeto Executivo` |
| cod_ifc | String | Grupo 3 | `IfcPipeSegment` |
| cod_omniclass | String | Grupo 3 | `23-13 11 11` |
| cod_ativo | String | Grupo 4 | `HID-TUB-001` |
| vida_util_anos | Integer | Grupo 4 | `30` |
| orgao_regulador | String | Grupo 5 | `INMETRO` |
| norma_reguladora | String | Grupo 5 | `Portaria INMETRO 455/2013` |
| descricao_completa | String | — | Montada semi-manualmente |
| data_insercao | DateTime | — | Data e hora do cadastro |

---

## 6. Rotas da API (9 rotas)

### Família
| # | Método | Rota | Descrição |
|---|--------|------|-----------|
| 1 | POST | `/familia` | Cadastrar nova família BIM |
| 2 | GET | `/familias` | Listar todas as famílias |
| 3 | GET | `/familia` | Buscar família por `codigo_familia` |
| 4 | DELETE | `/familia` | Deletar família e seus componentes |

### Componente
| # | Método | Rota | Descrição |
|---|--------|------|-----------|
| 5 | POST | `/componente` | Cadastrar novo componente BIM |
| 6 | GET | `/componentes` | Listar todos os componentes |
| 7 | GET | `/componente` | Buscar componente por `codigo_item` |
| 8 | GET | `/componentes/familia` | Listar componentes de uma família |
| 9 | DELETE | `/componente` | Deletar componente por `codigo_item` |

---

## 7. Estrutura de Arquivos

```
sp1-mvp/
├── desenvolvimento-full-stack/       ← Repositório de exemplo do curso (referência)
├── PLdeTrabalho.md                   ← Este documento
│
├── sgi-bim-api/                      ← REPOSITÓRIO 1 — Backend
│   ├── app.py                        ← Ponto de entrada da API, definição das rotas
│   ├── requirements.txt              ← Dependências Python
│   ├── README.md                     ← Documentação do projeto backend
│   ├── logger.py                     ← Configuração de log
│   ├── model/
│   │   ├── __init__.py               ← Exporta Session, Base e modelos
│   │   ├── base.py                   ← Configuração da conexão SQLAlchemy
│   │   ├── familia.py                ← Modelo da tabela familia_bim
│   │   └── componente.py             ← Modelo da tabela componente_bim
│   └── schemas/
│       ├── __init__.py               ← Exporta todos os schemas e funções
│       ├── familia.py                ← Schemas Pydantic para família
│       ├── componente.py             ← Schemas Pydantic para componente
│       └── error.py                  ← Schema de erro padrão
│
└── sgi-bim-front/                    ← REPOSITÓRIO 2 — Frontend
    ├── index.html                    ← SPA principal
    ├── styles.css                    ← Estilização própria (tema BIM)
    ├── scripts.js                    ← Lógica JavaScript e chamadas à API
    └── README.md                     ← Documentação do projeto frontend
```

---

## 8. Dados de Exemplo para Demonstração

### Família 1 — TUB-PVC (Tubulações e Conexões PVC)
| Código | Nome | Descrição Completa |
|--------|------|--------------------|
| TUB-PVC-001 | Tubo PVC Rígido Água Fria DN 25mm | `TUBO PVC RÍGIDO - SÉRIE NORMAL PN15 - ÁGUA FRIA - DN 25mm - COR MARROM - CONF. ABNT NBR 5648:2010 - FABRICANTE TIGRE` |
| TUB-PVC-002 | Tubo PVC Rígido Água Fria DN 50mm | `TUBO PVC RÍGIDO - SÉRIE NORMAL PN10 - ÁGUA FRIA - DN 50mm - COR MARROM - CONF. ABNT NBR 5648:2010 - FABRICANTE TIGRE` |
| TUB-PVC-003 | Joelho PVC 90° Curto DN 25mm | `JOELHO PVC 90° CURTO - ÁGUA FRIA - DN 25mm - COR MARROM - CONF. ABNT NBR 10351:2014 - FABRICANTE TIGRE` |

### Família 2 — CAB-BT (Cabos Elétricos Baixa Tensão)
| Código | Nome | Descrição Completa |
|--------|------|--------------------|
| CAB-BT-001 | Cabo Flexível 750V 1,5mm² Preto | `CABO DE ENERGIA FLEXÍVEL - CLASSE 4 - 0,6/1kV - 1X1,5mm² - ISOLAÇÃO PVC/70°C - COR PRETO - CONF. ABNT NBR IEC 60228 - FABRICANTE PRYSMIAN` |
| CAB-BT-002 | Cabo Flexível 750V 2,5mm² Preto | `CABO DE ENERGIA FLEXÍVEL - CLASSE 4 - 0,6/1kV - 1X2,5mm² - ISOLAÇÃO PVC/70°C - COR PRETO - CONF. ABNT NBR IEC 60228 - FABRICANTE PRYSMIAN` |
| CAB-BT-003 | Cabo Flexível 750V 4,0mm² Preto | `CABO DE ENERGIA FLEXÍVEL - CLASSE 4 - 0,6/1kV - 1X4,0mm² - ISOLAÇÃO PVC/70°C - COR PRETO - CONF. ABNT NBR IEC 60228 - FABRICANTE PRYSMIAN` |

---

## 9. Ordem de Implementação

1. **Criar estrutura de pastas** — `sgi-bim-api/` e `sgi-bim-front/`
2. **Criar ambiente virtual Python** — `.venv` dentro de `sgi-bim-api/`
3. **Instalar dependências** — `pip install -r requirements.txt`
4. **Implementar o backend:**
   - `model/base.py` → conexão com SQLite
   - `model/familia.py` → tabela familia_bim
   - `model/componente.py` → tabela componente_bim com FK
   - `model/__init__.py` → exportações
   - `schemas/` → validação Pydantic
   - `app.py` → 9 rotas Flask com Swagger
5. **Testar todas as rotas via Swagger** (`http://localhost:5000/openapi`)
6. **Implementar o frontend:**
   - `index.html` → estrutura SPA com seções para família e componentes
   - `styles.css` → tema BIM/engenharia com CSS próprio
   - `scripts.js` → fetch API chamando todas as 9 rotas
7. **Testar frontend** abrindo `index.html` diretamente no navegador
8. **Escrever README.md** para os dois repositórios
9. **Criar repositórios no GitHub** e publicar

---

## 10. Critérios de Entrega (Checklist)

- [ ] API em Python com Flask — mínimo 4 rotas (temos 9)
- [ ] Pelo menos 1 rota POST (temos 2: `/familia` e `/componente`)
- [ ] Banco SQLite com pelo menos 1 tabela (temos 2 com relacionamento)
- [ ] Documentação Swagger com descrição, request/response e status codes
- [ ] Frontend SPA em HTML + CSS + JavaScript puro (sem Angular/Vue/React)
- [ ] Elementos exibidos em cards
- [ ] Frontend chama todas as rotas da API
- [ ] CSS próprio com regras personalizadas
- [ ] `index.html` abre diretamente no navegador sem extensões ou servidores locais
- [ ] Dois repositórios públicos no GitHub
- [ ] README.md em ambos os repositórios (título, descrição, instruções de instalação)
- [ ] Vídeo de até 4 minutos: objetivo (20-60s) + API/Swagger (60-90s) + Frontend (60-90s)

---

## 11. Roteiro do Vídeo (a produzir após conclusão do código)

### Parte 1 — Objetivo da aplicação (20 a 60 segundos)
- Apresentar o conceito de LOIN e ISO 19650
- Explicar o problema: informações BIM dispersas em planilhas e catálogos
- Mostrar o SGI BIM como solução: banco de dados centralizado de componentes

### Parte 2 — Execução da API via Swagger (60 a 90 segundos)
- Abrir `http://localhost:5000/openapi`
- Demonstrar rota `POST /familia` — cadastrar TUB-PVC
- Demonstrar rota `GET /familias` — listar famílias
- Demonstrar rota `POST /componente` — cadastrar TUB-PVC-001
- Demonstrar rota `GET /componentes/familia` — filtrar por família
- Demonstrar rota `DELETE /componente` — deletar um componente

### Parte 3 — Execução do frontend (60 a 90 segundos)
- Abrir `index.html` diretamente no navegador (sem servidor)
- Mostrar cadastro de família (chama POST /familia)
- Mostrar listagem de famílias (chama GET /familias)
- Mostrar cadastro de componente com montagem da descrição (chama POST /componente)
- Mostrar cards de componentes (chama GET /componentes)
- Mostrar filtro por família (chama GET /componentes/familia)
- Mostrar exclusão de componente (chama DELETE /componente)

---

## 12. Evolução Futura — v2.0

As melhorias abaixo foram identificadas durante o desenvolvimento do MVP e representam o caminho natural de evolução do sistema para uma versão completa integrada ao SEBIM HUB.

### 12.1 Sistema de Propriedades Dinâmicas por Família
Atualmente os campos técnicos dos componentes são fixos (fabricante, norma, referência, etc.). Na v2.0, cada família poderia definir suas próprias propriedades (ex: "Diâmetro Nominal", "Pressão Nominal", "Cor", "Seção"), e os componentes preencheriam apenas os valores dessas propriedades. A descrição completa e o nome do item seriam gerados automaticamente pela concatenação dos valores cadastrados.

Isso exigiria duas novas tabelas:
- `propriedade_familia` — define quais atributos pertencem a cada família
- `valor_propriedade` — armazena os valores de cada atributo por componente

### 12.2 Integração com SEBIM HUB
O SGI BIM foi concebido como módulo standalone compatível com a plataforma SEBIM HUB (Intertechne). A integração prevista incluiria autenticação por token, exportação de componentes em formato IFC e consumo da API por ferramentas BIM como Autodesk Revit via plugins Dynamo.

### 12.3 Exportação para Lista de Materiais
Rota `GET /componentes/exportar` que gera um arquivo `.csv` ou `.xlsx` com todos os componentes de um projeto, no formato de lista de materiais pronta para uso em projetos de engenharia.

---

## 14. Observações

- O projeto usa como referência estrutural o código de exemplo do curso (`desenvolvimento-full-stack-basico/aula-3`), mas com domínio, modelos, lógica e interface completamente diferentes.
- Futura integração prevista com a plataforma **SEBIM HUB** (Intertechne) em segunda etapa, fora do escopo deste MVP.

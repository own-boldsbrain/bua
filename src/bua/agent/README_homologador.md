# Agente Autônomo Homologador 360º

Este projeto implementa um agente autônomo inteligente especializado em automatizar o processo de homologação de projetos de Geração Distribuída (GD) junto às concessionárias de energia e órgãos reguladores brasileiros.

## Visão Geral

O **HomologadorAgent** é uma personalização do framework BUA (Browser Using Agent) que automatiza as seguintes atividades:

- ✅ Navegação automatizada pelos portais das distribuidoras
- ✅ Autenticação automática (login/senha ou certificado digital)
- ✅ Preenchimento automático de formulários de solicitação
- ✅ Upload de documentos requeridos
- ✅ Acompanhamento do status da solicitação
- ✅ Consultas a órgãos reguladores (ANEEL, etc.)

## Funcionalidades Principais

### 1. Homologação Automática
```python
from bua.agent.homologador_agent import create_homologador_agent

# Criar agente para um projeto específico
agente = create_homologador_agent(
    projeto_id="PROJ-2024-001",
    distribuidora_codigo="CEMIG"
)

# Iniciar processo de homologação
resultado = agente.iniciar_homologacao(projeto_data)
```

### 2. Consulta a Órgãos Reguladores
```python
# Consultar normas da ANEEL
consulta = agente.consultar_orgao_regulador(
    orgao="aneel",
    consulta="normas_conexao_gd_2024"
)
```

### 3. Integração com Dados Existentes
O agente se integra automaticamente com:
- Base de dados das distribuidoras
- Informações de autenticação
- Lista de documentos requeridos
- Configurações específicas de cada portal

## Arquitetura

```
HomologadorAgent
├── Agent (base class)
├── DistribuidorasGDService (integração)
├── Métodos especializados:
│   ├── _realizar_autenticacao()
│   ├── _navegar_para_homologacao()
│   ├── _preencher_formulario_solicitacao()
│   ├── _upload_documentos()
│   ├── _submeter_solicitacao()
│   └── _acompanhar_status()
└── consultar_orgao_regulador()
```

## Fluxo de Homologação

1. **Carregamento de Dados**: O agente carrega informações da distribuidora
2. **Navegação**: Acesso ao portal da distribuidora
3. **Autenticação**: Login automático usando credenciais armazenadas
4. **Navegação Específica**: Localização da seção de homologação GD
5. **Preenchimento**: Formulário preenchido com dados do projeto
6. **Upload**: Documentos requeridos enviados automaticamente
7. **Submissão**: Solicitação finalizada
8. **Acompanhamento**: Status monitorado periodicamente

## Configuração

### Pré-requisitos
- Python 3.11+
- Framework BUA instalado
- Credenciais de acesso aos portais das distribuidoras
- Documentação do projeto preparada

### Instalação
```bash
pip install -e .
```

### Configuração de Credenciais
As credenciais devem ser configuradas no sistema de gestão de distribuidoras:

```python
# Exemplo de configuração
distribuidora_config = {
    "codigo": "CEMIG",
    "portal_homologacao": {
        "url": "https://portal.cemig.com.br/homologacao",
        "autenticacao": {
            "metodo": "login_senha",
            "usuario": "seu_usuario",
            "senha": "sua_senha"
        }
    },
    "documentos_requeridos": [
        "projeto_executivo",
        "art_licenciamento",
        "certificado_qualidade"
    ]
}
```

## Exemplo de Uso

Veja o arquivo `exemplo_homologador.py` para um exemplo completo de uso.

## Suporte a Distribuidoras

Atualmente suportado:
- CEMIG (Minas Gerais)
- COPEL (Paraná)
- ELETROPAULO (São Paulo)
- Outras distribuidoras podem ser adicionadas

## Órgãos Reguladores

Integração com:
- ANEEL (Agência Nacional de Energia Elétrica)
- ARSESP (Agência Reguladora de Saneamento e Energia do Estado de SP)
- Outros órgãos estaduais

## Segurança

- ✅ Autenticação segura
- ✅ Verificação de URLs confiáveis
- ✅ Isolamento de sessões
- ✅ Logs de auditoria

## Próximos Passos

- [ ] Suporte a mais distribuidoras
- [ ] Integração com OCR para documentos
- [ ] Machine Learning para otimização de processos
- [ ] Dashboard de monitoramento
- [ ] API REST para integração

## Contribuição

Para contribuir com o desenvolvimento:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Adicione testes
5. Submeta um Pull Request

## Licença

Este projeto está sob a licença MIT.
"""
Exemplo de uso do Agente Autônomo Homologador 360º
"""

from bua.agent.homologador_agent import create_homologador_agent


def exemplo_homologacao():
    """
    Exemplo de como usar o agente homologador para iniciar um processo
    de homologação de projeto de GD
    """

    # Dados do projeto
    projeto_data = {
        "id": "PROJ-2024-001",
        "potencia_instalada": 50.0,  # kWp
        "localizacao": {
            "endereco": "Rua das Flores, 123",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01234-567"
        },
        "proprietario": {
            "nome": "João Silva",
            "cpf": "123.456.789-00",
            "contato": "joao@email.com"
        },
        "documentos": [
            "projeto_executivo.pdf",
            "art_licenciamento.pdf",
            "certificado_qualidade.pdf"
        ]
    }

    # Criar instância do agente
    agente = create_homologador_agent(
        projeto_id=projeto_data["id"],
        distribuidora_codigo="CEMIG",  # Código da distribuidora
        computer=None,  # Será configurado posteriormente
        model="computer-use-preview"
    )

    # Simular entrada para iniciar homologação
    input_items = [{
        "type": "homologacao_request",
        "projeto_data": projeto_data
    }]

    # Executar o processo
    resultado = agente.run_full_turn(input_items)

    print("Resultado da homologação:")
    for item in resultado:
        print(f"- {item}")

    return resultado


def exemplo_consulta_orgao():
    """
    Exemplo de consulta a órgão regulador
    """

    agente = create_homologador_agent(
        projeto_id="PROJ-2024-002",
        distribuidora_codigo="COPEL"
    )

    # Consulta à ANEEL
    input_items = [{
        "type": "consulta_orgao",
        "orgao": "aneel",
        "consulta": "normas_conexao_gd_2024"
    }]

    resultado = agente.run_full_turn(input_items)

    print("Resultado da consulta:")
    for item in resultado:
        print(f"- {item}")

    return resultado


if __name__ == "__main__":
    print("=== Exemplo de Homologação ===")
    exemplo_homologacao()

    print("\n=== Exemplo de Consulta a Órgão ===")
    exemplo_consulta_orgao()
"""
Versão temporária (stub) do HomologadorAgent para permitir
que a API funcione enquanto o módulo BUA não é instalado propriamente.

Esta é uma versão simplificada do agente de homologação original
que implementa as mesmas interfaces mas com funcionalidade limitada.
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime


class HomologadorAgent:
    """
    Stub do agente autônomo especializado em homologação 360º de projetos de GD.
    """

    def __init__(
        self,
        model: str = "computer-use-preview",
        computer: Optional[Any] = None,
        tools: list[dict] = [],
        acknowledge_safety_check_callback: Callable = lambda: False,
        projeto_id: Optional[str] = None,
        distribuidora_codigo: Optional[str] = None,
    ):
        self.projeto_id = projeto_id
        self.distribuidora_codigo = distribuidora_codigo
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"[STUB] Inicializando HomologadorAgent para projeto {projeto_id} "
            f"na distribuidora {distribuidora_codigo}"
        )

    def iniciar_homologacao(self, projeto_data: Dict) -> List[Dict]:
        """
        Inicia o processo de homologação para um projeto específico (stub)

        Args:
            projeto_data: Dados do projeto a ser homologado

        Returns:
            Lista de ações realizadas
        """
        self.logger.info(f"[STUB] Iniciando homologação para projeto {self.projeto_id}")

        # Simular ações de homologação
        return [
            {
                "type": "homologacao_iniciada",
                "projeto_id": self.projeto_id,
                "distribuidora": self.distribuidora_codigo,
                "status": "em_analise",
                "mensagem": "Esta é uma implementação temporária (stub) do HomologadorAgent",
                "timestamp": datetime.now().isoformat(),
            }
        ]

    def consultar_orgao_regulador(self, orgao: str, consulta: str) -> Dict:
        """
        Consulta informações em órgãos reguladores (stub)

        Args:
            orgao: Nome do órgão (ex: 'aneel')
            consulta: Tipo de consulta

        Returns:
            Resultado da consulta
        """
        self.logger.info(f"[STUB] Consultando {orgao} sobre {consulta}")

        return {
            "orgao": orgao,
            "consulta": consulta,
            "resultado": "consulta_simulada",
            "mensagem": "Esta é uma implementação temporária (stub) do HomologadorAgent",
            "timestamp": datetime.now().isoformat(),
        }


# Função auxiliar para criar instância do agente homologador
def create_homologador_agent(
    projeto_id: str,
    distribuidora_codigo: str,
    computer: Optional[Any] = None,
    model: str = "computer-use-preview",
) -> HomologadorAgent:
    """
    Cria uma instância do agente homologador configurada (stub)

    Args:
        projeto_id: ID do projeto
        distribuidora_codigo: Código da distribuidora
        computer: Instância do computador/navegador
        model: Modelo a ser usado

    Returns:
        Instância configurada do HomologadorAgent
    """
    return HomologadorAgent(
        model=model,
        computer=computer,
        projeto_id=projeto_id,
        distribuidora_codigo=distribuidora_codigo,
    )

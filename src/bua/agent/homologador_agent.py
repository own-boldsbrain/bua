"""
Agente Autônomo Homologador 360º
Personalização do agente para homologação de projetos de geração distribuída
com interação automatizada junto às concessionárias e órgãos responsáveis.
"""

from pydantic import BaseModel
from bua.computers.actions import ActionUnion
import logging
from bua.computers import Computer
from typing import Callable, List, Dict, Optional
from datetime import datetime

# Importações específicas do projeto Homologacao
from api.services.gd.distribuidoras_gd_service import DistribuidorasGDService


class ActionParse(BaseModel):
    action: ActionUnion


class Agent:
    """
    A sample agent class that can be used to interact with a computer.
    (Base class for specialized agents)
    """

    def __init__(
        self,
        model="computer-use-preview",
        computer: Optional[Computer] = None,
        tools: list[dict] = [],
        acknowledge_safety_check_callback: Callable = lambda: False,
    ):
        self.model = model
        self.computer = computer
        self.tools = tools
        self.print_steps = True
        self.debug = False
        self.show_images = False
        self.acknowledge_safety_check_callback = acknowledge_safety_check_callback
        self.usages: list[dict] = []

        if computer:
            dimensions = computer.get_dimensions()
            self.tools += [
                {
                    "type": "computer-preview",
                    "display_width": dimensions[0],
                    "display_height": dimensions[1],
                    "environment": computer.get_environment(),
                },
            ]

    def debug_print(self, *args):
        if self.debug:
            print(*args)

    def handle_item(self, item):
        """Handle each item; may cause a computer action + screenshot."""
        # Implementação básica - será sobrescrita nas subclasses
        return []

    def run_full_turn(
        self,
        input_items,
        print_steps=True,
        debug=False,
        show_images=False,
    ):
        """Base implementation for running a full turn"""
        self.print_steps = print_steps
        self.debug = debug
        self.show_images = show_images
        # Implementação básica
        return []


class HomologadorAgent(Agent):
    """
    Agente autônomo especializado em homologação 360º de projetos de GD.
    Interage automaticamente com portais de distribuidoras e órgãos
    responsáveis.
    """

    def __init__(
        self,
        model="computer-use-preview",
        computer: Optional[Computer] = None,
        tools: list[dict] = [],
        acknowledge_safety_check_callback: Callable = lambda: False,
        projeto_id: Optional[str] = None,
        distribuidora_codigo: Optional[str] = None,
    ):
        super().__init__(model, computer, tools, acknowledge_safety_check_callback)

        self.projeto_id = projeto_id
        self.distribuidora_codigo = distribuidora_codigo
        self.distribuidora_data = None
        self.homologacao_steps = []
        self.logger = logging.getLogger(__name__)

        # Carregar dados da distribuidora se especificado
        if distribuidora_codigo:
            self._load_distribuidora_data()

    def _load_distribuidora_data(self):
        """Carrega dados da distribuidora para personalizar as ações"""
        if not self.distribuidora_codigo:
            return

        try:
            service = DistribuidorasGDService()
            distribuidora = service.obter_distribuidora_por_codigo(
                self.distribuidora_codigo
            )
            if distribuidora:
                self.distribuidora_data = distribuidora.model_dump()
                self.logger.info(
                    f"Dados da distribuidora {self.distribuidora_codigo} "
                    "carregados"
                )
            else:
                self.logger.warning(
                    f"Distribuidora {self.distribuidora_codigo} não encontrada"
                )
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados da distribuidora: {e}")

    def _get_portal_url(self) -> Optional[str]:
        """Obtém a URL do portal de homologação da distribuidora"""
        if (self.distribuidora_data and
                "portal_homologacao" in self.distribuidora_data):
            portal = self.distribuidora_data["portal_homologacao"]
            return portal.get("url")
        return None

    def _get_autenticacao_info(self) -> Optional[Dict]:
        """Obtém informações de autenticação do portal"""
        if (self.distribuidora_data and
                "portal_homologacao" in self.distribuidora_data):
            portal = self.distribuidora_data["portal_homologacao"]
            return portal.get("autenticacao")
        return None

    def _get_documentos_requeridos(self) -> List[Dict]:
        """Obtém lista de documentos requeridos para homologação"""
        if (
            self.distribuidora_data
            and "documentos_requeridos" in self.distribuidora_data
        ):
            return self.distribuidora_data["documentos_requeridos"]
        return []

    def iniciar_homologacao(self, projeto_data: Dict) -> List[Dict]:
        """
        Inicia o processo de homologação para um projeto específico

        Args:
            projeto_data: Dados do projeto a ser homologado

        Returns:
            Lista de ações realizadas
        """
        self.logger.info(
            f"Iniciando homologação para projeto {self.projeto_id}"
        )

        # Etapa 1: Navegar para o portal da distribuidora
        portal_url = self._get_portal_url()
        if not portal_url:
            return [{
                "type": "error",
                "message": "URL do portal não encontrada para a distribuidora"
            }]

        # Etapa 2: Realizar autenticação se necessário
        auth_info = self._get_autenticacao_info()
        if auth_info:
            self._realizar_autenticacao(auth_info)

        # Etapa 3: Navegar para seção de homologação
        self._navegar_para_homologacao()

        # Etapa 4: Preencher formulário de solicitação
        self._preencher_formulario_solicitacao(projeto_data)

        # Etapa 5: Upload de documentos requeridos
        documentos = self._get_documentos_requeridos()
        self._upload_documentos(documentos, projeto_data)

        # Etapa 6: Submeter solicitação
        self._submeter_solicitacao()

        # Etapa 7: Acompanhar status
        status = self._acompanhar_status()

        return [{
            "type": "homologacao_iniciada",
            "projeto_id": self.projeto_id,
            "distribuidora": self.distribuidora_codigo,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }]

    def _realizar_autenticacao(self, auth_info: Dict):
        """Realiza autenticação no portal"""
        metodo = auth_info.get("metodo", "login_senha")

        if metodo == "login_senha":
            # Implementar login com usuário/senha
            self.logger.info("Realizando autenticação com login/senha")
            # Aqui seria implementada a lógica específica de cada portal
            pass
        elif metodo == "certificado_digital":
            # Implementar autenticação com certificado
            self.logger.info("Realizando autenticação com certificado digital")
            pass

    def _navegar_para_homologacao(self):
        """Navega para a seção de homologação do portal"""
        self.logger.info("Navegando para seção de homologação")
        # Implementar navegação específica
        pass

    def _preencher_formulario_solicitacao(self, projeto_data: Dict):
        """Preenche o formulário de solicitação de homologação"""
        self.logger.info("Preenchendo formulário de solicitação")
        # Implementar preenchimento de formulário
        pass

    def _upload_documentos(self, documentos: List[Dict], projeto_data: Dict):
        """Faz upload dos documentos requeridos"""
        self.logger.info(f"Fazendo upload de {len(documentos)} documentos")
        # Implementar upload de documentos
        pass

    def _submeter_solicitacao(self):
        """Submete a solicitação de homologação"""
        self.logger.info("Submetendo solicitação de homologação")
        # Implementar submissão
        pass

    def _acompanhar_status(self) -> str:
        """Acompanha o status da solicitação"""
        self.logger.info("Acompanhando status da solicitação")
        # Implementar acompanhamento
        return "em_analise"

    def consultar_orgao_regulador(self, orgao: str, consulta: str) -> Dict:
        """
        Consulta informações em órgãos reguladores (ANEEL, etc.)

        Args:
            orgao: Nome do órgão (ex: 'aneel')
            consulta: Tipo de consulta

        Returns:
            Resultado da consulta
        """
        self.logger.info(f"Consultando {orgao} sobre {consulta}")

        # Implementar consulta específica
        return {
            "orgao": orgao,
            "consulta": consulta,
            "resultado": "consulta_realizada",
            "timestamp": datetime.now().isoformat()
        }

    def run_full_turn(
        self,
        input_items,
        print_steps=True,
        debug=False,
        show_images=False,
    ):
        """Sobrescreve para adicionar lógica específica de homologação"""
        # Verificar se é uma solicitação de homologação
        for item in input_items:
            if item.get("type") == "homologacao_request":
                projeto_data = item.get("projeto_data", {})
                return self.iniciar_homologacao(projeto_data)
            elif item.get("type") == "consulta_orgao":
                orgao = item.get("orgao")
                consulta = item.get("consulta")
                return [self.consultar_orgao_regulador(orgao, consulta)]

        # Caso contrário, usar comportamento padrão
        return super().run_full_turn(
            input_items, print_steps, debug, show_images
        )


# Função auxiliar para criar instância do agente homologador
def create_homologador_agent(
    projeto_id: str,
    distribuidora_codigo: str,
    computer: Optional[Computer] = None,
    model: str = "computer-use-preview",
) -> HomologadorAgent:
    """
    Cria uma instância do agente homologador configurada

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
        distribuidora_codigo=distribuidora_codigo
    )

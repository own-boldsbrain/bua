"""
Integração com Temporal para gerenciamento de tarefas duráveis de homologação
"""
import logging
import os
import json
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta

# Import temporalio client
from temporalio.client import Client
from temporalio.common import RetryPolicy
from temporalio import workflow, activity

from api.core.config import settings
from api.models.homologacao_models import HomologacaoJobRequest, JobStatus
from services.bua.agent.homologador_agent import create_homologador_agent

# Configurar logger
logger = logging.getLogger(__name__)

# Define a duração máxima do workflow em 24 horas
WORKFLOW_MAX_DURATION = timedelta(hours=24)
# Define o tempo de retenção do histórico em 30 dias
WORKFLOW_RETENTION = timedelta(days=30)

# Define a política de retry (tentativas 3x, começando com 1s, dobra a cada retry, timeout 30min)
DEFAULT_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=10),
    maximum_attempts=3,
    non_retryable_error_types=["ValueError", "KeyError"]
)


# Definição das atividades
@activity.defn
async def iniciar_homologacao_activity(projeto_id: str, distribuidora_codigo: str, 
                                       projeto_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Atividade que inicia o processo de homologação
    
    Args:
        projeto_id: ID do projeto
        distribuidora_codigo: Código da distribuidora
        projeto_data: Dados adicionais do projeto
        
    Returns:
        Resultado da ação de homologação
    """
    logger.info(f"Iniciando homologação para projeto {projeto_id} na distribuidora {distribuidora_codigo}")
    
    try:
        # Criar agente homologador
        agent = create_homologador_agent(
            projeto_id=projeto_id,
            distribuidora_codigo=distribuidora_codigo
        )
        
        # Executar homologação
        result = agent.iniciar_homologacao(projeto_data)
        
        return {
            "status": "completed",
            "actions": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao iniciar homologação: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@activity.defn
async def consultar_status_homologacao_activity(projeto_id: str, 
                                                distribuidora_codigo: str) -> Dict[str, Any]:
    """
    Atividade que consulta o status de um processo de homologação
    
    Args:
        projeto_id: ID do projeto
        distribuidora_codigo: Código da distribuidora
        
    Returns:
        Status atual da homologação
    """
    logger.info(f"Consultando status de homologação para projeto {projeto_id}")
    
    try:
        # Criar agente homologador
        agent = create_homologador_agent(
            projeto_id=projeto_id,
            distribuidora_codigo=distribuidora_codigo
        )
        
        # Em uma implementação real, consultaria API da distribuidora
        # Aqui estamos simulando
        return {
            "status": "em_analise",
            "mensagem": "Processo em análise pela distribuidora",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao consultar status: {e}")
        return {
            "status": "erro_consulta",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@activity.defn
async def submeter_documentos_activity(projeto_id: str, 
                                      distribuidora_codigo: str,
                                      documentos: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Atividade que submete documentos adicionais para um processo de homologação
    
    Args:
        projeto_id: ID do projeto
        distribuidora_codigo: Código da distribuidora
        documentos: Lista de documentos a submeter
        
    Returns:
        Resultado da submissão
    """
    logger.info(f"Submetendo {len(documentos)} documentos para o projeto {projeto_id}")
    
    try:
        # Criar agente homologador
        agent = create_homologador_agent(
            projeto_id=projeto_id,
            distribuidora_codigo=distribuidora_codigo
        )
        
        # Em uma implementação real, enviaria os documentos
        # Aqui estamos simulando
        return {
            "status": "enviado",
            "documentos_enviados": len(documentos),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao submeter documentos: {e}")
        return {
            "status": "falha_envio",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# Definição do workflow de homologação
@workflow.defn
class HomologacaoWorkflow:
    """
    Workflow para gerenciar o processo completo de homologação de um projeto
    """

    @workflow.run
    async def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o workflow de homologação
        
        Args:
            request: Dados do job de homologação
            
        Returns:
            Resultado final do workflow
        """
        projeto_id = request["projeto_id"]
        distribuidora_codigo = request["distribuidora_codigo"]
        projeto_data = request.get("projeto_data", {})
        
        logger.info(f"Iniciando workflow de homologação para {projeto_id}")
        
        # Registrar etapas do workflow
        steps = []
        
        # Etapa 1: Iniciar homologação
        steps.append({
            "step": "iniciar_homologacao",
            "status": "iniciado",
            "timestamp": datetime.now().isoformat()
        })
        
        resultado_inicio = await workflow.execute_activity(
            iniciar_homologacao_activity,
            projeto_id, 
            distribuidora_codigo, 
            projeto_data,
            start_to_close_timeout=timedelta(minutes=30),
            retry_policy=DEFAULT_RETRY_POLICY
        )
        
        if resultado_inicio["status"] == "failed":
            steps.append({
                "step": "iniciar_homologacao",
                "status": "falhou",
                "timestamp": datetime.now().isoformat(),
                "error": resultado_inicio["error"]
            })
            
            return {
                "job_id": workflow.info().workflow_id,
                "status": JobStatus.FAILED.value,
                "steps": steps,
                "error": resultado_inicio["error"]
            }
        
        steps.append({
            "step": "iniciar_homologacao",
            "status": "concluido",
            "timestamp": datetime.now().isoformat(),
            "result": resultado_inicio
        })
        
        # Etapa 2: Consultar status (poderia ser um timer para consultas periódicas)
        # Em um cenário real, isso poderia ser um loop com sleep
        steps.append({
            "step": "consultar_status",
            "status": "iniciado",
            "timestamp": datetime.now().isoformat()
        })
        
        resultado_consulta = await workflow.execute_activity(
            consultar_status_homologacao_activity,
            projeto_id,
            distribuidora_codigo,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=DEFAULT_RETRY_POLICY
        )
        
        steps.append({
            "step": "consultar_status",
            "status": "concluido",
            "timestamp": datetime.now().isoformat(),
            "result": resultado_consulta
        })
        
        # Workflow concluído
        return {
            "job_id": workflow.info().workflow_id,
            "status": JobStatus.COMPLETED.value,
            "projeto_id": projeto_id,
            "distribuidora_codigo": distribuidora_codigo,
            "steps": steps,
            "result": {
                "inicio": resultado_inicio,
                "status": resultado_consulta
            }
        }


# Cliente Temporal como singleton
_temporal_client = None

async def get_temporal_client() -> Client:
    """
    Obtém ou cria um cliente Temporal
    
    Returns:
        Cliente Temporal
    """
    global _temporal_client
    
    if _temporal_client is None:
        # Configurar conexão com o Temporal Server
        temporal_host = os.environ.get("TEMPORAL_HOST", "localhost")
        temporal_port = os.environ.get("TEMPORAL_PORT", "7233")
        
        # Criar cliente
        _temporal_client = await Client.connect(f"{temporal_host}:{temporal_port}")
        
        logger.info(f"Conectado ao Temporal Server em {temporal_host}:{temporal_port}")
    
    return _temporal_client


async def iniciar_homologacao_workflow(request: HomologacaoJobRequest) -> str:
    """
    Inicia um workflow de homologação no Temporal
    
    Args:
        request: Dados do job de homologação
        
    Returns:
        ID do workflow
    """
    # Obter cliente Temporal
    client = await get_temporal_client()
    
    # Gerar ID do workflow (usar UUID ou projeto_id + timestamp)
    workflow_id = f"homologacao-{request.projeto_id}-{int(datetime.now().timestamp())}"
    
    # Iniciar workflow
    await client.start_workflow(
        HomologacaoWorkflow.run,
        request.model_dump(),
        id=workflow_id,
        task_queue="homologacao",
        # Usar workflow_id como ID da execução para idempotência
        execution_id=workflow_id,
        # Não usar FIFO para permitir execução paralela de workflows diferentes
        fifo=False,
        retention_period=WORKFLOW_RETENTION,
    )
    
    logger.info(f"Workflow de homologação iniciado: {workflow_id}")
    
    return workflow_id


async def consultar_homologacao_workflow(workflow_id: str) -> Optional[Dict[str, Any]]:
    """
    Consulta o status de um workflow de homologação no Temporal
    
    Args:
        workflow_id: ID do workflow
        
    Returns:
        Resultado do workflow ou None se não encontrado
    """
    # Obter cliente Temporal
    client = await get_temporal_client()
    
    try:
        # Consultar workflow
        handle = client.get_workflow_handle(workflow_id)
        
        # Verificar se o workflow existe e seu estado
        result = await handle.query("getStatus")
        
        return result
    except Exception as e:
        logger.error(f"Erro ao consultar workflow {workflow_id}: {e}")
        return None


async def cancelar_homologacao_workflow(workflow_id: str, motivo: str) -> bool:
    """
    Cancela um workflow de homologação em execução no Temporal
    
    Args:
        workflow_id: ID do workflow
        motivo: Motivo do cancelamento
        
    Returns:
        True se cancelado com sucesso, False caso contrário
    """
    # Obter cliente Temporal
    client = await get_temporal_client()
    
    try:
        # Obter handle do workflow
        handle = client.get_workflow_handle(workflow_id)
        
        # Cancelar workflow com motivo
        await handle.cancel(reason=motivo)
        
        logger.info(f"Workflow {workflow_id} cancelado: {motivo}")
        
        return True
    except Exception as e:
        logger.error(f"Erro ao cancelar workflow {workflow_id}: {e}")
        return False
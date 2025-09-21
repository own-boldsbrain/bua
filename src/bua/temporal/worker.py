"""
Módulo principal para executar o worker do Temporal.
"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Importe as atividades e workflows
from bua.temporal.homologacao_workflow import (
    HomologacaoWorkflow,
    iniciar_homologacao_activity,
    consultar_status_homologacao_activity,
    submeter_documentos_activity,
    enviar_notificacao_listmonk_activity,
)


async def main():
    """Conecta ao servidor Temporal e inicia o worker."""
    # Conecte ao servidor Temporal
    client = await Client.connect("temporal:7233", namespace="homologacao")

    # Crie um worker que escuta na task queue "homologacao"
    worker = Worker(
        client,
        task_queue="homologacao",
        workflows=[HomologacaoWorkflow],
        activities=[
            iniciar_homologacao_activity,
            consultar_status_homologacao_activity,
            submeter_documentos_activity,
            enviar_notificacao_listmonk_activity,
        ],
    )

    print("Iniciando o worker do Temporal...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

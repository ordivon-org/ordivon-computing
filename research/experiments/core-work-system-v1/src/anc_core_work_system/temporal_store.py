from __future__ import annotations

import asyncio
from importlib.metadata import version
from pathlib import Path
from typing import Any

from temporalio import workflow
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from .model import WorkState


@workflow.defn
class DurableWorkStateWorkflow:
    """Temporal baseline: application work semantics live as ordinary Workflow state."""

    def __init__(self) -> None:
        self.state: dict[str, Any] = {}
        self.done = False

    @workflow.run
    async def run(self, initial: dict[str, Any]) -> dict[str, Any]:
        self.state = initial
        await workflow.wait_condition(lambda: self.done)
        return self.state

    @workflow.update
    def save(self, state: dict[str, Any]) -> dict[str, Any]:
        self.state = state
        return self.state

    @workflow.query
    def load(self) -> dict[str, Any]:
        return self.state

    @workflow.signal
    def finish(self) -> None:
        self.done = True


async def temporal_restart_roundtrip(
    initial: WorkState,
    checkpoint: WorkState,
    *,
    workflow_id: str,
    download_dir: str | Path,
) -> tuple[WorkState, dict[str, object]]:
    cache = Path(download_dir)
    cache.mkdir(parents=True, exist_ok=True)
    async with await WorkflowEnvironment.start_time_skipping(download_dest_dir=str(cache)) as env:
        task_queue = f"round1-{workflow_id.replace(':', '-')}"
        first_worker = Worker(
            env.client,
            task_queue=task_queue,
            workflows=[DurableWorkStateWorkflow],
            max_cached_workflows=0,
        )
        first_task = asyncio.create_task(first_worker.run())
        handle = await env.client.start_workflow(
            DurableWorkStateWorkflow.run,
            initial.to_dict(),
            id=workflow_id,
            task_queue=task_queue,
        )
        await handle.execute_update(DurableWorkStateWorkflow.save, checkpoint.to_dict())
        before_restart = await handle.query(DurableWorkStateWorkflow.load)
        await first_worker.shutdown()
        await first_task

        second_worker = Worker(
            env.client,
            task_queue=task_queue,
            workflows=[DurableWorkStateWorkflow],
            max_cached_workflows=0,
        )
        second_task = asyncio.create_task(second_worker.run())
        after_restart = await handle.query(DurableWorkStateWorkflow.load)
        await handle.signal(DurableWorkStateWorkflow.finish)
        terminal = await handle.result()
        await second_worker.shutdown()
        await second_task

    recovered = WorkState.from_dict(after_restart)
    return recovered, {
        "temporalioVersion": version("temporalio"),
        "beforeRestartDigest": WorkState.from_dict(before_restart).digest,
        "afterRestartDigest": recovered.digest,
        "terminalDigest": WorkState.from_dict(terminal).digest,
        "workerRestarted": True,
    }

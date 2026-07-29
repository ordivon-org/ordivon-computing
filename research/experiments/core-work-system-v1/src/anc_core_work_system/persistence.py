from __future__ import annotations

from pathlib import Path
import json
import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .model import WorkState, canonical_bytes
from .scenario import state_from_summary


class JsonStateStore:
    """Typed durable state used by the Ordivon-style deterministic variant."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: WorkState) -> None:
        envelope = {
            "schemaVersion": 1,
            "kind": "anc.typed-work-state-envelope",
            "stateDigest": state.digest,
            "state": state.to_dict(),
        }
        self.path.write_bytes(canonical_bytes(envelope) + b"\n")

    def load(self) -> WorkState:
        value = json.loads(self.path.read_text("utf-8"))
        if set(value) != {"schemaVersion", "kind", "stateDigest", "state"}:
            raise ValueError("typed state envelope fields differ")
        state = WorkState.from_dict(value["state"])
        if state.digest != value["stateDigest"]:
            raise ValueError("typed state digest differs")
        return state

    @property
    def byte_length(self) -> int:
        return self.path.stat().st_size


class TranscriptSummaryStore:
    """Bounded rolling-summary baseline with the raw transcript retained for audit only."""

    def __init__(self, root: str | Path, *, omit_pending_on_summary: bool) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.omit_pending_on_summary = omit_pending_on_summary
        self.transcript_path = self.root / "transcript.jsonl"
        self.summary_path = self.root / "summary.json"

    def save(self, state: WorkState, events: list[dict[str, object]]) -> None:
        with self.transcript_path.open("a", encoding="utf-8") as stream:
            for event in events:
                stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        summary = state_from_summary(
            state,
            omit_pending_operation=self.omit_pending_on_summary,
        )
        envelope = {
            "schemaVersion": 1,
            "kind": "anc.rolling-summary",
            "summaryDigest": summary.digest,
            "state": summary.to_dict(),
            "rawTranscriptUsedForResume": False,
        }
        self.summary_path.write_bytes(canonical_bytes(envelope) + b"\n")

    def load_for_resume(self) -> WorkState:
        value = json.loads(self.summary_path.read_text("utf-8"))
        state = WorkState.from_dict(value["state"])
        if state.digest != value["summaryDigest"]:
            raise ValueError("rolling summary digest differs")
        return state

    @property
    def byte_length(self) -> int:
        return self.transcript_path.stat().st_size + self.summary_path.stat().st_size


class _GraphState(TypedDict):
    work_state: dict[str, object]


def _persist_node(state: _GraphState) -> _GraphState:
    return state


class LangGraphStateStore:
    """Actual LangGraph thread/checkpoint persistence backed by SQLite."""

    def __init__(self, path: str | Path, *, thread_id: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.thread_id = thread_id
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.saver = SqliteSaver(self.connection)
        builder = StateGraph(_GraphState)
        builder.add_node("persist", _persist_node)
        builder.add_edge(START, "persist")
        builder.add_edge("persist", END)
        self.graph = builder.compile(checkpointer=self.saver)
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def save(self, state: WorkState) -> None:
        self.graph.invoke({"work_state": state.to_dict()}, self.config)

    def load(self) -> WorkState:
        snapshot = self.graph.get_state(self.config)
        value = snapshot.values.get("work_state")
        if not isinstance(value, dict):
            raise ValueError("LangGraph checkpoint omitted work_state")
        return WorkState.from_dict(value)

    def close(self) -> None:
        self.connection.close()

    @property
    def byte_length(self) -> int:
        self.connection.commit()
        return self.path.stat().st_size


def dependency_identity() -> dict[str, str]:
    from importlib.metadata import version

    return {
        "langgraph": version("langgraph"),
        "langgraph-checkpoint-sqlite": version("langgraph-checkpoint-sqlite"),
    }

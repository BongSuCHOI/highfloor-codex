from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias


Json: TypeAlias = str | int | float | bool | None | list["Json"] | dict[str, "Json"]
JsonMap: TypeAlias = dict[str, Json]


@dataclass(frozen=True, slots=True)
class Options:
    platforms: frozenset[str]
    roots: tuple[Path, ...]
    queries: tuple[str, ...]
    date_from: str | None
    date_to: str | None
    cwd: str | None
    model: str | None
    reasoning_effort: str | None
    limit: int
    workers: int
    include_subagents: bool
    include_internal: bool


@dataclass(frozen=True, slots=True)
class Session:
    platform: str
    id: str
    path: str
    cwd: str | None
    created_at: str | None
    updated_at: str | None
    provider: str | None
    model: str | None
    first_user_message: str
    usage: JsonMap
    parent_id: str | None = None
    agent: str | None = None
    last_user_message: str = ""
    models: tuple[str, ...] = ()
    reasoning_efforts: tuple[str, ...] = ()
    internal: bool = False
    internal_kind: str | None = None

    def to_json(self) -> JsonMap:
        return {
            "platform": self.platform,
            "id": self.id,
            "path": self.path,
            "cwd": self.cwd,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "provider": self.provider,
            "model": self.model,
            "models": list(self.models or ((self.model,) if self.model else ())),
            "reasoning_efforts": list(self.reasoning_efforts),
            "first_user_message": self.first_user_message[:300],
            "last_user_message": (self.last_user_message or self.first_user_message)[:300],
            "usage": self.usage,
            "parent_id": self.parent_id,
            "agent": self.agent,
            "internal": self.internal,
            "internal_kind": self.internal_kind,
        }


"""Pydantic schemas for the pivot service."""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Scale(str, Enum):
    TEXTUAL = "TEXTUAL"
    CHRONOLOGICAL = "CHRONOLOGICAL"


class PivotIn(BaseModel):
    text_section: str
    scale: Scale = Scale.TEXTUAL
    lens: List[str] = Field(default_factory=list)


class PivotPoint(BaseModel):
    detector: str
    position: int
    score: float


class PivotOut(BaseModel):
    text_section: str
    scale: Scale
    points: List[PivotPoint]


class ForecastRequest(BaseModel):
    user_id: str
    horizon: int = 30


class ForecastPoint(BaseModel):
    timestep: int
    probability: float

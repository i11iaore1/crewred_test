from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator
class PlaceBase(BaseModel):
    external_id: int
    notes: str | None = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: str | None = None
    is_visited: bool | None = None


class PlaceRead(PlaceBase):
    id: int
    project_id: int
    is_visited: bool

    model_config = ConfigDict(from_attributes=True)


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    start_date: date | None = None


class ProjectCreate(ProjectBase):
    places: List[PlaceCreate] | None = Field(default=[], max_length=10)

    @field_validator("places")
    @classmethod
    def validate_places_limit(cls, v):
        if v is None:
            return v
        if len(v) > 10:
            raise ValueError("A project cannot have more than 10 places.")

        external_ids = [p.external_id for p in v]
        if len(external_ids) != len(set(external_ids)):
            raise ValueError(
                "Duplicate external IDs in the same project are not allowed."
            )
        return v


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


class ProjectRead(ProjectBase):
    id: int
    is_completed: bool
    places: List[PlaceRead] = []

    model_config = ConfigDict(from_attributes=True)

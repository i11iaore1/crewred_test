from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        columns = [
            f"{column_name}={getattr(self, column_name)}"
            for column_name in self.__table__.columns.keys()
        ]
        return f"<{self.__class__.__name__} {', '.join(columns)}>"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str | None]
    start_date: Mapped[date | None]
    is_completed: Mapped[bool] = mapped_column(default=False)

    places: Mapped[list["Place"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Place(Base):
    __tablename__ = "places"

    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_project_place"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[int] = mapped_column(index=True)
    notes: Mapped[str | None]
    is_visited: Mapped[bool] = mapped_column(default=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    project: Mapped["Project"] = relationship(back_populates="places")

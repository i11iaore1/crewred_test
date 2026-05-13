import contextlib
from typing import List

from fastapi import FastAPI, HTTPException, status

from . import database, models, schemas, services

APP_VERSION = "v1"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Travel Planner API",
    version=APP_VERSION,
    description="REST API for planning trips and collecting desired places to visit",
)

@app.post(
    "/projects",
    response_model=schemas.ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(project: schemas.ProjectCreate, db: database.SessionDep):
    if project.places:
        place_ids = [p.external_id for p in project.places]
        is_valid = await services.are_valid_place_ids(place_ids)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more place external IDs are invalid.",
            )

    db_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date,
    )

    if project.places:
        for p in project.places:
            db_place = models.Place(
                external_id=p.external_id,
                notes=p.notes,
            )
            db_project.places.append(db_place)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@app.get("/projects", response_model=List[schemas.ProjectRead])
def list_projects(db: database.SessionDep, offset: int = 0, limit: int = 100):
    projects = db.query(models.Project).offset(offset).limit(limit).all()
    return projects


@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: database.SessionDep):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@app.patch("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: database.SessionDep,
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: database.SessionDep):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if any(place.is_visited for place in project.places):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a project if any of its places are already marked as visited.",
        )

    db.delete(project)
    db.commit()


@app.post(
    "/projects/{project_id}/places",
    response_model=schemas.PlaceRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_place_to_project(
    project_id: int, place: schemas.PlaceCreate, db: database.SessionDep
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if len(project.places) >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A project cannot have more than 10 places.",
        )

    if any(p.external_id == place.external_id for p in project.places):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This place is already in the project.",
        )

    is_valid = await services.are_valid_place_ids([place.external_id])
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid place external ID.",
        )

    db_place = models.Place(
        external_id=place.external_id,
        notes=place.notes,
        project_id=project_id,
    )
    db.add(db_place)

    project.is_completed = False

    db.commit()
    db.refresh(db_place)

    return db_place


@app.get("/projects/{project_id}/places", response_model=List[schemas.PlaceRead])
def list_places_for_project(
    project_id: int, db: database.SessionDep, offset: int = 0, limit: int = 100
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    places = (
        db.query(models.Place)
        .filter(models.Place.project_id == project_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return places


@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceRead)
def get_place(project_id: int, place_id: int, db: database.SessionDep):
    place = (
        db.query(models.Place)
        .filter(models.Place.project_id == project_id, models.Place.id == place_id)
        .first()
    )
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found in this project",
        )
    return place


@app.patch("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceRead)
def update_place(
    project_id: int,
    place_id: int,
    place_update: schemas.PlaceUpdate,
    db: database.SessionDep,
):
    place = (
        db.query(models.Place)
        .filter(models.Place.project_id == project_id, models.Place.id == place_id)
        .first()
    )
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found in this project",
        )

    update_data = place_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(place, key, value)

    project = place.project
    if project.places:
        project.is_completed = all(p.is_visited for p in project.places)

    db.commit()
    db.refresh(place)
    return place

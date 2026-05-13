import contextlib
from typing import List

from fastapi import FastAPI, status

from . import database, models, schemas

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


# --- PROJECTS ---


@app.post(
    "/projects",
    response_model=schemas.ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(project: schemas.ProjectCreate, db: database.SessionDep):
    pass


@app.get("/projects", response_model=List[schemas.ProjectRead])
def list_projects(db: database.SessionDep):
    pass


@app.get("/projects/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: database.SessionDep):
    pass


@app.patch("/projects/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: database.SessionDep,
):
    pass


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: database.SessionDep):
    pass


# --- PLACES ---


@app.post(
    "/projects/{project_id}/places",
    response_model=schemas.PlaceRead,
    status_code=status.HTTP_201_CREATED,
)
def add_place_to_project(
    project_id: int, place: schemas.PlaceCreate, db: database.SessionDep
):
    pass


@app.get("/projects/{project_id}/places", response_model=List[schemas.PlaceRead])
def list_places_for_project(project_id: int, db: database.SessionDep):
    pass


@app.get("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceRead)
def get_place(project_id: int, place_id: int, db: database.SessionDep):
    pass


@app.patch("/projects/{project_id}/places/{place_id}", response_model=schemas.PlaceRead)
def update_place(
    project_id: int,
    place_id: int,
    place_update: schemas.PlaceUpdate,
    db: database.SessionDep,
):
    pass

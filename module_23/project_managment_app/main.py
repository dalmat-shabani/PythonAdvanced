from fastapi import FastAPI
from models import Developer, Project

app = FastAPI()

@app.post("/developers/")
def create_developer(developer: Developer):
    return {"message": "Developer created successfully", "developer":developer}

@app.post("/projects/")
def create_project(project: Project):
    return {"message": "Project created successfully", "project":project}


@app.get("/project/")
def get_projects():
    sample_project = Project(
        title="Sample Project",
        description="Sample description",
        languages=["Python", "JavaScript"],
        lead_developer=Developer(name="Jane Doe", experience = 5),

    )
    return {"projects": sample_project}
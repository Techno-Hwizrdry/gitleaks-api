from config import Settings
from fastapi import Body, Depends, FastAPI
from functools import lru_cache
from gitleaks import GitLeaks
from typing import Dict
from typing_extensions import Annotated

app = FastAPI()

@lru_cache
def get_settings() -> Settings:
    return Settings()


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]) -> Dict:
    return {"message": f"Hello World {settings}"}

@app.post("/detection")
async def detect(
    settings: Annotated[Settings, Depends(get_settings)],
    repo: str = Body(...)) -> Dict:
    gl = GitLeaks(settings.gitleaks_path)
    print(repo)
    return gl.detect(repo)

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src import config
from src.tasks.router import tasks_router

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    version=config.settings.VERSION,
    description=config.settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
)
app.include_router(tasks_router, prefix="")


# Guards against HTTP Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.settings.ALLOWED_HOSTS)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.assistant import router as asst_router
from api.routes.chunk import router as chunk_router
from api.routes.document import router as doc_router
from api.routes.kb import router as kb_router
from api.routes.llm import router as llm_router
from api.routes.user import router as user_router
from core.config import settings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(kb_router, prefix="/kb", tags=["kb"])
app.include_router(doc_router, prefix="/document", tags=["document"])
app.include_router(chunk_router, prefix="/chunk", tags=["chunk"])
app.include_router(llm_router, prefix="/llm", tags=["llm"])
app.include_router(asst_router, prefix="/assistant", tags=["assistant"])

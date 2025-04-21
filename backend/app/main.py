import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# OpenTelemetry setup
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from api.routes.assistant import router as asst_router
from api.routes.chunk import router as chunk_router
from api.routes.document import router as doc_router
from api.routes.kb import router as kb_router
from api.routes.llm import router as llm_router
from api.routes.metrics import router as metrics_router
from api.routes.user import router as user_router
from app.api.routes.health import router as health_router
from core.config import settings


# Configure structured JSON logging with Loguru & inject OTEL trace/span IDs
def inject_trace_context(record):
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if ctx.is_valid:
        record["extra"]["trace_id"] = f"{ctx.trace_id:032x}"
        record["extra"]["span_id"] = f"{ctx.span_id:016x}"


logger.remove()
logger.add(
    sys.stdout,
    serialize=True,
    level=settings.LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    enqueue=True,
    patch=inject_trace_context,
)

# configure tracer provider
resource = Resource(attributes={"service.name": "backend-service"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

app = FastAPI()

# instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

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
app.include_router(metrics_router)
app.include_router(health_router)

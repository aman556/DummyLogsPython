import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "containers",
            "service.instance.id": "93a0d54b079a",
        }
    ),
)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)

# Log directly
logging.info("Debugging the container with id 93a0d54b079a.")

# Create different namespaced loggers
logger1 = logging.getLogger("myapp.area1")
logger2 = logging.getLogger("myapp.area2")

logger1.debug("Debugging container")
logger1.info("container_id: 93a0d54b079a")
logger2.warning("Name is not allocated to the container")
logger2.error("pip command not present")


# Trace context correlation
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("Container_Logs"):
    # Do something
    logger2.error("Install the pip command.")

logger_provider.shutdown()

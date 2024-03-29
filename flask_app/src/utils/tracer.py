from opentelemetry import _metrics
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from utils.settings import get_settings

jaeger_settings = get_settings()
jaeger_host = jaeger_settings.JAEGER_HOST
jaeger_port = jaeger_settings.JAEGER_PORT
TRACING = jaeger_settings.TRACING

resource = Resource(attributes={
    SERVICE_NAME: 'Auth_API'
})


def configure_tracer() -> None:
    # Sets the global default tracer provider
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                # agent_host_name='localhost',
                agent_host_name=jaeger_host,
                agent_port=int(jaeger_port),
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

configure_tracer()

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

# To start collecting metrics, you’ll need to initialize a MeterProvider
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])

# Sets the global default meter provider
_metrics.set_meter_provider(provider)

# Creates a meter from the global meter provider
meter = _metrics.get_meter(__name__)


def conditional_tracer(decorator):
    def tracer_decorator(func):
        if not TRACING:
            return func
        return decorator(func)
    return tracer_decorator

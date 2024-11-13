import os
import base64
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import Compression
from opentelemetry.sdk.resources import SERVICE_NAME, DEPLOYMENT_ENVIRONMENT, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from src.Utils.OpenTelemetry.config import oTelConfig as Config


if Config.trace_config_provided():

    trace_resource = Resource.create(
        attributes={
            SERVICE_NAME: "THDc-Backend",
            DEPLOYMENT_ENVIRONMENT: Config.environment,
        }
    )
    trace.set_tracer_provider(TracerProvider(resource=trace_resource))

    # OTLP Exporter
    otlp_exporter: OTLPSpanExporter = OTLPSpanExporter(
        endpoint=Config.url,
        headers=Config.get_auth_header(),
        insecure=False,
    )
    tracer_provider: TracerProvider = trace.get_tracer_provider()
    span_processor: BatchSpanProcessor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)


def instrument_fastapi(app):
    (FastAPIInstrumentor().instrument_app(app))


def instrument_sqlalchemy(engine):
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
    )


def get_trace_id() -> str:
    current_span = trace.get_current_span()
    trace_id = current_span.get_span_context().trace_id
    if trace_id == 0:
        str_trace_id = None
    else:
        str_trace_id = "{trace:032x}".format(trace=trace_id)

    return str_trace_id


def get_span_id() -> str:
    current_span = trace.get_current_span()
    span_id = current_span.get_span_context().span_id

    if span_id == 0:
        str_span_id = None
    else:
        str_span_id = "{span:016x}".format(span=span_id)

    return str_span_id


def get_response_headers() -> dict[str, str]:
    return {"trace_id": get_trace_id()}

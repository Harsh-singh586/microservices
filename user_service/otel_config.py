"""
OpenTelemetry Configuration for User_Service
Enhanced configuration with explicit database resource attributes
"""

import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def configure_opentelemetry():
    """Configure OpenTelemetry with explicit database resource attributes"""
    
    # Create resource with database-specific attributes
    resource = Resource.create({
        "service.name": "user_service",
        "service.version": "1.0.0",
        "service.instance.id": f"user_service-{os.getpid()}",
        "deployment.environment": "development",
        "db.system": "sqlite",
        "db.name": "user_service_db",
        "db.connection_string": "sqlite:///db_user_service.sqlite3",
        "db.namespace": "user_service_namespace",
        "db.operation": "select,insert,update,delete",
        "service.namespace": "microservices",
        "telemetry.sdk.name": "opentelemetry",
        "telemetry.sdk.language": "python",
        "telemetry.sdk.version": "1.20.0",
    })
    
    # Configure tracer provider with resource
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer_provider = trace.get_tracer_provider()
    
    # Configure OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",
        headers={"service-name": "user_service"},
    )
    
    # Add span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Instrument frameworks
    DjangoInstrumentor().instrument()
    SQLite3Instrumentor().instrument()
    RequestsInstrumentor().instrument()
    
    print(f"🔧 OpenTelemetry configured for user_service")
    print(f"📊 Database: user_service_db")
    print(f"🌐 Endpoint: http://localhost:4318/v1/traces")
    
    return tracer_provider

# Auto-configure when imported
if __name__ != "__main__":
    configure_opentelemetry()

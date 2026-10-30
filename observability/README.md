# Observability

OpenTelemetry collector configuration and future Grafana, Prometheus, Loki,
and Tempo configuration will live here as those capabilities are introduced.

Keep runnable configurations here and human instructions under `docs/`:

- [Architecture proposal](../docs/architecture/observability.md)
- [Planned local setup](../docs/setup/observability.md)

No component configuration exists yet. The proposed services will use an
optional profile in the existing root Compose file, preserving PostgreSQL.

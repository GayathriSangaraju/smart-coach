# Run PostgreSQL with Docker

The root [`compose.yaml`](../../compose.yaml) defines the project's local
PostgreSQL service. You do not need to install PostgreSQL directly on your
computer.

## Configure the database

From the repository root, copy the example environment file:

```powershell
Copy-Item .env.example .env
```

On macOS or Linux, use:

```bash
cp .env.example .env
```

The defaults create this local database:

| Setting | Default |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | `unshaken_smart_coach` |
| Username | `unshaken` |
| Password | `change-me-for-local-development` |

Change the password in `.env` if desired. The `.env` file is ignored by Git;
never commit real credentials. The checked-in `.env.example` contains only
development placeholders.

## Start and verify PostgreSQL

```text
docker compose up -d postgres
docker compose ps
docker compose logs postgres
```

The service should eventually report `healthy`. Test it from inside the
container:

```text
docker compose exec postgres psql -U unshaken -d unshaken_smart_coach -c "SELECT version();"
```

If you changed the username or database in `.env`, use those values in the
command.

## Stop PostgreSQL

Stop the container while preserving its database volume:

```text
docker compose down
```

`docker compose down -v` also deletes the local database volume and all of its
data. Use it only when you intentionally want a fresh database.

## Environment changes after first startup

The official PostgreSQL image uses `POSTGRES_DB`, `POSTGRES_USER`, and
`POSTGRES_PASSWORD` only when initializing an empty data directory. Editing
those values later does not modify an existing database. Either make the
change through SQL/migrations or deliberately recreate the development volume.

See the [official PostgreSQL image documentation][postgres-image] for image
configuration details.

[postgres-image]: https://hub.docker.com/_/postgres

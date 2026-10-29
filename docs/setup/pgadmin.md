# Install pgAdmin and connect to local PostgreSQL

pgAdmin is an optional graphical PostgreSQL administration tool. PostgreSQL
continues to run inside Docker; pgAdmin is only a client.

## Install pgAdmin

1. Download pgAdmin from the [official download page][pgadmin-download].
2. Select your operating system and install the desktop application.
3. Open pgAdmin. If prompted, choose a master password to protect saved server
   passwords on your computer.

## Register the Docker database

Make sure the database is running:

```text
docker compose up -d postgres
```

In pgAdmin:

1. Right-click **Servers** and select **Register > Server**.
2. On the **General** tab, enter `UNShaken Local` as the name.
3. On the **Connection** tab, enter:

   | Field | Value |
   |---|---|
   | Host name/address | `localhost` |
   | Port | `5432` (or `POSTGRES_PORT` from `.env`) |
   | Maintenance database | `unshaken_smart_coach` |
   | Username | `unshaken` |
   | Password | The `POSTGRES_PASSWORD` value from `.env` |

4. Optionally select **Save password** for local development.
5. Select **Save**.

The database should appear under **Servers > UNShaken Local > Databases**.

These host settings apply to the pgAdmin desktop application. If pgAdmin is
later run as another Compose service, it must connect to host `postgres` (the
Compose service name), not `localhost`.

## Troubleshooting

- Confirm that `docker compose ps` reports PostgreSQL as healthy.
- Confirm that the host port in `.env` matches the pgAdmin port.
- Check `docker compose logs postgres` for initialization or authentication
  errors.
- If port `5432` is already in use, set `POSTGRES_PORT=5433` in `.env`, restart
  Compose, and use port `5433` in pgAdmin.
- Credentials changed after the database was first initialized do not update
  the existing database automatically; see the PostgreSQL setup guide.

See pgAdmin's [official connection documentation][pgadmin-connect] for more
details.

[pgadmin-download]: https://www.pgadmin.org/download/
[pgadmin-connect]: https://www.pgadmin.org/docs/pgadmin4/latest/connecting.html

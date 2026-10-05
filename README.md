# Run EmergenSee locally

Install and open Docker Desktop. No host Node.js, Python, or PostgreSQL installation is required.

From this folder:

```sh
docker compose up -d --build
```

The first run downloads dependencies. The backend trains its models before opening the API ports.
Check readiness with `docker compose ps` (backend should be healthy) and view logs with
`docker compose logs -f backend frontend`.

Open http://localhost:4200.

| Role | Email | Password |
| --- | --- | --- |
| Doctor | doctor1@example.com | password1 |
| Admin | admin1@example.com | password1 |

A fictional Demo Patient is provided for the doctor account.

Stop with `docker compose stop`; resume with `docker compose up -d`.
After editing code, rebuild with `docker compose up -d --build`.
Database records and uploaded patient images persist in Docker volumes.
The database initialization script runs only when the database volume is first created.

The UI uses port 4200 and APIs use ports 8001–8011, bound only to this computer.
The database is accessible only inside the Compose network.

## Checks

```sh
docker compose exec backend python -m unittest discover -s tests -p test_local_setup.py -v
docker compose exec frontend npm run build
```

The older controller unit/integration tests predate the current endpoint contracts and are not the local setup regression suite.

## Scope

This is a local demonstration, not a production deployment. The original application still lacks
server-side authorization and uses plain-text passwords. Use fictional data only. The displayed
risk percentages are model-derived scores, not validated clinical probabilities.

The backend dependency versions are declared in `back/requirements.txt`. Database configuration
uses `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`; Compose supplies these automatically.
`API_HOST` controls the backend bind address. Dataset paths resolve relative to the source files.

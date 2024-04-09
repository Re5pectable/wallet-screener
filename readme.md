# Kek

```bash
docker-compose exec wallet-screener-parser /bin/sh -c "cd src && alembic upgrade head"
```

To auto-generate a new migration:

```bash
docker-compose exec wallet-screener-parser /bin/sh -c "cd src && alembic revision --autogenerate -m 'init'"
```

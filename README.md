


## Postgres DB(with Docker) set up
```
docker pull postgres
```

```
docker run -p 5432:5432 -d \
    --name krakenPG \
    -e POSTGRES_PASSWORD=krakenkey \
    -e POSTGRES_USER=krakenadmin \
    -e POSTGRES_DB=krakendb \
    -v pgdata:/var/lib/postgresql/data \
    postgres

```
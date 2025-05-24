


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

## Import file
```
python manage.py import_d0010 sample_files/sample.D0010  
```

## Admin search
```
python3 manage.py createsuperuser
```
```
python3 manage.py runserver
```
```
visit http://localhost:8000/admin
```
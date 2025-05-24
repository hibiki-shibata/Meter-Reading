# ⚡ Kraken Meter Data Import Tool

A Django-based tool to import and manage electricity meter data (D0010 flow files), using PostgreSQL and Docker for infrastructure.

---
## 🚀 Quick Start Guide


### 1. 🐘 Set Up PostgreSQL with Docker

Set up a local PostgreSQL instance using Docker:

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


### 2. ⚙️ Set Up Django Project


In ~KrakenProject/ 
Install required dependencies:
(Use venv depending on your environment)

```
pip3 install -r requirements.txt
```

Database migration:
```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```



### 3. 📥 Import example D0010 Data File into the DB

In ~KrakenProject/
```
python3 manage.py import_d0010 sample_files/sample.D0010  
```



### 4. 🔐 Access the Admin Panel

In ~KrakenProject/
Create a superuser account:

```
python3 manage.py createsuperuser
```

Start the development server:

```
python3 manage.py runserver
```

Open your browser and go to:

```
http://localhost:8000/admin 
```


## 5. ✅ Run Tests

In ~KrakenProject/

```
python3 manage.py test    
```

---


📁 Project Structure

```
KrakenProject/
├── apps/
│   └── meterData_handler_app/
│       ├── admin.py # Admin site config
│       ├── apps.py
│       ├── management/
│       │   └── commands/
│       │       └── import_d0010.py # manual command config
│       ├── migrations/
│       ├── models/
│       │   └── models.py # Model
│       ├── services/
│       │   └── file_parser.py # parser files imported via manual command
│       ├── tests/ # corresponded test files
│       │   ├── test_management/
│       │   ├── test_models/
│       │   └── test_services/
│       └── views.py
├── sample_files/
│   └── sample.D0010 # samle D0010 file
├── manage.py
├── requirements.txt
└── README.md
```
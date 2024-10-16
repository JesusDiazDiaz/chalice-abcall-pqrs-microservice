

```bash
python3 -m venv .venv
pip install -r requirements.txt
docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres
export DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb
chalice local
```
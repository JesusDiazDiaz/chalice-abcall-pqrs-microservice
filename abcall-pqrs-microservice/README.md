
```bash
chalice package --merge-template extras.json out

aws cloudformation package \
     --template-file out/sam.json \
     --s3-bucket infra-abc \
     --output-template-file out/packaged-app/packaged.yaml

aws cloudformation deploy \
    --template-file out/packaged-app/packaged.yaml \
    --stack-name pqrs-service-stack \
    --capabilities CAPABILITY_IAM

```

# Run local using chalice local
```bash
python3 -m venv .venv
pip install -r requirements.txt
docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres
export DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb
chalice local
```
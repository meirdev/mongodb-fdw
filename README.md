# MongoDB FDW: python + multicorn2

## Install

```bash
docker build -t multicorn .
docker run -d -v $PWD:/home/code -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword multicorn
```

inside the container:

```bash
cd /home/code
python setup.py install
```

create file to logs:

```bash
touch /var/log/mongodb_fdw.txt
chmod 0777 /var/log/mongodb_fdw.txt
```

connect to PostgreSQL:

```bash
psql -U postgersql
```

add tables (change the connection details to MongoDB):

```sql
CREATE SERVER mongodb_fdw
FOREIGN DATA WRAPPER multicorn
OPTIONS (
    wrapper 'mongodb_fdw.MongoDB'
);

CREATE USER MAPPING FOR postgres
SERVER mongodb_fdw
OPTIONS (
    host 'host.docker.internal',
    port '55000',
    username 'docker',
    password 'mongopw',
    db 'demo'
);

CREATE FOREIGN TABLE posts (
    _id text,
    title text,
    content text,
    created_at timestamp
)
SERVER mongodb_fdw
OPTIONS (
    collection 'posts'
);

-- DROP FOREIGN TABLE posts;
```

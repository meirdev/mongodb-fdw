# Dockerfile

FROM postgres:13-bullseye

RUN apt update && \
    apt install -y build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev libxml2-utils xsltproc && \
    apt install -y python3 python3-dev python3-setuptools python3-pip && \
    apt install -y postgresql-server-dev-13 && \
    apt install -y git

RUN git clone https://github.com/pgsql-io/multicorn2.git && \
    cd multicorn2 && \
    make && \
    make install

RUN echo "CREATE EXTENSION multicorn;" >> docker-entrypoint-initdb.d/multicorn.sql

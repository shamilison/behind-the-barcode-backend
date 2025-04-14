FROM postgres:17

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Optional: copy SQL scripts for initialization
COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

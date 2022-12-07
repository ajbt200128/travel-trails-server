FROM postgis/postgis
COPY postgis.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
ENV POSTGRES_PASSWORD=postgres
CMD ["postgres"]

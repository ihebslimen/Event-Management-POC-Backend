FROM mariadb:10.11.6

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

FROM mysql:8.0

EXPOSE 3306
COPY ./conf.d/* /etc/mysql/conf.d/
COPY ./init.d/* /docker-entrypoint-initdb.d/

CMD ["mysqld"]
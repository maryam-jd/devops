FROM mongo:7.0
ENV MONGO_INITDB_DATABASE=tododb
COPY init-db.js /docker-entrypoint-initdb.d/init-db.js
EXPOSE 27017
VOLUME ["/data/db"]
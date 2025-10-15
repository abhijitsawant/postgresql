<h1>API build documentation for Postgres SQL API Server (Node.JS)</h1>

<pre>
#_____Directory Structure_____
postgres-api/
├─ Dockerfile
├─ package.json
├─ index.js
└─ package-lock.json (auto-created)


#_____Create a Docker network_____
docker network create flowdb-net

#_____Ensure you're running PostgreSQL container on above created network_____
docker network connect flowdb-net postgres-flowdb

#_____Build API Image_____
docker build -t postgres-api .

#_____Run API Server_____
docker run -d --name postgres-api --network flowdb-net -p 3000:3000 postgres-api


</pre>

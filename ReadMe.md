<h1>PostgreSQL Experimentation</h1>

<h2>Docker Setup</h2>
<pre>
#_____Dockerfile_____
FROM postgres:15

# Environment variables
ENV POSTGRES_USER=flowuser
ENV POSTGRES_PASSWORD=flowpass
ENV POSTGRES_DB=flowdb

# Expose default port
EXPOSE 5432

#_____Build Image_____
docker build -t postgres-flowdb .

#_____Run Container Instance_____
docker run -d --name postgres-flowdb -p 5432:5432 postgres-flowdb


</pre>

<h2>Database Operations</h2>
<pre>
#_____Login to Postgres Client through container_____
docker exec -it 87eef2399cbe psql -U flowuser -d flowdb

#_____Create Table_____
CREATE TABLE IF NOT EXISTS flow_records (
    key_bin TEXT PRIMARY KEY,
    b_in BIGINT,
    b_out BIGINT,
    p_in BIGINT,
    p_out BIGINT,
    proto BIGINT,
    t_bytes BIGINT,
    cnt BIGINT,
    dev TEXT,
    src_ip TEXT,
    dst_ip TEXT,
    dst_port INT
);

#_____See all tables_____
\dt

#_____Verify Table_____
\d flow_records

#_____See Records_____
SELECT * FROM flow_records
SELECT * FROM flow_records WHERE dst_port = 443;



</pre>





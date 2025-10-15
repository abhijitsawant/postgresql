#Build Image
docker build -t postgres-flowdb .


#Run Container Instance
docker run -d --name postgres-flowdb -p 5432:5432 postgres-flowdb

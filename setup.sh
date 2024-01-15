#; Prior to running the docker-compose, ensure the instances have
#; read-write permissions to the bindmounts.

source parameters.cfg

chmod -R 755 iris
chmod -R 755 webgateway

#export IRIS_BASE_IMAGE=containers.intersystems.com/iscinternal/sds/base_iris:1.20.10
#export IRIS_WEBGATEWAY_IMAGE=containers.intersystems.com/intersystems/webgateway:2023.3

cd LLM_layer/LC_Chain 
docker build -t dbchain_test .

cd ..
cd ..

cd iris_base
docker build -t irisdata .
docker-compose up -d 
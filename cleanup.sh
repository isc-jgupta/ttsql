docker stop iris_base-iris-1
docker rm iris_base-iris-1
rm -rf iris/durable

docker stop webgateway
docker rm webgateway
rm -rf webgateway/durable

docker stop iris_base-DBChain-1
docker rm iris_base-DBChain-1
rm -rf DBChain/durable
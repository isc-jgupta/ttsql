cd pytest
docker build -t pytest .
#docker container run -it --network=iris_base_llm-layer pytest
docker container run --name pytesting -d --network=iris_base_llm-layer pytest
docker exec pytesting pytest test2.py --html=report.html --junitxml=tests.xml
docker cp pytesting:/app/report.html .
docker cp pytesting:/app/tests.xml .
docker rm -f pytesting

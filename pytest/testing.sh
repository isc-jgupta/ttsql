docker build -t pytest .
docker container run -it --network=iris_base_llm-layer pytest pytest test2.py


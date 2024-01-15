FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get install ca-certificates-java && \
    apt-get install -y --no-install-recommends python3 && \
    apt-get install -y python3-pip && \
    apt-get clean && \ 
    update-ca-certificates -f;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV OPENAI_API_KEY="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"


RUN pip install --upgrade pip 

RUN pip install pytest langserve fastapi pytest-html 

WORKDIR /app
COPY . .

#CMD ["pytest", "test.py"]

ENTRYPOINT ["tail", "-f", "/dev/null"]

#docker run -it pytest pytest test.py
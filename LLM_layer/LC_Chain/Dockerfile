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

RUN pip install openai langchain==0.0.354 langchain_experimental &&\
    pip install SQLAlchemy &&\
    pip install sse-starlette &&\
    pip install fastapi &&\
    pip install langserve &&\
    pip install JayDeBeApi
    
WORKDIR /app
ADD ./DBChain .

RUN pip install https://github.com/intersystems-community/intersystems-irispython/releases/download/3.7.5/intersystems_iris-3.7.5-py3-none-any.whl
RUN pip install sqlalchemy-iris

EXPOSE 12344 
CMD ["uvicorn", "DBChainUpdated:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "12344"]

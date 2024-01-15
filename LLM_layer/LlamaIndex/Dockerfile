FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    apt-get install -y python3-pip && \
    apt-get clean && \ 
    update-ca-certificates -f;

ENV OPENAI_API_KEY="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"

RUN pip install --upgrade pip
RUN pip install openai langchain==0.0.354
#RUN pip install "langserve[all]"
RUN pip install -U langchain-cli

WORKDIR /app
ADD ./app /app

RUN 

CMD [ "python3", "./server.py"]

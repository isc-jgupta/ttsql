FROM jupyter/base-notebook

ENV OPENAI_API_KEY="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"

RUN pip install --upgrade pip

RUN pip install openai langchain==0.0.354 langchain_experimental &&\
    pip install SQLAlchemy &&\
    pip install sse-starlette &&\
    pip install fastapi &&\
    pip install langserve
    
WORKDIR /app
ADD . .

RUN pip install https://github.com/intersystems-community/intersystems-irispython/releases/download/3.7.5/intersystems_iris-3.7.5-py3-none-any.whl
RUN pip install sqlalchemy-iris


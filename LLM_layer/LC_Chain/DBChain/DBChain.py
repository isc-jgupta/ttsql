"""An example that shows how to use the API handler directly.

For this to work with RemoteClient, the routes must match those expected
by the client; i.e., /invoke, /batch, /stream, etc. No trailing slashes should be used.
"""
from importlib import metadata
from typing import Annotated
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from fastapi import Depends, FastAPI, Request, Response
from langchain_core.runnables import RunnableLambda
from sse_starlette import EventSourceResponse

from langserve import APIHandler

PYDANTIC_VERSION = metadata.version("pydantic")
_PYDANTIC_MAJOR_VERSION: int = int(PYDANTIC_VERSION.split(".")[0])

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)


##
# Example 1 -- invoke, batch together with doc-generation
# This endpoint shows how to expose `invoke` and `batch` using the APIHandler.
# It also shows how to generate documentation properly so it works correctly
# depending on Fast API and pydantic versions.
def add_one(x: str) -> str:
    
    _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}

    Never use LIMIT statement, Never use TOP statement.
    Format all numeric response ###,###,###,###.
    Question: {input}"""
    PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
    )


    connection_string = "iris://superuser:test@irisData:1972/SDS"
    db = SQLDatabase.from_uri(connection_string)
    llm = OpenAI(temperature=0, verbose=True, model="gpt-3.5-turbo-instruct")
    #db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)
    return db_chain.run(x)
  
chain = RunnableLambda(add_one)

api_handler = APIHandler(chain, path="/simple")


# First register the endpoints without documentation
@app.post("/simple/invoke", include_in_schema=False)
async def simple_invoke(request: Request) -> Response:
    """Handle a request."""
    # The API Handler validates the parts of the request
    # that are used by the runnnable (e.g., input, config fields)
    return await api_handler.invoke(request)


@app.post("/simple/batch", include_in_schema=False)
async def simple_batch(request: Request) -> Response:
    """Handle a request."""
    # The API Handler validates the parts of the request
    # that are used by the runnnable (e.g., input, config fields)
    return await api_handler.batch(request)


# Here, we show how to populate the documentation for the endpoint.
# Please note that this is done separately from the actual endpoint.
# This happens due to two reasons:
# 1. FastAPI does not support using pydantic.v1 models in the docs endpoint.
#    "https://github.com/tiangolo/fastapi/issues/10360"
#    LangChain uses pydantic.v1 models!
# 2. Configurable Runnables have a *dynamic* schema, which means that
#    the shape of the input depends on the config.
#    In this case, the openapi schema is a best effort showing the documentation
#    that will work for the default config (and any non-conflicting configs).
if _PYDANTIC_MAJOR_VERSION == 1:  # Do not use in your own
    # Add documentation
    @app.post("/simple/invoke")
    async def simple_invoke_docs(
        request: api_handler.InvokeRequest,
    ) -> api_handler.InvokeResponse:
        """API endpoint used only for documentation purposes. Populate /docs endpoint"""
        raise NotImplementedError(
            "This endpoint is only used for documentation purposes"
        )

    @app.post("/simple/batch")
    async def simple_batch_docs(
        request: api_handler.BatchRequest,
    ) -> api_handler.BatchResponse:
        """API endpoint used only for documentation purposes. Populate /docs endpoint"""
        raise NotImplementedError(
            "This endpoint is only used for documentation purposes"
        )

else:
    print(
        "Skipping documentation generation for pydantic v2: "
        "https://github.com/tiangolo/fastapi/issues/10360"
    )


##
# Example 2 -- Expose `invoke` and `stream` using the API Handler.
# Uses FastAPI Depends get a ready API handler.
async def _get_api_handler() -> APIHandler:
    """Prepare a RunnableLambda."""
    return APIHandler(RunnableLambda(add_one), path="/v2")


@app.post("/v2/invoke")
async def v2_invoke(
    request: Request, runnable: Annotated[APIHandler, Depends(_get_api_handler)]
) -> Response:
    """Handle invoke request."""
    # The API Handler validates the parts of the request
    # that are used by the runnnable (e.g., input, config fields)
    return await runnable.invoke(request)


@app.post("/v2/stream")
async def v2_stream(
    request: Request, runnable: Annotated[APIHandler, Depends(_get_api_handler)]
) -> EventSourceResponse:
    """Handle stream request."""
    # The API Handler validates the parts of the request
    # that are used by the runnnable (e.g., input, config fields)
    return await runnable.stream(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=12344)

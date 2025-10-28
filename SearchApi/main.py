from pathlib import Path
import logging
from fastapi import FastAPI, Request

from SearchApi.version import v as version
#from chromanew.chromanew import LocalEmbedding, PATH_EMBEDDING_MODEL, PATH_CHROMA
import chromanew.chromanew

s = logging.StreamHandler()
logging.basicConfig(handlers=[s], level=logging.INFO)

app = FastAPI()

# Load vector db class
chromanew.chromanew.PATH_CHROMA = Path.cwd() / "chromanew" / "data"
chromanew.chromanew.PATH_EMBEDDING_MODEL = Path.cwd() / "chromanew" / "embeddinggemma-300m"
COUNT_DOCS_IN_SEARCH_RES = 2

core = chromanew.chromanew.LocalEmbedding()


@app.get("/")
async def root(request: Request):
    client = request.client
    return {"message": "Api for get results of vector similarity search",
            "example": f"http://{client.host}/search/*text_of_your_query*",
            "version": version}


@app.get("/search/{query_text}")
def search(query_text: str):  # sync multythread need test chroma
    res = core.search(query_texts=[query_text],
                      count_docs=COUNT_DOCS_IN_SEARCH_RES)
    if res:
        return {"Search Results": res}

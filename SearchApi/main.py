from pathlib import Path
import logging
from fastapi import FastAPI, Request, Body
from yaml import safe_load

from SearchApi.version import v as version
#from chromanew.chromanew import LocalEmbedding, PATH_EMBEDDING_MODEL, PATH_CHROMA
import chromanew.chromanew

s = logging.StreamHandler()
logging.basicConfig(handlers=[s], level=logging.INFO)

app = FastAPI()

# Load vector db class
chromanew.chromanew.PATH_CHROMA = Path.cwd() / "chromanew" / "data"

with open(Path.cwd() / "SearchApi" / "config.yaml", "r") as f:
    config = safe_load(f)
if config:
    chromanew.chromanew.PATH_EMBEDDING_MODEL = Path.cwd() / "chromanew" / config.get("MODEL_DIR_NAME")
    COUNT_DOCS_IN_SEARCH_RES = config.get("COUNT_DOCS_IN_SEARCH_RES")
else:
    chromanew.chromanew.PATH_EMBEDDING_MODEL = Path.cwd() / "chromanew" / "embeddinggemma-300m"
    COUNT_DOCS_IN_SEARCH_RES = 2
    logging.warning("Default config loaded.")

core = chromanew.chromanew.LocalEmbedding()


@app.get("/")
async def root(request: Request):
    client = request.client
    return {"message": "Api for get results of vector similarity search",
            # "example": f"http://{client.host}/search/*text_of_your_query*", # not for container
            "examples": {"search": f"http://HOST/search/*text_of_your_query*",
                         "add_docs": "POST /add body:{'docs':[], 'ids':[]}"},
            "version": version}


@app.get("/search/{query_text}")
def search(query_text: str):  # sync multythread need test chroma
    res = core.search(query_texts=[query_text],
                      count_docs=COUNT_DOCS_IN_SEARCH_RES)
    if res:
        return {"Search Results": res}


@app.post("/add")
def append_documents(docs: list = Body(embed=True),
                     ids: list = Body(embed=True),
                     meta: list | None = Body(embed=True)):
    if docs and ids:
        if len(docs) == len(ids):
            if meta:
                res = core.append_docs(documents=docs, ids=ids, meta=meta)
            else:
                res = core.append_docs(documents=docs, ids=ids)
            if res:
                return 'Documents successfully added.'
            else:
                return 'Something bad was happened.'
        else:
            return 'Count documents must be equal count IDs.'

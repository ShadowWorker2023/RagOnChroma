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
    # client = request.client
    return {"message": "Api for get results of vector similarity search",
            # "example": f"http://{client.host}/search/*text_of_your_query*", # not for container
            "examples": {"root": "This page.",
                         "search": {"GET": f"http://HOST/search/text_of_your_query?collection=collection_name"
                                    f" - optional key"},
                         "add_docs": {"POST": "http://HOST/add?collection=collection_name - optional key",
                                      "body": {'docs': [],
                                               "ids": [],
                                               "meta": 'null | [{},...]'}},
                         "collections": {"GET": "http://HOST/collections"}},
            "version": version}


@app.get("/search/{query_text}")
def search(query_text: str,
           collection: str = None):  # sync multythread need test chroma
    if collection:
        res = core.search(query_texts=[query_text],
                          count_docs=COUNT_DOCS_IN_SEARCH_RES,
                          collection_name=collection)
    else:
        res = core.search(query_texts=[query_text],
                          count_docs=COUNT_DOCS_IN_SEARCH_RES)
    if res:
        return {"Search Results": res}


@app.get("/collections")
def search():  # sync multythread need test chroma
    res = core.get_collections()
    if res:
        return {f"Collections in vector DB ({len(res)})": res}
    else:
        return {"message": "Can't get collections."}


@app.post("/add")
def append_documents(docs: list = Body(embed=True),
                     ids: list = Body(embed=True),
                     meta: list | None = Body(embed=True),
                     collection: str | None = None):
    if docs and ids:
        if len(docs) == len(ids):
            if meta:
                if collection:
                    res = core.append_docs(documents=docs, ids=ids, meta=meta, collection_name=collection.lower())
                else:
                    res = core.append_docs(documents=docs, ids=ids, meta=meta)
            else:
                if collection:
                    res = core.append_docs(documents=docs, ids=ids, collection_name=collection.lower())
                else:
                    res = core.append_docs(documents=docs, ids=ids)
            if res:
                return 'Documents successfully added.'
            else:
                return 'Something bad was happened.'
        else:
            return 'Count documents must be equal count IDs.'


@app.post("/embedding")
def get_embedding(doc: str = Body(embed=True)):
    embedding_result = core.get_embedding(text=doc)
    return {"vector_size": embedding_result.get("size"),
            "vector": embedding_result.get("embedding")}

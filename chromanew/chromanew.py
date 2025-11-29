from pathlib import Path
import logging
from typing import List

import chromadb
#from chromadb import Documents, EmbeddingFunction, Embeddings
#from sentence_transformers import SentenceTransformer
#from transformers import PreTrainedModel
#import torch
#import torchvision
from sentence_transformers import SentenceTransformer
from chromadb import Documents, EmbeddingFunction, Embeddings


PATH_CHROMA = Path.cwd() / "data"
PATH_EMBEDDING_MODEL = Path.cwd() / "embeddinggemma-300m"
SEARCH_DOCS_COUNT = 2
DEF_COLLECTION = "my_collection"


class LocalEmbedding(EmbeddingFunction[Documents]):
    model: any
    vdb_client: any
    collection: any

    def __init__(self):
        self._init_vector_db(path_to_vbd=PATH_CHROMA)
        self._init_embedding_model(path_to_model=PATH_EMBEDDING_MODEL)

    def __call__(self, input: Documents) -> Embeddings:
        # Convert the numpy array to a Python list
        logging.info(f'Embedding func called with param: {str(input)}')
        return self.model.encode_document(input).tolist()

    def _init_vector_db(self, path_to_vbd: Path):
        self.vdb_client = chromadb.PersistentClient(path=path_to_vbd)
        logging.info(f'ChromaDB init successfully, v{self.vdb_client.get_version()}')

    def _init_embedding_model(self, path_to_model: Path):
        self.model = SentenceTransformer(str(path_to_model))
        logging.info('Embedding model loaded')

    def append_docs(self, documents: list | None, ids, collection_name: str = DEF_COLLECTION):
        # switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
        self.collection = self.vdb_client.get_or_create_collection(name=collection_name, embedding_function=self)
        # switch `add` to `upsert` to avoid adding the same documents every time
        self.collection.upsert(documents=documents, ids=ids)
        return True

    def search(self, query_texts: List[str], count_docs: int | None = SEARCH_DOCS_COUNT) -> list:
        if not hasattr(self, 'collection'):
            self.collection = self.vdb_client.get_or_create_collection(name=DEF_COLLECTION, embedding_function=self)
            # TODO сообщать о том, что пытаемся искать в созданной только что пустой коллекции
        results = self.collection.query(query_texts=query_texts,  # Chroma will embed this for you
                                        n_results=count_docs)  # how many results to return
        if results:
            ids = results.get('ids')[0]
            docs = results.get("documents")[0]
            metadatas = results.get("metadatas")[0]
            distances = results.get("distances")[0]

            answer = []
            for index, id in enumerate(ids):
                answer.append({'id': id,
                               'document': docs[index],
                               'metadata': metadatas[index],
                               'distance': distances[index]})
            return answer

s = logging.StreamHandler()
logging.basicConfig(handlers=[s], level=logging.INFO)


if __name__ == '__main__':
    documents = [
            "This is a document about apple",
            "This is a document about oranges",
            "This is a document about another objects",
            "This is a document about cars"
            ]
    ids = ["id1", "id2", "id3", "id4"]

    model = LocalEmbedding()
    model.append_docs(documents=documents, ids=ids)
    print(model.search(["about engine"]))

# TODO : разбиение на чанки, мб с исп langchain-splitter, с заполнением? pad
# разобраться с видами поиска в хроме
# на основе данных тестить, вместо разбиения на чанки всего текста документа.
# Строить вектора из Анотаций\наборов ключевых слов, которые целиком влезут в один чанк

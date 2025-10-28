from typing import Dict, Any, List

from langchain_text_splitters import RecursiveCharacterTextSplitter

MAX_CHUNK_SIZE = 512
CHUNK_OVERLAP = 64


class TextPreProcessor:
    @staticmethod
    def split_text_into_chunks(text: str, metadata: Dict[str, Any]) -> List[Any]:
        """Разделение текста на чанки с сохранением метаданных."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.create_documents(texts=[text], metadatas=[metadata])
        return chunks

    def chanks_by_summary(self, text: str, metadata: Dict[str, Any], summary_size: int = MAX_CHUNK_SIZE) -> List[Any]:
        """
        1 Chank by 1 input text
        Use an AI summarization
        """
        # integrate AI API
        pass



from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(text: str, metadata: Dict[str, Any]) -> List[Any]:
    """Разделение текста на чанки с сохранением метаданных."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.create_documents(texts=[text], metadatas=[metadata])
    return chunks

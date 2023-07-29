import requests
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

from llama_index.readers.base import BaseReader
from llama_index import GPTVectorStoreIndex
from llama_index.schema import Document

class SimpleWebPageReader(BaseReader):
    """Simple web page reader.

    Reads pages from the web.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.

    """

    def __init__(self, html_to_text: bool = False) -> None:
        """Initialize with parameters."""
        try:
            import html2text  # noqa: F401
        except ImportError:
            raise ImportError(
                "`html2text` package not found, please run `pip install html2text`"
            )
        self._html_to_text = html_to_text

    def load_data(urls: List[str]) -> List[Document]:
        """Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []
        for url in urls:
            response = requests.get(url, headers=None).text
            import html2text

            response = html2text.html2text(response)

            documents.append(Document(text=response))

        return documents

docs = SimpleWebPageReader.load_data(urls=['https://hack2skill.com/hack/gen-ai-rush-buildathon/','https://mindsdb.com/about'])
print(docs)

index = GPTVectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
query_results = query_engine.query("what is the TPF GenAI Rush - Buildathon?" )
query_results = query_engine.query("who founded MindsDB?")
#query_results = query_engine.query("How many sick leaves an employee is eligible for?")


print(query_results)

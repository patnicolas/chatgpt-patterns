from unittest import TestCase
from src.llm_langchain.llmembeddingsearch import LLMEmbeddingSearch


class TestLLMEmbeddingSearch(TestCase):
    def test_default_search_with_text(self):
        search_type = LLMEmbeddingSearch.default_search
        document_type = LLMEmbeddingSearch.text_document_type

        llmEmbeddingSearch = LLMEmbeddingSearch.build(["../../input/file1.txt", "../../input/file2.txt"], document_type)
        query = "what are the duties for Principal Data Architect"
        responses = llmEmbeddingSearch(query, search_type)
        print(str(responses))

    def test_embedding_vector_search_with_text(self):
        search_type = LLMEmbeddingSearch.search_by_vector
        document_type = LLMEmbeddingSearch.text_document_type

        llmEmbeddingSearch = LLMEmbeddingSearch.build(["../../input/file1.txt", "../../input/file2.txt"], document_type)
        query = "what are the duties for Principal Data Architect"
        responses = llmEmbeddingSearch(query, search_type)
        print(str(responses))

from langchain.vectorstores import VectorStore
from langchain.embeddings import OpenAIEmbeddings

class CustomVectorStore(VectorStore):
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.documents = []

    def add_document(self, file_path):
        # Process the document and add it to the vector store
        with open(file_path, 'r') as file:
            content = file.read()
            embedding = self.embeddings.embed(content)
            self.documents.append((content, embedding))

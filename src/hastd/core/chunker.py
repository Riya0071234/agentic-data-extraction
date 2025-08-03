import re
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    A utility class for splitting large unstructured text into
    semantically coherent and overlapping chunks.
    """

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        """
        Initialize the chunker with a chunk size and overlap.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )

    def clean_text(self, text: str) -> str:
        """
        Pre-clean the text by removing excessive whitespace and broken symbols.
        """
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\u00a0", " ", text)  # non-breaking space
        text = text.strip()
        return text

    def chunk_text(self, text: str) -> List[str]:
        """
        Split the input text into semantically aware chunks.
        """
        cleaned = self.clean_text(text)
        return self.splitter.split_text(cleaned)


# Optional CLI test
if __name__ == "__main__":
    sample = """
    Jane Doe is the lead engineer. You can reach her at jane@example.com.
    Her user ID is 12345. She leads the AI division of Acme Corp.
    """
    chunker = TextChunker()
    chunks = chunker.chunk_text(sample)
    for i, chunk in enumerate(chunks):
        print(f"[Chunk {i+1}]\n{chunk}\n")

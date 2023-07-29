from pathlib import Path
from llama_index import GPTVectorStoreIndex, download_loader
from typing import Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PDFReader(BaseReader):
    """PDF reader."""
  

    def load_data():
        """Parse file."""
        import pypdf

        import os
        import glob

        directory_path = '/Users/bseetharaman/Desktop/FY23/TPF_Hackathon/documents/hr'

        pdf_files = []
        for file in glob.glob(os.path.join(directory_path, '*.pdf')):
            pdf_files.append(file)
        
       
        docs = []
        print("List of PDF files in the directory:")
        for file in pdf_files:

            with open(file, "rb") as fp:
                pdf = pypdf.PdfReader(fp)
                num_pages = len(pdf.pages)
               
                for page in range(num_pages):
                    page_text = pdf.pages[page].extract_text()
                    page_label = pdf.page_labels[page]
                    metadata = {"page_label": page_label, "file_name": file}

                    docs.append(Document(text=page_text, extra_info=metadata))

        return docs

docs = PDFReader.load_data()
print(docs)


index = GPTVectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
query_results = query_engine.query("what is maximum amount for Educational & Learning Reimbursement?")
#query_results = query_engine.query("How many sick leaves an employee is eligible for?")


print(query_results)

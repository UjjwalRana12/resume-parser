from langchain_community.document_loaders import PyPDFLoader


path = "C9742.pdf"  
loader = PyPDFLoader(path)

try:
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {path}.")

    # Check if the PDF is empty
    if not documents:
        print("The PDF is empty or could not be loaded.")
    else:
        # Process all pages
        resume_text = ""
        for i, doc in enumerate(documents):
            print(f"--- Page {i+1} ---")
            print(f"Content (first 100 chars): {doc.page_content[:100]}...")
            print(f"Metadata: {doc.metadata}")
            resume_text += doc.page_content + "\n"

        # Save or process the full text
        print(f"\nTotal text length: {len(resume_text)} characters")
except Exception as e:
    print(f"An error occurred while loading the PDF: {e}")
from pymongo import MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import key_param

# Set the MongoDB URI, DB, Collection Names
client = MongoClient(key_param.MONGODB_URI)
dbName = "book_mongodb_chunks"
collectionName = "chunked_data"
collection = client[dbName][collectionName]

# Load PDF and clean pages
loader = PyPDFLoader("deeplearningbook.pdf")
pages = loader.load()
cleaned_pages = []

for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)


# Create a custom metadata tagger for Gemini
def create_custom_metadata_tagger(schema):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b",
        google_api_key=key_param.LLM_API_KEY,
        temperature=0
    )

    # Create a prompt that instructs the model to extract metadata
    template = """
    Extract metadata from the text below according to this JSON schema:
    {schema}

    Text: {text}

    Return only a valid JSON object that matches the schema, nothing else.
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)

    def extract_metadata(text):
        try:
            response = chain.invoke({"schema": json.dumps(schema), "text": text})
            # Get the output key from the response
            if isinstance(response, dict) and "text" in response:
                json_str = response["text"]
            else:
                json_str = str(response)

            # Clean up the response to ensure it's valid JSON
            # Remove any markdown formatting if present
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()

            # Parse the JSON
            metadata = json.loads(json_str)
            return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            # Return a default metadata object that matches the schema
            return {
                "title": "Unknown title",
                "keywords": ["unknown"],
                "hasCode": False
            }

    return extract_metadata


# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)

# Define schema
schema = {
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "hasCode": {"type": "boolean"},
    },
    "required": ["title", "keywords", "hasCode"],
}

# Create custom metadata tagger
metadata_tagger = create_custom_metadata_tagger(schema)

# Process documents with metadata
processed_docs = []
for page in cleaned_pages:
    # Extract metadata
    metadata = metadata_tagger(page.page_content)
    # Add metadata to page
    page.metadata.update(metadata)
    processed_docs.append(page)

# Split documents
split_docs = text_splitter.split_documents(processed_docs)

# Initialize embeddings using Google Generative AI Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=key_param.LLM_API_KEY
)

# Store in MongoDB
vectorStore = MongoDBAtlasVectorSearch.from_documents(
    split_docs, embeddings, collection=collection
)

print(f"Successfully processed and stored {len(split_docs)} document chunks in MongoDB.")
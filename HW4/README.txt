CSCI 572 - INFORMATION RETRIEVAL AND WEB SEARCH ENGINES - HOME WORK 4

Q1.

Query1 - ("Author","Book","Summary") - data2.json
Query2 - ("Author","Book","Summary") - data2.json
Query3 - ("School","CourseName","CourseDesc") Page Rank (query) - CSCI 572 INFORMATION RETRIEVAL AND WEB SEARCH ENGINES (answer) - data3.json

Q2.

Query1   - Harry Potter Complete Collection.pdf
Query2_1 - Harry Potter Complete Collection.pdf
Query2_2 - Harry Potter Complete Collection.pdf


Q3.

Query1 - Recipes.pdf
Query2 - Harry Potter and Sorcerers Stone.pdf

I have gone through the source of the PDF-RAG app hosted on Hugging Face (https://huggingface.co/spaces/samim2024/PDF-RAG), and here’s a breakdown of the RAG process and UI:

1. RAG Workflow in the App (Steps Involved):

WORKFLOW SUMMARY:

File Upload -> Text Extraction -> Text Splitting -> Vector Store Creation -> Query -> Semantic Retrieval -> LLM Response Generation -> Output Display

The Retrieval Augmented Generation (RAG) process in this app is implemented using LangChain and involves the following key steps:


PDF Upload and Document Loading:

The user uploads a PDF file via the Streamlit UI using the st.file_uploader() function.
The file is saved to the local files directory.
The PyPDFLoader is used to load and parse the content of the PDF into a format suitable for further processing.


Text Splitting:

The PDF content is split into smaller chunks using the RecursiveCharacterTextSplitter class.
This ensures that the document is divided into manageable portions for embedding generation and retrieval, with a chunk size of 1500 characters and no overlap.


Vector Store Creation:

The Chroma vector store is initialized and populated with embeddings created using the HuggingFaceEmbeddings model (sentence-transformers/all-mpnet-base-v2).
The embeddings are persisted in the local directory (jj) for later retrieval.


Retriever Initialization:

A retriever is created using the vector store (st.session_state.vectorstore.as_retriever()).
This allows the app to retrieve relevant chunks of text based on user queries.


Prompt and Memory Setup:

A custom prompt template and conversation memory (ConversationBufferMemory) are set up to maintain the context of the conversation and generate coherent responses.


QA Chain Initialization:

A RetrievalQA chain is created using the vector store retriever and a HuggingFace model (mistralai/Mistral-7B-Instruct-v0.2) accessed via the HuggingFaceEndpoint.
The chain uses the retriever to fetch contextually relevant chunks of the document and generates responses based on user queries.


User Interaction and Response Generation:

When the user inputs a question, it is passed to the QA chain, which combines the retrieved document context with the LLM's generative capabilities to produce a response.
The response is displayed in the chat interface, simulating real-time typing for a more engaging experience.


2. How the UI Works:

UI SUMMARY:

Browse Files -> Upload the required PDF -> Analyzing PDF -> Enter your query in the text box provided below (You:) -> Click on '>' button beside the text -> Q is added to the conversation thread -> Answer is generated below the Question using RAG (Required Output).

It also have three dots on the top right (menu). It contains features like screencast to record the interactions with the RAG model, print option to print the image of user conversation (Q&A) and settings that enables the users to adjust the view (Wide Mode - Turn on to make this app occupy the entire width of the screen),themes and execution options (Run on save - Automatically updates the app when the underlying code is updated). The app's UI is built using Streamlit, and the following components are involved:

File Uploader:

The st.file_uploader() widget allows the user to upload a PDF.
Once a file is uploaded, it triggers the document processing workflow, including saving, loading, and splitting the PDF content.


Chat History Display:

Previous messages in the conversation are stored in st.session_state.chat_history and displayed using the st.chat_message() function.
Each message is labeled as either "user" or "assistant" for clarity.


Dynamic Chat Input:

The st.chat_input() widget enables the user to enter questions interactively.
User queries are appended to the session state and processed through the QA chain.


Assistant Response Display:

Responses are generated dynamically using the st.spinner() and st.empty() functions to simulate typing with a blinking cursor.
The final response is displayed alongside the user input in the chat interface.


Status Indicators:

The st.status() function shows a loading message ("Analyzing your document...") while the PDF is being processed.


Session State Management:

Streamlit's st.session_state is heavily used to maintain the state of various components, including the vector store, LLM, memory, and prompt.


THANK YOU
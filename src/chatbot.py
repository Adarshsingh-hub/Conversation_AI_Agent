from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import(ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)
from src.config import config
import logging

logger = logging.getLogger(__name__)

def load_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(
        model = config.EMBED_MODEL,
        openai_api_key=config.OPENAI_API_KEY
    )
    return Chroma(
        persist_directory=config.CHROMA_PATH,
        embedding_function = embeddings
    )
    
def build_prompt() -> ChatPromptTemplate:
    system = config.SYSTEM_PROMPT + (
        "\n\nContext from knowledge base:\n{context}"
    )
    
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system),
        HumanMessagePromptTemplate.from_template(
            "Question: {question}"
        )
    ])
    
class CustomerSupportChatbot:
    def __init__(self):
        self.vectorstore = load_vectorstore()
        self.retriever = self.vectorstore.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k": config.TOP_K}
        )
        self.llm = ChatOpenAI(
            model_name = config.OPENAI_MODEL,
            openai_api_key = config.OPENAI_API_KEY,
            temperature = 0,
            max_tokens = config.MAX_TOKENS
        )
        self.memory = ConversationBufferWindowMemory(
            k = 10,
            memory_key = "chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever = self.retriever,
            memory = self.memory,
            combine_docs_chain_kwargs={
                "prompt":build_prompt()
            },
            return_source_documents=True,
            verbose =False
        )
        
    def chat(self,message:str) -> dict:
        try:
            result = self.chain.invoke({
            "question"
            : message})
            sources = list({
            doc.metadata.get(
            "source"
            ,
            "unknown"
            )
            for doc in result.get(
            "source_documents"
            ,[])
            })
            return {
            "answer"
            : result[
            "answer"
            ],
            "sources"
            : sources,
            "success"
            : True
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"answer": "Something went wrong. Please try again.",
            "sources": [],
            "success": False}
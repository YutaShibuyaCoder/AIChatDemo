from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from document_loader import load_document

def create_chatbot(uploaded_file, api_key, model_name):
    # アップロードされたファイルからテキストを抽出
    text = load_document(uploaded_file)
    
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_texts([text], embedding=embeddings)
    
    # プロンプトテンプレートの定義
    prompt_template = """
    あなたは社内FAQの質問に答えるAIアシスタントです。以下の情報源に基づいて質問に簡潔に答えてください。

    情報源: {context}

    人間: {question}

    指示:
    - 情報源の内容に基づいて、直接的かつ簡潔に回答してください。
    - 大項目や箇条書きは避け、できるだけ1〜2文で回答してください。
    - 情報源に記載がない場合は、「申し訳ありませんが、その情報はFAQに含まれていません」と簡潔に答えてください。

    AIアシスタント:
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    # モデルの指定とチェーンの作成
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=api_key),
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    
    return qa

def get_response(qa, query, chat_history):
    result = qa({"question": query, "chat_history": chat_history})
    return result['answer']
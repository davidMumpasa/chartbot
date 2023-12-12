from flask import Flask, jsonify, request
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from flask_cors import CORS
import logging

import bussinessLogic

app = Flask(__name__)
CORS(app, supports_credentials=True)

loggedInUser = []
conversation_history = []
chain = None

# user_email = "david@fluidintellect.com"
#
# result = bussinessLogic.execute_query(f"SELECT email,user_type FROM user WHERE email = '{user_email}'")
# db_email = result[0][0] if result else None
# user_type = result[0][1] if result else None


@app.route('/login', methods=['POST'])
def login():
    global chain, courses
    data = request.get_json()
    user_email = data.get('user_email', '')

    if not user_email:
        return jsonify({'error': 'User email is required'}), 400

    # Assuming your BusinessLogic class has a method like execute_query
    result = bussinessLogic.execute_query(f"SELECT email,user_type FROM user WHERE email = '{user_email}'")
    db_email = result[0][0] if result else None
    user_type = result[0][1] if result else None

    if user_email == db_email:
        # loggedInUser.append(user_email)
        # loggedInUser.append(user_type)

        if user_type == "SuperAdmin":
            users = bussinessLogic.fetch_users()
            badges = bussinessLogic.fetch_badges()
            user_quizzies = bussinessLogic.fetch_all_user_quizzes()
            quizzes = bussinessLogic.fetch_quizzes()
            courseUser = bussinessLogic.fetch_all_course_users()
        else:
            users = bussinessLogic.fetch_user_data(user_email)
            badges = bussinessLogic.fetch_user_badges(user_email)
            user_quizzies = bussinessLogic.fetch_user_quizzes(user_email)
            quizzes = bussinessLogic.fetch_quizzes()
            courseUser = bussinessLogic.fetch_user_has_course()
            courses = bussinessLogic.fetch_courses()

        combined_content = bussinessLogic.convert_data_to_documents(users, user_quizzies, quizzes, courses,
                                                                    courseUser, badges)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_text(combined_content)

        # print("*******************************************************************")
        # print(quizzes, "\n\n", courseUser, "\n\n", user_quizzies, "\n\n", badges, "\n\n", users)
        # print(combined_content)

        llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q8_0.bin", model_type="llama",
                            config={'max_new_tokens': 128, 'temperature': 0.1})
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                           model_kwargs={'device': "cpu"})
        vector_store = FAISS.from_texts(text_chunks, embeddings)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                      retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                      memory=memory)

        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/submitUserInput', methods=['POST'])
def submit_user_input():
    try:
        data = request.get_json()
        user_input = data.get('userInput', '')
        conversation_history.append({'user': user_input, 'llama': ''})  # Update based on your data structure
        return jsonify({'message': 'User input submitted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/getLlamaResponse', methods=['POST'])
def get_llama_response():
    try:
        data = request.get_json()
        user_input = data.get('userInput', '')
        # Use the Llama model to generate a response
        result = chain({"question": user_input, "chat_history": conversation_history})
        llama_response = result["answer"]

        # Update conversation history
        conversation_history.append({'user': user_input, 'llama': llama_response})

        return jsonify({'message': llama_response})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/getConversationHistory', methods=['GET'])
def get_conversation_history():
    return jsonify({'history': conversation_history})


if __name__ == '__main__':
    app.run()

import streamlit as st
import sqlite3
from utils.get_response import (
    get_bot_response,
    display_model_mapping,
    get_model, get_provider,
)
import csv
import os


st.set_page_config(page_title="DarkGPT", page_icon="random", layout="wide", initial_sidebar_state="expanded")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

# Create a connection to the database
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Create table if not exists
try:
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (conversation_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
except Exception as e:
    st.error(f"An error occurred: {e}")


def main():
    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = 1

        columns = st.columns(3)  # Split the layout into three columns

        with columns[1]:
            st.header("DarkGPT")

        with columns[2]:
            display_model = st.selectbox("Select Model", list(display_model_mapping.keys()), index=0)
            internal_model = get_model(display_model)
            provider_name = get_provider(internal_model)

        with columns[0]:
            st.page_link(page='app.py', label='Back to Home', icon='🏠')
            st.page_link(page='pages/Summarize.py', label='Summarize', icon='📝')

        # Sidebar (left side) - New chat button
        if st.sidebar.button("✨ New Chat", key="new_chat_button"):
            st.session_state.chat_history.clear()
            st.session_state.conversation_id += 1

        # Sidebar (left side) - Display saved chat
        st.sidebar.write("Chat History")
        c.execute("SELECT DISTINCT conversation_id FROM chat_history")
        conversations = c.fetchall()
        for conv_id in reversed(conversations):
            c.execute("SELECT content FROM chat_history WHERE conversation_id=? AND role='bot' LIMIT 1",
                      (conv_id[0],))
            first_bot_response = c.fetchone()
            if first_bot_response:
                if st.sidebar.button(" ".join(first_bot_response[0].split()[0:5])):
                    display_conversation(conv_id[0])

        # Sidebar (left side) - Clear Chat History button
        if st.sidebar.button("Clear Chat History ✖️"):
            st.session_state.chat_history.clear()
            c.execute("DELETE FROM chat_history")
            conn.commit()

        # Main content area (center)
        st.markdown("---")

        user_input = st.chat_input("Ask Anything ...")

        if user_input:
            try:
                bot_response = get_bot_response(user_input, internal_model, provider_name)

                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "bot", "content": bot_response})

                for chat in st.session_state.chat_history:
                    c.execute("INSERT INTO chat_history VALUES (?, ?, ?)",
                    (st.session_state.conversation_id, chat["role"], chat["content"]))
                    conn.commit()

                # Display chat history
                for index, chat in enumerate(st.session_state.chat_history):
                    with st.chat_message(chat["role"]):
                        if chat["role"] == "user":
                            st.markdown(chat["content"])
                        elif chat["role"] == "bot":
                            st.markdown(chat["content"])

            except Exception as e:
                st.error(f"An error occurred: {e}")

    except Exception as e:
        st.error(f"An error occurred: {e}")


def display_conversation(conversation_id):
    c.execute("SELECT * FROM chat_history WHERE conversation_id=?", (conversation_id,))
    chats = c.fetchall()
    st.markdown(f"### Conversation")
    for chat in chats:
        st.markdown(f"{chat[1]}")
        st.markdown(f"{chat[2]}")


if __name__ == "__main__":
    main()

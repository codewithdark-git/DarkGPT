import streamlit as st
from g4f.client import Client
import sqlite3
import subprocess
import pyttsx3
import os
from cookies import *
from undetected_chromedriver import *

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


def copy(text):
    """
    Copy text to clipboard on Windows.

    Parameters:
    text (str): The text to copy to the clipboard.

    Returns:
    bool: True if the text was successfully copied, False otherwise.
    """
    try:
        subprocess.run(['clip'], input=text.strip().encode('utf-16'), check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error: Unable to copy text to clipboard on Windows.")
        return False


# Streamlit app
def main():

    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = 1

        models = {
            "🚀Airoboros 70B": "airoboros-70b",
            "⚡GPT-4 Turbo": "gpt-4-turbo"
        }

        columns = st.columns(3)  # Split the layout into three columns
        with columns[0]:
            st.header("DarkGPT")

        with columns[2]:
            selected_model_display_name = st.selectbox("Select Model", list(models.keys()), index=0)

        with columns[1]:
            selected_model = models[selected_model_display_name]

        # Sidebar (left side) - New chat button
        if st.sidebar.button("✨New Chat", key="new_chat_button"):
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
        if selected_model == "gpt-4-turbo":
            with st.chat_message("bot"):
                st.markdown("Working with this model used the default model for generation.")

        user_input = st.chat_input("Ask Anything ...")

        # Listen for changes in user input and generate completion
        if user_input:
            client = Client()
            response = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": "user", "content": user_input}],
            )
            bot_response = response.choices[0].message.content

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "bot", "content": bot_response})

            # Store chat in the database
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
                    col1 = st.columns(10)
                    with col1[0]:
                        copy_button = f"text_copy_{index}"
                        if st.button('📋', key=copy_button):
                            copy(chat["content"])  # Assuming chat["content"] contains the text to copy

                    # Add a speak button in the second column
                    with col1[1]:
                        speak_button = f"text_regenerate_{index}"
                        if st.button('🔊', key=speak_button):
                            engine = pyttsx3.init()
                            engine.say(chat["content"])
                            engine.runAndWait()




    except Exception as e:
        st.error(f"An error occurred: {e}")

    except TimeoutError:
        st.error("Check Your Internet Connection:")

    except ConnectionError:
        st.error("Check Your Internet Connection:")

    except RuntimeError:
        st.error("Check Your Internet Connection:")

def display_conversation(conversation_id):
    c.execute("SELECT * FROM chat_history WHERE conversation_id=?", (conversation_id,))
    chats = c.fetchall()
    st.markdown(f"### Conversation")
    for chat in chats:
        st.markdown(f"{chat[1]}")
        st.markdown(f"{chat[2]}")

if __name__ == "__main__":
    main()

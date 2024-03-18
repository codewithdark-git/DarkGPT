import streamlit as st
from g4f.client import Client
import sqlite3
import clipboard
import os
from cookies import *
from undetected_chromedriver import *

# Open the clipboard and get data
# win32clipboard.OpenClipboard()
# data = win32clipboard.GetClipboardData()
# win32clipboard.CloseClipboard()

# Disable pyperclip fallback
os.environ["PYPERCLIP_FALLBACK"] = "disabled"

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

# Streamlit app
def main():
    # Apply custom CSS styles
    st.write(
        """
        <style>
        .stButton>button {
            position: relative;
            max-height: 30px;
            min-width: 250px;
            padding: auto;
            margin: -3px -3px;
            border: none;
            border-radius: 10px ;
            # background-color: #4CAF50 ;
            color: white ;
            font-size: 5px;
            font-width: ;
            cursor: pointer;
            # box-sizing: border-box
        }
        .stButton>button:hover {
            background-color: #000000 !important;
            color: #00CED1;
            # border: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "conversation_id" not in st.session_state:
            st.session_state.conversation_id = 1

        models = {
            "Airoboros 70B": "airoboros-70b",
            "GPT-4 Turbo": "gpt-4-turbo"
        }

        columns = st.columns(3)  # Split the layout into three columns
        with columns[0]:
            st.header("DarkGPT")

        with columns[2]:
            selected_model_display_name = st.selectbox("Select Model", list(models.keys()), index=0)

        with columns[1]:
            selected_model = models[selected_model_display_name]

        # Sidebar (left side) - New chat button
        if st.sidebar.button("New Chat", key="new_chat_button"):
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
        if st.sidebar.button("Clear Chat History"):
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
                    button_key_copy = f"text_copy_{index}"  # Unique key for each copy button
                    button_key_regenerate = f"text_regenerate_{index}"  # Unique key for each regenerate button
                    if st.button('📋 Copy', key=button_key_copy):
                        clipboard.copy(chat["content"])



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

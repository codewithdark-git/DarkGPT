import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="DarkGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"

)

def display_homepage():
    st.markdown("<h1 style='text-align: center; color: white; font-size: 36px;'>Welcome to DarkGPT! 🧨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size: 56px;'>🤖</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size: 20px;'>DarkGPT: Your AI text assistant for quick summarization and analysis. Summarize text, analyze complexity, and get insights instantly!</h3>", unsafe_allow_html=True)

    st.markdown('---')

    st.markdown("<h3 style='text-align: left; color:#F63366; font-size: 24px;'><b>What is DarkGPT?</b></h3>", unsafe_allow_html=True)
    st.markdown("""
        DarkGPT is a versatile AI-powered text assistant designed to enhance your reading and writing experience. 
        Leveraging advanced natural language processing models, DarkGPT provides two main functionalities:
        text summarization and text analysis. Whether you need to quickly understand the essence of a lengthy article or 
        dive deep into the complexity of a text, DarkGPT is here to help.
    """)

    st.markdown("<h3 style='text-align: left; color:#F63366; font-size: 24px;'><b>Features</b></h3>", unsafe_allow_html=True)

    st.markdown("### 🤖 DarkGPT - AI-Powered Chatbot:\n"
                "DarkGPT is an advanced AI-powered chatbot designed to simulate human-like conversations.\n"
                "Using state-of-the-art natural language processing models, DarkGPT can understand and generate\n"
                "responses based on user input, making it ideal for various applications such as customer support,\n"
                "virtual assistants, and interactive content generation.\n\n"
                "DarkGPT supports multiple AI models, each tailored for different tasks and levels of complexity.\n"
                "Users can select from a range of models, including those optimized for general chat, technical queries,\n"
                "creative writing, and more, providing flexibility and customization to suit specific needs.\n\n"
                "**Key Features:**\n"
                "- **AI Models:** Utilizes models like Airoboros 70B and Gemini Pro for robust conversation handling.\n"
                "- **Natural Language Processing:** Processes user input to generate contextually relevant responses.\n"
                "- **Chat History:** Stores and retrieves chat history to maintain continuity across sessions.\n"
                "- **Customization:** Offers options to fine-tune responses and personalize user interaction.\n\n"
                "Explore DarkGPT's capabilities and start conversing today!", unsafe_allow_html=True)

    st.markdown("### 🔍 Summarization Page:\n"
                "- **Input Options:** Users can input text directly or upload a text file for summarization.\n"
                "- **Example Text:** An example text is provided to help users get started quickly.\n"
                "- **Summarize Button:** Click the 'Summarize' button to generate a summary using the BART model.\n"
                "- **Error Handling:** Error messages are displayed if the input text length requirements are not met.", unsafe_allow_html=True)

    st.markdown("### 📊 Analysis Page:\n"
                "- **Input Options:** Users can input text directly or upload a text file for analysis.\n"
                "- **Example Text:** An example text is provided to help users get started quickly.\n"
                "- **Analyze Button:** Click the 'Analyze' button to generate various metrics such as reading time, text complexity, lexical richness, and number of sentences.\n"
                "- **Error Handling:** Error messages are displayed if the input text length requirements are not met.", unsafe_allow_html=True)

    footer = '''
    <footer style="text-align: center; margin-top: 50px; font-family: Arial, sans-serif; color: #555;">
        <p>Developed by DarkCoder</p>
        <p>
            <a href="https://github.com/codewithdark-git" target="_blank" style="text-decoration: none; color: #007bff; margin-right: 10px;">GitHub</a>
            | <a href="https://www.linkedin.com/in/codewithdark/" target="_blank" style="text-decoration: none; color: #007bff; margin-right: 10px;">Linkedin</a>
            | <a href="https://www.facebook.com/codewithdark.fb/" target="_blank" style="text-decoration: none; color: #007bff;">Facebook</a>
        </p>
    </footer>
    '''

    # Display the footer
    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    display_homepage()

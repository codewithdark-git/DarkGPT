import streamlit as st
import time
from io import StringIO
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import readtime
import textstat
from transformers import pipeline

st.set_page_config(page_title="DarkGPT", page_icon="random", layout="wide", initial_sidebar_state="expanded")


# Function to summarize text using BART model
def summarize_text(input_text):
    summarizer = pipeline("summarization")
    summarized_text = summarizer(input_text, max_length=10050, min_length=50, do_sample=False)[0]['summary_text']
    return summarized_text

# Function to analyze text and return metrics
def analyze_text(input_text):
    nltk.download('punkt')
    tokenized_words = word_tokenize(input_text)
    reading_time = readtime.of_text(input_text)
    text_complexity = textstat.flesch_reading_ease(input_text)
    lexical_richness = len(set(tokenized_words)) / len(tokenized_words)
    num_sentences = len(sent_tokenize(input_text))
    analysis_results = {
        'reading_time': reading_time,
        'text_complexity': text_complexity,
        'lexical_richness': lexical_richness,
        'num_sentences': num_sentences
    }
    return analysis_results

# Function to display the homepage
def display_homepage():
    st.markdown("<h1 style='text-align: center; color: white; font-size:28px;'>Welcome to DarkGPT!🧨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size:56px;'<p>🤖</p></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>DarkGPT: Your AI text assistant for quick summarization and analysis. Summarize text, analyze complexity, and get insights instantly.!</h3>", unsafe_allow_html=True)
    st.page_link(page='app.py', label='Back to Home', icon='🏠')
    st.page_link(page='pages/DarkGPT.py', label='DarkGPT', icon='📝')
    st.markdown('___')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
    st.write("The provided code is a Streamlit web application named 'DarkGPT' that allows users to summarize and analyze text. Here's an overview of each page and the footer mentioning the author:")
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>Display Functionality:<b></h3>", unsafe_allow_html=True)

    st.markdown("Homepage:\n"
                "- Displays a welcome message and introduction to the DarkGPT app.\n"
                "- Provides information about the purpose and target audience of the app.\n"
                "- Users are encouraged to explore the app's features and contribute to its open-source development on GitHub.")

    st.markdown("Summarization Page:\n"
                "- Allows users to input text or upload a file for summarization.\n"
                "- Users can choose between inputting text directly or uploading a file.\n"
                "- Provides an example text for users to test.\n"
                "- After input, users can click the 'Summarize' button to generate a summary using the BART model.\n"
                "- Error messages are displayed if input text length requirements are not met.")

    st.markdown("Analysis Page:\n"
                "- Similar to the Summarization page, but focuses on analyzing text.\n"
                "- Users can input text or upload a file for analysis.\n"
                "- Provides an example text for users to test.\n"
                "- After input, users can click the 'Analyze' button to generate various metrics such as reading time, text complexity, lexical richness, and number of sentences.\n"
                "- Error messages are displayed if input text length requirements are not met.")

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

# Function to display the text summarization page
def display_summarization_page():
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with DarkGPT &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:28px;'>Summarize</h3>", unsafe_allow_html=True)
    st.text('')

    source = st.radio("How would you like to start? Choose an option below", ("I want to input some text", "I want to upload a file"))
    st.text('')

    s_example = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans or animals. Leading AI textbooks define the field as the study of 'intelligent agents': any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term 'artificial intelligence' to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving, however this definition is rejected by major AI researchers. AI applications include advanced web search engines, recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri or Alexa), self-driving cars (such as Tesla), and competing at the highest level in strategic game systems (such as chess and Go). As machines become increasingly capable, tasks considered to require intelligence are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology."

    if source == 'I want to input some text':
        input_su = st.text_area("Use the example below or input your own text in English (between 1,000 and 10,000 characters)", value=s_example, max_chars=10000, height=330)
        if st.button('Summarize'):
            if len(input_su) < 50:
                st.error('Please enter a text in English of minimum 1,000 characters')
            else:
                # Call the summarization function
                summarized_text = summarize_text(input_su)
                st.success(summarized_text)
                st.balloons()

    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here', type=['txt'])
        if file is not None:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            if len(string_data) < 50 or len(string_data) > 10000:
                st.error('Please upload a file between 50 and 10,000 characters')
            else:
                # Call the summarization function
                summarized_text = summarize_text(string_data)
                st.success(summarized_text)
                st.balloons()

# Function to display the text analysis page
def display_analysis_page():
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with DarkGPT &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:28px;'>Analyze</h3>", unsafe_allow_html=True)
    st.text('')

    a_example = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans or animals. Leading AI textbooks define the field as the study of 'intelligent agents': any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term 'artificial intelligence' to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving, however this definition is rejected by major AI researchers. AI applications include advanced web search engines, recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri or Alexa), self-driving cars (such as Tesla), and competing at the highest level in strategic game systems (such as chess and Go). As machines become increasingly capable, tasks considered to require intelligence are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology."

    source = st.radio("How would you like to start? Choose an option below", ("I want to input some text", "I want to upload a file"))
    st.text('')

    if source == 'I want to input some text':
        input_me = st.text_area("Use the example below or input your own text in English (maximum of 10,000 characters)", max_chars=10000, value=a_example, height=330)
        if st.button('Analyze'):
            if len(input_me) > 10000:
                st.error('Please enter a text in English of maximum 10,000 characters')
            else:
                # Call the text analysis function
                analysis_results = analyze_text(input_me)
                st.write('Reading Time:', analysis_results['reading_time'])
                st.write('Text Complexity:', analysis_results['text_complexity'])
                st.write('Lexical Richness:', analysis_results['lexical_richness'])
                st.write('Number of Sentences:', analysis_results['num_sentences'])
                st.balloons()

    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here', type=['txt'])
        if file is not None:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            if len(string_data) > 10000:
                st.error('Please upload a file of maximum 10,000 characters')
            else:
                # Call the text analysis function
                analysis_results = analyze_text(string_data)
                st.write('Reading Time:', analysis_results['reading_time'])
                st.write('Text Complexity:', analysis_results['text_complexity'])
                st.write('Lexical Richness:', analysis_results['lexical_richness'])
                st.write('Number of Sentences:', analysis_results['num_sentences'])
                st.balloons()

# Main function to run the Streamlit app
def main():
    st.sidebar.header('DarkGPT, I want to :crystal_ball:')
    nav = st.sidebar.radio('', ['Go to homepage', 'Summarize text', 'Analyze text'])

    # Display the navigation options

    if nav == 'Go to homepage':
        display_homepage()
    elif nav == 'Summarize text':
        display_summarization_page()
    elif nav == 'Analyze text':
        display_analysis_page()

if __name__ == "__main__":
    main()

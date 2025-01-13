from langchain_groq import ChatGroq

def process_query(query):
    """
    Process a query using the Groq model and return the response.
    """
    model = ChatGroq(model_name="Llama-3")  # or Mixtral
    response = model.generate(query)
    return response

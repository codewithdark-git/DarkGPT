from langchain.llms import Groq

def process_query(query):
    """
    Process a query using the Groq model and return the response.
    """
    model = Groq(model_name="Llama-3")  # or Mixtral
    response = model.generate(query)
    return response

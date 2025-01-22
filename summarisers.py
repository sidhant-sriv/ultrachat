# Loaders
from langchain.schema import Document

# Splitters
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Model
from langchain_groq import ChatGroq
# Embedding Support
from langchain.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
# Summarizer we'll use for Map Reduce
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
# Data Science
import numpy as np
from sklearn.cluster import KMeans
import os
from langchain_core.prompts import PromptTemplate


load_dotenv()
verbose = False
def large_summariser(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        text = f.read()
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000, chunk_overlap=3000)

    docs = text_splitter.create_documents([text])

    num_documents = len(docs)

    print(f"Now our chat is split up into {num_documents} documents")
    embeddings =  CohereEmbeddings(model="embed-english-v3.0")

    vectors = embeddings.embed_documents([x.page_content for x in docs])

    num_clusters = num_documents//9 + 1


    print(f"Number of clusters {num_clusters}")

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    # Find the closest embeddings to the centroids

    # Create an empty list that will hold your closest points
    closest_indices = []

    # Loop through the number of clusters you have
    for i in range(num_clusters):
        # Get the list of distances from that particular cluster center
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)

        # Find the list position of the closest one (using argmin to find the smallest distance)
        closest_index = np.argmin(distances)

        # Append that position to your closest indices list
        closest_indices.append(closest_index)

    selected_indices = sorted(closest_indices)

    llm = ChatGroq(groq_api_key=os.getenv("GROQ"), model_name="llama-3.1-8b-instant", max_tokens = 1000)

    map_prompt = """You will be given a single passage of a Discord Chat log. This section will be enclosed in triple backticks (```)
    Summarize the summaries capturing all essential details. Include:
Key Points: Critical points, decisions, conclusions.
Important Messages: Significant messages or exchanges.
Context: Relevant references or external content.
Ensure the summary is clear, thorough, and easy to understand, leaving no important details out. Assume the reader is unfamiliar with the conversation.
    ```{text}```
FULL SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

    map_chain = load_summarize_chain(llm=llm,
                                     chain_type="stuff",
                                     prompt=map_prompt_template,
                                     verbose = verbose)

    selected_docs = [docs[doc] for doc in selected_indices]

    # Make an empty list to hold your summaries
    summary_list = []

    # Loop through a range of the lenght of your selected docs
    for i, doc in enumerate(selected_docs):
        # Go get a summary of the chunk
        chunk_summary = map_chain.run([doc])

        # Append that summary to your list
        summary_list.append(chunk_summary)

        print(f"Summary #{i} (chunk #{selected_indices[i]}) - Preview: {chunk_summary[:250]} \n")


    summaries = "\n".join(summary_list)
    # Convert it back to a document
    summaries = Document(page_content=summaries)

    print(f"Your total summary has {llm.get_num_tokens(summaries.page_content)} tokens")

    llm2 = ChatGroq(groq_api_key=os.getenv("GROQ"), model_name="llama-3.3-70b-versatile", max_tokens = 2000)
    combine_prompt = """
    You will be given a series of summaries from a Discord chat log. The summaries will be enclosed in triple backticks (```)
    Summarize the summaries capturing all essential details. Include:

Participants: Key individuals involved.
Topics: Main and subtopics discussed.
Key Points: Critical points, decisions, conclusions.
Important Messages: Significant messages or exchanges.
Context: Relevant references or external content.
Tone and Sentiment: General tone and any shifts in sentiment.
Ensure the summary is clear, thorough, and easy to understand, leaving no important details out. Assume the reader is unfamiliar with the conversation.

    ```{text}```
    VERBOSE SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
    reduce_chain = load_summarize_chain(llm=llm2,
                                        chain_type="stuff",
                                        prompt=combine_prompt_template,
                                        verbose=verbose) # Set this to true if you want to see the inner workings

    output = reduce_chain.run([summaries])
    #print(output)
    return output




if __name__ == "__main__":
    print(large_summariser("sample.txt"))

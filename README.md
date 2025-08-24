Here’s the corrected version of your text with spelling and grammatical mistakes fixed:  

---

[![GDSC VIT](https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only)](https://dscvit.com/)  

## UltraChat  

#### A Discord bot to supercharge your productivity in servers  

[](https://github.com/GDGVIT/template#--insert-project-description-here--)  

This repo contains the code for **UltraChat**, a Discord bot aimed at boosting productivity in highly active Discord servers where keeping up with chat is imperative but difficult to do simultaneously.  

With common Discord bot functionality, such as moderation tools and some fun commands for memes and random interests like cryptography, it also includes features for chat summaries and querying based on all collected chats within a certain server. The summaries are then stored in a database for future use.  

---

### **Summarization**  

The summary engine for this bot is built using **LangChain**, leveraging a mix of **map-reduce** and **clustering** to handle extremely large quantities of text. The summarization engine follows these steps:  

- **Collection**: The text within the chats is collected and passed to the summarization engine.  
- **Chunking**: The text is split into chunks of a given length.  
- **Embedding Generation**: These chunks are processed through an embedding model (**embed-english-v3.0 via Cohere**) to generate their corresponding vector embeddings, which store the semantic meaning of the chunks.  
- **Clustering**: The chunks are clustered via **K-Means clustering** (where every 9 chunks are clustered together, with a maximum of 11; these numbers were chosen somewhat arbitrarily).  
- **Map-Reduce**: The most central chunk of each cluster is chosen as the average of the clusters and summarized individually. All these summaries are then combined and summarized again.  

While this method may result in some loss of detail, making it a poor choice for **needle-in-a-haystack** problems, it is highly efficient for general summarization tasks. By grouping similar text into clusters and selecting the most relevant chunk to summarize, the engine significantly reduces processing time and cost, as less text needs to be handled by the LLM.  

For cases where **specific** questions need to be answered, all stored chats and their respective vector embeddings are stored in a **vector database (ChromaDB)** for quick querying via a **RAG (Retrieval-Augmented Generation) pipeline**. Read more about RAG [here](https://huggingface.co/docs/transformers/en/model_doc/rag).  

The LLMs used are hosted on **Groq**, which provides incredibly high inference speeds. The **LLaMA family of models** was chosen due to their strong performance among open-source models.  

---

## **Installation and Running UltraChat**  

You need to have **Python** installed along with a **Discord developer account**. Visit the [Discord Developer Portal](https://discord.com/developers/applications), create a bot application, and obtain its token.  

Clone the repository using:  
```shell
git clone https://github.com/GDGVIT/ultra-chat-bot.git
cd ultrachat
```

### **1. Configure API Keys**  
Check `.env.example` and obtain all the required API keys:  

- [Hugging Face API](https://huggingface.co/settings/tokens)  
- [Groq API](https://console.groq.com/keys)  
- [Discord API](https://discord.com/developers/applications)  
- [Cohere API](https://dashboard.cohere.com/api-keys)  

### **2. Host UltraChat Backend**  
Ensure that the UltraChat backend is hosted and provide the respective endpoints.  

### **3. Set Up the Environment File**  
Rename `.env.example` to `.env`, which will contain all the required client secrets.  

### **4. Create a Virtual Environment (Recommended)**  
#### **Windows**  
```shell
python -m venv venv
.\venv\Scripts\activate
```
#### **Linux and macOS**  
```shell
source venv/bin/activate
```

### **5. Install Dependencies**  
It is recommended to use **Python >= 3.10**.  
```shell
pip install -r requirements.txt
```

### **6. Run the Main Script**  
```shell
python app.py
```

---

## **Running UltraChat with Docker**  

### **1. Install Docker**  
Ensure Docker is installed on your system.  

### **2. Configure Credentials**  
Make sure all credentials are properly set in the `.env` file as described earlier.  

### **3. Build and Run Using Docker Compose**  
```shell
docker-compose build
docker-compose up
```

---

### **Getting Started**  

Once the bot is running, obtain the bot's invite link (OAuth2 URL) from the **Discord Developer Portal**, invite it to your server, and run the `!help` command to get a list of available commands and start using **UltraChat**! 🚀

## Contributors
---
<table>
	<tr align="center">
		<td>
		Noel Alex
		<p align="center">
			<img src = "https://avatars.githubusercontent.com/u/79050483?v=4" width="150" height="150">
		</p>
			<p align="center">
				<a href = "https://github.com/Noel-alex">
					<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36" alt="GitHub"/>
				</a>
				<a href = "https://www.linkedin.com/in/noel-alex-b1731128b/">
					<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36" alt="LinkedIn"/>
				</a>
			</p>
		</td>
	<tr align="center">
		<td>
		Sidhant Srivastava
		<p align="center">
			<img src = "https://avatars.githubusercontent.com/u/66166455?v=4" width="150" height="150">
		</p>
			<p align="center">
				<a href = "https://github.com/sidhant-sriv">
					<img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36" alt="GitHub"/>
				</a>
				<a href = "https://www.linkedin.com/in/sidhant-srivastava-41803620b/">
					<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36" alt="LinkedIn"/>
				</a>
			</p>
		</td>
</table>

<p align="center">
	Made with ❤ by <a href="https://dscvit.com">GDSC-VIT</a>
</p>

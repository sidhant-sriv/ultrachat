[![GDSC VIT](https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only)](https://dscvit.com/)

## UltraChat


#### A Discord bot to supercharge your productivity in servers

[](https://github.com/GDGVIT/template#--insert-project-description-here--)
This repo contains the code for the ultrachat, a discord bot aimed at boosting productivity in highly active discord servers where keeping up with the chat is imperative however difficult to do so at the same time. 

With common discord bot functionality, like moderation tools and some fun commands for memes and random interests like cryptography, it also contains functions for chat summaries and querying based on all collected chats within a certain server. The summaries are then stored in a database for future use.

###### Summarisation:
The summary engine for this bot is written using langchain using a mix of map-reduce and clustering to handle extremely large quantities of text, the summarisation engine follows the given steps

- **Collection**: The text within the chats is collected and passed to the summarisation engine.
- **Chunking**: The text is then split into chunks with a given length.
- **Embedding Generation**: These chunks are then passed through an embedding model (embed-english-v3.0 via Cohere in this case) to generate their corresponding vector embeddings (which store the semantic meaning of these chunks).
- **Clustering**:These chunks are then clustered via Kmeans clustering (where every 9 chunks are clustered together in this case to a maximum of 11, these numbers were chosen somewhat arbitrarily).
- **Map Reduce**: The most central chunks of every cluster is then chosen as the average of these clusters and summarised individually, and all these summaries are then summarised once more.

We do lose some details mentioned within the give text, thereby making it a poor choice for needle in a hay stack problems, however for summarisation tasks, the ability to generalise a lot of text with similar meaning into clusters and choosing the best chunk of text to summarise, enables the engine to massively reduce the time to generate a given summary, as less text is processed by the llm, leading to lower costs, and massive speed ups.

However for cases when more specific questions need to be answered, all the stored chats along with their respective vector embeddings are stored in a vector store (chromadb) for quick querying via a RAG pipeline. Read more about RAG [here](https://huggingface.co/docs/transformers/en/model_doc/rag)

The llms used are hosted on Groq which provides increadibly high inference speeds, and the llama family of models were used for most of our tasks due to them being some of the best performing open source models currently available.


# Installation and running UltraChat
---
You need to have Python installed along with a developer account on discord. Visit their developer's portal and create a bot application and get it's token. Clone the repository using 
- `git clone https://github.com/GDGVIT/ultra-chat-bot.git` 
- `cd ultrachat`

1. check .env.example and get all the required api keys 
	- [HuggingFace api](https://huggingface.co/settings/tokens)
	- [Groq api](https://console.groq.com/keys)
	- [Discord api](https://discord.com/developers/applications)
	- [Cohere api](https://dashboard.cohere.com/api-keys)

2. Host Ultra-chat-backend and provide the respective endpoints

3. Remove the .example from the end of the filename, and this will contain all client secrets for your projects
 
4. It is recommended to create a python virtual environment 
- Windows
 ```shell
 python -m venv venv
 .\venv\Scripts\activate
```
- Linux and MacOS
```shell
source myenv/bin/activate
```

5. Install the project dependencies using (It is recommended to use python >=3.10)
```shell
pip3 install requirements.txt

```
6. Run the main script
```shell
python app.py
```
# Run using Docker

1. Install Docker

2. Make sure all the credentials are available in the .env file as described above

3. Run the command
```shell
docker-compose build
docker-compose up
```

Get the Bot invite link (OAuth2 URL) from your discord developer portal, invite the bot into a server and run the !help command to get a list of commands and start using UltraChat


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
		Sidhant Srivastav
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
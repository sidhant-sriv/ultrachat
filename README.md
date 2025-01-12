[![GDSC VIT](https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only)](https://dscvit.com/)

## UltraChat


#### A Discord bot to supercharge your productivity in servers



# Installation and running UltraChat
---
You need to have Python installed along with a developer account on discord. Visit their developer's portal and create a bot application and get it's token.

1. check .env.example and get all the required api keys 
	- [HuggingFace api](https://huggingface.co/settings/tokens)
	- [Groq api](https://console.groq.com/keys)
	- [Discord api](https://discord.com/developers/applications)

2. Host Ultra-chat-backend and provide the respective endpoints

3. Remove the .example from the end of the filename, and this will contain all client secrets for your projects
 
4. It is recommended to create a python virtual environment using 
 ```shell
 python -m venv venv
 .\venv\Scripts\activate
 
```

5. Install the project dependencies using (It is recommended to use python >=3.10)
```shell
pip3 install requirements.txt

```
6. Run the main script
	```shell
	python app.py
```
## Run using Docker

1. Install Docker

2. Make sure all the credentials are available in the .env file as described above

3. Run the command
```shell
docker-compose up
```

Get the Bot invite link (OAuth2 URL) from your discord developer portal, invite the bot into a server and run the !help command to get a list of commands and start using UltraChat


## Contributors
---

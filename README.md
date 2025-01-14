[![GDSC VIT](https://user-images.githubusercontent.com/56252312/159312411-58410727-3933-4224-b43e-4e9b627838a3.png#gh-light-mode-only)](https://dscvit.com/)

## UltraChat


#### A Discord bot to supercharge your productivity in servers

[](https://github.com/GDGVIT/template#--insert-project-description-here--)
This repository contains the the code for the the discord bot Ultra-Chat. 

# Installation and running UltraChat
---
You need to have Python installed along with a developer account on discord. Visit their developer's portal and create a bot application and get it's token. Clone the repository using 
- `git clone https://github.com/GDGVIT/UltraChat.git` 
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
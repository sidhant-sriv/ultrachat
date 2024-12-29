import requests
import os
import dotenv
dotenv.load_dotenv()




def create_summary(data):
    url = os.getenv("CREATE_SUMMARY_URL")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.json())

    return response.json()


def get_summaries(id, server_id):
    url = os.getenv("GET_SUMMARY_URL")
    params = {"user_id": str(id), "server_id": str(server_id)}
    response = requests.get(url, params=params)
    print(response.status_code, response.json())

    return response.json()

def update_summary(data):
    url = os.getenv("UPDATE_SUMMARY_URL")
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, headers=headers, json=data)
    print(response.status_code, response.json())

    return response.json()


def del_summary(id, server_id):
    url = os.getenv("DELETE_SUMMARY_URL")
    params = {"user_id": str(id), "server_id": str(server_id) }
    response = requests.get(url, params=params)
    print(response.status_code, response.json())

    return response.json()

data =  {
    "content": "This is a sample summary",
    "server_id": "1234",
    "is_private": True,
    "user_id": "803431354406010920"
}

summary = create_summary(data)
print(summary)
summaries = get_summaries(data["user_id"], data["server_id"])
print(summaries)
summary = del_summary(data["user_id"], data["server_id"])
print(summary)




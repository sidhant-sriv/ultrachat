import requests
import os
import dotenv
dotenv.load_dotenv()




def create_summary(data:dict):
    '''
    data : {
                "content": str(summary),
                "server_id": str(ctx.message.guild.id),
                "is_private": True if str(ctx.message.type) == 'private' else False,
                "user_id": str(ctx.author.id)
            }
    stores this data using mongodb on backend server
    '''
    print("sending data to server")
    url = os.getenv("CREATE_SUMMARY_URL")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.json())

    return response


def get_summaries(id, server_id):
    '''
        id:str = ctx.author.id
        server_id:str = ctx.guild.id
    '''

    print("getting summaries")
    url = os.getenv("GET_SUMMARY_URL")
    headers = {"ID": str(id)}
    params = {"user_id": str(id), "server_id": str(server_id)}
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code, response.json())

    return response

def update_summary(data):
    '''
            data : {
                "content": str(summary),
                "server_id": str(ctx.message.guild.id),
                "is_private": True if str(ctx.message.type) == 'private' else False,
                "user_id": str(ctx.author.id)
            }
    updates data on backend server
    '''
    url = os.getenv("UPDATE_SUMMARY_URL")
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, headers=headers, json=data)
    print(response.status_code, response.json())

    return response


def del_summary(summary_id:str, id):
    print("deleting summary")
    url = os.getenv("DELETE_SUMMARY_URL")
    headers = {"ID": str(id)}
    request = {"summary_id": str(summary_id)}
    response = requests.delete(url, json=request, headers=headers)
    print(response.status_code, response.json())

    return response




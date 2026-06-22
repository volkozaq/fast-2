# client.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# print("--- Creating user ---")
# response = requests.post(
#     f'{BASE_URL}/user',
#     json={"username": "testuser", "password": "test password"}
# )
# print(f'Status: {response.status_code}')
# if response.status_code == 200:
#     user_data = response.json()
#     print(f'User created with id: {user_data["id"]}')
# else:
#     print(f'Error: {response.text}')
#     exit()

# print("\n--- Logging in ---")
# response = requests.post(
#     f'{BASE_URL}/login',
#     json={"username": "testuser3", "password": "4567"}
# )
# print(f'Status: {response.status_code}')
# if response.status_code == 200:
#     token_data = response.json()
#     print(f'Got token: {token_data["token"]}')
#     USER_TOKEN = token_data["token"]
# else:
#     print(f'Error: {response.text}')
#     exit()
#
# print("\n--- Updating user ---")
# resp = requests.patch(
#     f'{BASE_URL}/user/{token_data["id"]}',
#     json={"username": "test users new name"}
# )
# print(f'Status: {response.status_code}')
# if response.status_code == 200:
#     user_data = response.json()
#     print(user_data)
# else:
#     print(f'Error: {response.text}')
#     exit()
#
# print(f'Token data: {token_data}')
# print(f' User data: {user_data}')
# print("\n--- Creating advert ---")
# response = requests.post(
#     f'{BASE_URL}/advertisement/',
#     json={"title": "Test advert", "description": "Test description", "author": token_data["id"],"price": 2},
#     headers={"x-token": USER_TOKEN}
# )
# if response.status_code == 200:
#     advert_data = response.json()
#     print(f'Advert created with id: {advert_data["id"]}')
# else:
#     print(f'Error: {response.text}, {response.status_code}')
#     exit()
#
#
# print("\n--- Getting Ad by ID ---")
# response = requests.get(
#     f'{BASE_URL}/advertisement/{advert_data["id"]}',
#     headers={"x-token": USER_TOKEN}
# )
# if response.status_code == 200:
#     advert_data = response.json()
#     print(f'Advert created with id: {advert_data["id"]}')
#     print(f'advert data: {advert_data}')
# else:
#     print(f'Error: {response.text}, {response.status_code}')
#     exit()














# print("\n--- Acting as testuser4 ---")
# create_response = requests.post(
#     f'{BASE_URL}/user',
#     json={"username": "testuser2", "password": "1234"}
# )
# print(f'Create user 4 status: {create_response.status_code}')
resp = requests.post(
    f'{BASE_URL}/login',
    json={"username": "testuser7", "password": "4567"}
)
print(resp.json())
user1_token = resp.json()['token']
user1_id = resp.json()['user_id']
print(user1_id)

resp = requests.post(
    f'{BASE_URL}/advertisement',
    json={"title": "Test advert", "description": "Test description","author_id": user1_id, "price": 2},
    headers={"x-token": user1_token}
)
print(resp.json())
ad_id = resp.json()['id']

resp = requests.get(
    f'{BASE_URL}/advertisement/{ad_id}',

)
print(resp.json())

resp = requests.post(
    f'{BASE_URL}/login',
    json={"username": "admin", "password": "admin"}
)
print(resp.json())
new_tok = resp.json()['token']
new_id = resp.json()['user_id']

print(f'admin:')
resp = requests.get(
    f'{BASE_URL}/user/{new_id}'
)
print(resp.json())

resp = requests.patch(
    f'{BASE_URL}/advertisement/{ad_id}',
    json={"title": "New advert"},
    headers={"x-token": new_tok}
)
print(resp.json())

print(f'New user tries to update user1')
resp = requests.get(
    f'{BASE_URL}/advertisement/{ad_id}',

)
print(resp.json())

resp = requests.delete(
    f'{BASE_URL}/advertisement/{ad_id}',
    headers={"x-token": new_tok}
)
print(resp.json())


resp = requests.get(
    f'{BASE_URL}/advertisement/{ad_id}',

)
print(resp.json())


print(f'Admin tries to update user1')
resp = requests.patch(
    f'{BASE_URL}/user/{user1_id}',
    json={"username": "testuser7"},
    headers={"x-token": new_tok}
)
print(resp.json())

print(f'Updated user:')
resp = requests.get(
    f'{BASE_URL}/user/{user1_id}'
)
print(resp.json())

print("Admin tries to delete")
resp = requests.delete(
    f'{BASE_URL}/user/{user1_id}',
    headers={"x-token": new_tok}
)
print(f'Status: {resp.status_code}')
if resp.status_code == 200:
    user_data = resp.json()
    print(user_data)
else:
    print(f'Error: {resp.text}')
print(f'Status: {resp.status_code}')

print(f'Updated user:')
resp = requests.get(
    f'{BASE_URL}/user/{user1_id}'
)
print(resp.json())

# print("\n--- Getting Ad by fields---")
# response = requests.get(
#     f'{BASE_URL}/advertisement/?search_data=advert'
#
# )
# if response.status_code == 200:
#     advert_data = response.json()
#     print(f'advert data: {advert_data}')
# else:
#     print(f'Error: {response.text}, {response.status_code}')
#     exit()


# resp = requests.post(
#     f'{BASE_URL}/login',
#     json={"username": "testuser2", "password": "1234"}
# )
# print(resp.json())
# new_tok = resp.json()['token']
# new_id = resp.json()['user_id']
# print(new_id)
#
# resp = requests.delete(
#     f'{BASE_URL}/advertisement/{ad_id}',
#     headers={"x-token": new_tok}
# )
# print(resp.json())

#
# resp = requests.patch(
#     f'{BASE_URL}/advertisement/{ad_id}',
#     json={"title": "New advert"},
#     headers={"x-token": new_tok}
# )
# print(resp.json())
# user4_ad_id = resp.json()["id"]
# print(f'User4 created ad with id: {user4_ad_id}')

# print("\n--- Acting as new user ---")
# resp = requests.post(
#     f'{BASE_URL}/user',
#     json={"username": "new_user", "password": "test4"}
# )
# print(f'New user created. Status: {resp.status_code}')


#
# print(f'New user tries to update user1')
# resp = requests.get(
#     f'{BASE_URL}/advertisement/{ad_id}',
#
# )
# print(resp.json())

# resp = requests.delete(
#     f'{BASE_URL}/user/{user1_id}',
#     headers={"x-token": new_tok}
# )
# print(f'Status: {resp.status_code}')
# if resp.status_code == 200:
#     user_data = resp.json()
#     print(user_data)
# else:
#     print(f'Error: {resp.text}')
# print(f'Status: {resp.status_code}')
#
# if resp.status_code == 403:
#     print("Success!!! Access denied as expected")
# else:
#     print(f'Something went wrong: {resp.text}')
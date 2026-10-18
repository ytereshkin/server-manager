import paramiko
import getpass
import os
import json
from cryptography.fernet import Fernet

def get_or_create_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as file:
            key = file.read()
        return key
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as file:
            file.write(key)
        return key
    
def save_credentials(host, user, password, port):
    data = {
        "host":host,
        "user":user,
        "password":password,
        "port":port    
    }   
    
    json_data = json.dumps(data)
    bytes_data = json_data.encode()
    key = get_or_create_key()
    chipher = Fernet(key)
    encrypted_data = chipher.encrypt(bytes_data)
    
    with open("cred.enc", "wb") as file:
        file.write(encrypted_data)

def load_credentials():
    with open("cred.enc","rb") as file:
        encrypted_data  = file.read()
    key = get_or_create_key()
    chipher = Fernet(key)
    decode_data = chipher.decrypt(encrypted_data).decode()
    data = json.loads(decode_data)
    return data 

def connect_to_server(host, user, password, port):    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password, port=port)
    
    return client

def execute_command(client,cmd):
    _, output, error = client.exec_command(cmd) 
    output = output.read().decode()
    error = error.read().decode()
    return  output, error
    
if os.path.exists("cred.enc"):
    data = load_credentials()
    host = data["host"]
    user = data["user"]
    password = data["password"]
    port = data["port"]
else:
    print("please write credential information:")
    
    host = input("Host: ")
    user = input("User: ")
    password = getpass.getpass("Password: ")
    port = 22

client = None
try:   
    client = connect_to_server(host,user,password,port)    
    save_credentials(host,user,password,port)
    
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        if not cmd:
            continue        
        output, error = execute_command(client,cmd)
        if output:
            print(output)
        if error:
            print(error)
    
except paramiko.AuthenticationException:    
    print("Credentials error ")
    
except Exception as e:
    print(f"Unexpected error: {e}")
   
finally:   
    if client:
        client.close()
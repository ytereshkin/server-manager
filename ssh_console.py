import paramiko
import getpass

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
    

host = input("Host: ")
user = input("User: ")
password = getpass.getpass("Password: ")
port = 22

client = None
try:   
    client = connect_to_server(host,user,password,port)    
    
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
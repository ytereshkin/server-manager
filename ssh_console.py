import paramiko
import getpass

host = input("Host: ")
user = input("User: ")
password = getpass.getpass("Password: ")
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:    
   
    client.connect(hostname=host, username=user, password=password, port=port)
    while True:
        cmd = input("> ")
        if cmd == "exit":
            break
        if not cmd:
            continue        
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
except paramiko.AuthenticationException:    
    print("Credentials error ")
    
except Exception as e:
    print(f"Unexepected error: {e}")
   
finally:   
    client.close()
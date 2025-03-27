

import socket,mysql.connector

import id_


def db_connection():

    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='train'

    )
    return conn


def extract_body_from_request(request):

    
        body=[]

        request=request.split('\n')
        # print("here\n",request)
        i=len(request)-1

        while i>=0 and request[i]!='\r':

            body.insert(0,request[i])
            i-=1
        
        
        x=body[0].split('&')
        name=x[0][5::].replace('+',' ')
        
        password=x[1][5::].replace('+',' ')

        return name,password







server_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_skt.bind(('localhost', 5000))
server_skt.listen(5)



index_file=""

with open("index.html",'r') as f:
    index_file=f.read()


index_response=html_response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n

{index_file}
""".encode()


create_account=""

with open("create_account.html",'r') as f:
    create_account=f.read()


account_response=f"""HTTP/1.1 200 OK \r\nContent-Type: text/html\r\n\r\n

{create_account}
""".encode()


insert_response=f"""HTTP/1.1 200 OK \r\nContent-Type: text/plane\r\n\r\n
done
""".encode()



check_response1=f"""HTTP/1.1 200 OK \r\nContent-Type: text/plane\r\n\r\n
exist
""".encode()

check_response0=f"""HTTP/1.1 200 OK \r\nContent-Type: text/plane\r\n\r\n
not exist
""".encode()

while True:  

    # moving the connection from the accept q of the socket to be a independent entity (connection) 
    client_skt, client_address = server_skt.accept()


    print(f"Connection accepted from {client_address}")

    

    request=client_skt.recv(1024).decode()

    
    route,method="",""

    if len(request):
        method=request.split()[0]
        route=request.split()[1]
    

    if method=='GET' and (route=='/' or route=='/index'):

        client_skt.send(index_response)

  


    elif method=='GET' and route=='/create_account':

        client_skt.send(account_response)
    

    elif method=="POST" and route=="/insert":
        

        
        name,password=extract_body_from_request(request)
        
        
        
        # insert in the data base 

        conn=db_connection()

        cursor=conn.cursor()

        query="insert into info (id,name,pass) values (%s,%s,%s)"

        res=cursor.execute(query,(id_.id,name,password))
        id_.id+=1
        conn.commit()

        print("res is ",res)

        client_skt.send(insert_response)
        cursor.close()
        conn.close()
        

    

    elif method=='POST' and route=='/check':

        name,password=extract_body_from_request(request)

        conn=db_connection()

        cursor=conn.cursor()

        query="select * from info where name=%s and pass=%s"

        cursor.execute(query,(name,password))

        res=cursor.fetchall()


        if len(res):

            client_skt.send(check_response1)

        else:
            client_skt.send(check_response0)





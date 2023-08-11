import socket
import ssl
from cryptography.fernet import Fernet
import pastesAPI.read as read



#in questa funzione leggiamo il contenuto criptato del pastes tramite lo slug(parte finale dell'url pastes in gergo discriminante es: https://pastes.io/QZB5yVjdpH il discriminante QZB5yVjdpH 
def readPastesContent(slug):
    cryptedPastes = read.readPastes(slug) 

    encryptedContent = cryptedPastes["success"]["content"] #assegna a questa variabile il contenuto criptato del pastes 

    print("\t encrypted content read from pastes\n", encryptedContent)
    print("\n---------------------------------------------\n")

    decryptedContent = cipher_suite.decrypt(encryptedContent) #decripto il contenuto del pastes
    decryptedContent = decryptedContent.decode() #print contenuto decriptato
    print("\t decrypted content read from pastes\n", decryptedContent)
    print("\n---------------------------------------------\n")

    save_data(decryptedContent) #uso la funzione save_data per salvare il contenuto decriptato in un file



def save_data(contenuto_decriptato):
    with open(filepath, "w") as file:
        file.write(contenuto_decriptato)


def start_receiver():
    # Parametri SMTP
    smtp_port = 25

    # Crea il socket object  TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # assegnazione dei parametri al socket
        server_socket.bind(("localhost", smtp_port))

        # Metti il socket in modalità di ascolto
        server_socket.listen(1)
        print("Receiver in ascolto sulla porta", smtp_port)

        while True:
            # Accetta una connessione in entrata
            client_socket, client_address = server_socket.accept()
            print("Server SSL/TLS protocol version:", ssl.OPENSSL_VERSION)

            print("Connessione in entrata da", client_address)

            # Wrap del socket con TLS, ovviamenten ha bisogno di chiave e certificato 
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(
                certfile="self_certificate/certificate.pem",
                keyfile="self_certificate/private_key.pem",
            )
            client_socket = context.wrap_socket(client_socket, server_side=True)




            #Ricevi il messaggio di arrivo del client
            banner = client_socket.recv(1024).decode()
            print("\n0: " + banner + "\n")


            # Manda il messaggio di benvenuto al client
            welcome_message = "220 Welcome to the SMTP receiver"
            client_socket.sendall(welcome_message.encode())

            # Ricevi i comandi dal client fin quando il client non smette di inviare dati
            while True:
                command = client_socket.recv(1024).decode()
                if not command:
                    break
                    
                    
		#  da riga 79 a riga 101 riceve l'url 
                if command.startswith("DATA"): #aspetta fin quando uno dei pacchetti non contiene DATA, se contiene DATA entra in questo if 
                    # Invia una conferma al client per iniziare a inviare il corpo dell'url criptato
                    client_socket.sendall(
                        "354 Start URL input; end with FINE MESSAGGIO\r\n".encode()
                    )
                    
                    #creo una variabile per contenere l'url mandato dal client
                    url_data = ""
                   
                    print("1: 354 Receiving Data\n")


 		    #nel while il server va a leggere 1024 byte alla volta in maniera segmentata quindi fino a quando va a trovare FINE MESSAGGIO
                    while True:
                        url_chunk = client_socket.recv(1024).decode() #ricevo segmenti dati
                        url_data += url_chunk
                        if url_data.endswith("\r\nFINE MESSAGGIO\r\n"):
                            url_data.replace("FINE MESSAGGIO", "")
                            break
                    print("2: 250 Received Data\n")

                    # Invia una conferma al client che i dati sono stati ricevuti correttamente
                    client_socket.sendall("250 OK\r\n".encode())

                # ---------------------------------------------------------------------
                #aspetta fin quando uno dei pacchetti non contiene KEY, se contiene KEY entra in questo if 
                   
		
		
		#comando KEY per la chiave
                if command.startswith("KEY"):
                     # Invia una conferma al client per iniziare a inviare il corpo della chiave criptato
                    client_socket.sendall(
                        "354 Start KEY SHARING; end with FINE KEY\r\n".encode()
                    )

                    
                    print("3: 354 Receiving Key\n")
                   
                   #creo una variabile per contenere la chiave
                    key_data = ""
                    #nel while il server va a leggere 1024 byte alla volta in maniera segmentata quindi fino a quando va a trovare FINE KEY
                    while True:
                        key_chunk = client_socket.recv(1024).decode() #ricevo segmenti key
                        key_data += key_chunk
                        if key_data.endswith("\r\nFINE KEY\r\n"):
                            break
                    print("4: 250 Received Key\n")

                    
                    key_data = key_data.replace("\r\nFINE KEY\r\n", "") #sostiuscie FINE KEY con nulla per prendermi solo la chiave ossia la parte rilevante
                    key = key_data.encode()
                    global cipher_suite #creo la variabile globale poichè mi servirà in futuro per decriptare il contenuto del pastes
                    cipher_suite = Fernet(key) #creo oggetto ciphersuite e gli assegno il fernet object che mi permette di decriptare l'url  
                    decryptedUrl = (cipher_suite.decrypt(url_data)).decode() #qui decripto l'url

                    print("\n---------------------------------------------\n")
                    print("\tencrypted url the client passed\n" + url_data)
                    print("\n---------------------------------------------\n")

                    print("\tencryption key the client passed\n" + key_data)
                    print("\n---------------------------------------------\n")

                    print("\tdecrypted url the client passed\n" + decryptedUrl)
                    print("\n---------------------------------------------\n")

                    readPastesContent(decryptedUrl) #questo manda alla funzione readPastesContent l'url decriptato CHE ANDRÀ A SCARICARE I CONTENUTI DEL PASTES E LI ANDRÀ A SCRIVERE SU DISCO

                    # Invia una conferma al client che l'url è stata ricevuta correttamente
                    client_socket.sendall("250 OK\r\n".encode())

            # Chiudi la connessione con il client
            client_socket.close()
            print("Connessione chiusa con", client_address)

    except socket.error as e:
        print("Errore di connessione:", str(e))
    finally:
        # Chiudi il socket del server
        server_socket.close()


# Utilizzo dell'example receiver
filepath = "ReceivedData.txt"
with open(filepath, "w+"):
    start_receiver()

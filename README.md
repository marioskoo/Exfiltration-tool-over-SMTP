#sender
- Genera una chiave crittografica usando Fernet.generate_key() e memorizzala nella variabile key.
- Crea un oggetto della classe Fernet utilizzando la chiave generata e assegnalo alla variabile cipher_suite.
- Converti la chiave in una stringa usando key.decode() e memorizzala nella variabile key_string.
- Apri il file specificato da file_path in modalità di lettura.
- Leggi il contenuto del file.
- Crittografa il contenuto usando cipher_suite.encrypt(content.encode()) e memorizza il contenuto crittografato nella variabile encryptedContent.
- Chiama la funzione create.createPaste() per creare una nuova paste con il contenuto crittografato.
- Crittografa l'URL usando cipher_suite.encrypt(not_encryptedUrl.encode()) e memorizza l'URL crittografato nella variabile encryptedUrl.
- Restituisci l'URL crittografato come una stringa decodificata.
- Crea un socket TCP utilizzando socket.socket(socket.AF_INET, socket.SOCK_STREAM).
- Chiama la funzione upload_to_pastes(file) per caricare il contenuto su pastes.io e ottenere l'URL, che poi verrà crittografato.
- Stabilisci una connessione con il server SMTP specificato da smtp_server e smtp_port utilizzando client_socket.connect((smtp_server, smtp_port)).
- Crea un contesto SSL utilizzando ssl.create_default_context().
- Imposta le opzioni del contesto SSL (context.check_hostname e context.verify_mode) per disabilitare la verifica del nome host e la verifica - del certificato.
- Aggiorna la connessione a TLS utilizzando context.wrap_socket(client_socket, server_hostname=smtp_server).
- Invia il messaggio di benvenuto al server.
- Ricevi il messaggio di benvenuto del server.
- Invia il comando "DATA" utilizzando client_socket.sendall(data_command.encode()).
- Invia l'URL crittografato utilizzando client_socket.sendall(url.encode()).
- Termina i dati dell'URL con un messaggio utilizzando client_socket.sendall("\r\nFINE MESSAGGIO\r\n".encode()).
- Invia il comando "KEY" utilizzando client_socket.sendall(data_command.encode()).
- Invia la chiave di crittografia (key_string) come messaggio utilizzando client_socket.sendall(key_string.encode()).
- Termina la chiave con una riga separata contenente un singolo punto utilizzando client_socket.sendall("\r\nFINE KEY\r\n".encode()).
- Chiudi il socket TCP utilizzando client_socket.close().


#receiver
- Il programma crea un socket TCP e lo mette in modalità di ascolto sulla porta specificata.
- Accetta una connessione in entrata da un client e stabilisce una connessione SSL/TLS con il client.
- Riceve un messaggio di benvenuto dal client.
- Invia un messaggio di benvenuto al client
- Riceve comandi dal client all'interno di un loop.
- Se il comando inizia con "DATA", invia una conferma al client per iniziare a inviare il corpo dell'email.
- Riceve il corpo dell'email dal client e lo salva nella variabile email_data.
- Invia una conferma al client che l'email è stata ricevuta correttamente.
- Se il comando inizia con "KEY", invia una conferma al client per iniziare a inviare la chiave di crittografia.
- Riceve la chiave dal client e la salva nella variabile key_data.
- Utilizza la chiave per decrittare il messaggio precedente (il corpo dell'email) e ottiene l'URL decrittato.
- Stampa l'URL criptato, la chiave di crittografia e l'URL decrittato.
- Chiama la funzione readPastesContent() passando l'URL decrittato.
- La funzione readPastesContent() legge il contenuto dei pastes utilizzando la libreria pastesAPI e decifra il contenuto crittografato.
- Salva il contenuto decifrato in un file specificato da filepath.
- Continua a ricevere comandi dal client finché la connessione non viene chiusa.
- Chiude la connessione con il client.
- Il programma torna al passo 2 per ascoltare ulteriori connessioni.



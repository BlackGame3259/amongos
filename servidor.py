import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

clientes = []
apodos = []

def transmitir(mensaje):
    """Envía un mensaje a todos los clientes conectados."""
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except:
            pass # Si falla al enviar a un cliente, lo ignoramos por ahora

def manejar(cliente):
    """Maneja la conexión de cada cliente de forma segura."""
    while True:
        try:
            mensaje = cliente.recv(1024)
            transmitir(mensaje)
        except:
            # Si el cliente se desconecta o hay un error, lo limpiamos de forma segura
            if cliente in clientes:
                indice = clientes.index(cliente)
                clientes.remove(cliente)
                cliente.close()
                apodo = apodos[indice]
                transmitir(f'[{apodo}] ha abandonado el chat.\n'.encode('utf-8'))
                apodos.remove(apodo)
            break

def recibir():
    """Acepta nuevas conexiones constantemente."""
    print("El servidor está activo y escuchando...")
    while True:
        cliente, direccion = servidor.accept()
        
        # Pedimos el apodo
        cliente.send('NICK'.encode('utf-8'))
        apodo = cliente.recv(1024).decode('utf-8')
        
        apodos.append(apodo)
        clientes.append(cliente)
        
        print(f"Nuevo usuario conectado: {apodo} {str(direccion)}")
        transmitir(f"¡[{apodo}] se ha unido al chat!\n".encode('utf-8'))
        
        # Iniciamos el hilo para el nuevo cliente
        hilo = threading.Thread(target=manejar, args=(cliente,))
        hilo.start()

if __name__ == "__main__":
    recibir()
import customtkinter as ctk
import socket
import threading
import sys

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AplicacionChat(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Chat Privado")
        self.geometry("600x500")
        
        # Interceptamos el botón "X" para cerrar todo de forma segura
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        # Diseño de la interfaz
        self.caja_chat = ctk.CTkTextbox(self, width=560, height=380, font=("Arial", 14))
        self.caja_chat.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.caja_chat.configure(state="disabled")

        self.entrada_mensaje = ctk.CTkEntry(self, placeholder_text="Escribe tu mensaje...", width=430, font=("Arial", 14))
        self.entrada_mensaje.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.entrada_mensaje.bind("<Return>", lambda event: self.enviar_mensaje())

        self.boton_enviar = ctk.CTkButton(self, text="Enviar", width=100, font=("Arial", 14, "bold"), command=self.enviar_mensaje)
        self.boton_enviar.grid(row=1, column=1, padx=(0, 20), pady=10)

        # Lógica de Red
        dialogo = ctk.CTkInputDialog(text="Ingresa tu nombre de usuario:", title="Login")
        self.apodo = dialogo.get_input()
        if not self.apodo:
            self.apodo = "Anónimo"

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.cliente.connect(('127.0.0.1', 55555))
            # Hilo para recibir mensajes (daemon=True asegura que muera al cerrar la app)
            hilo_recibir = threading.Thread(target=self.recibir_mensajes)
            hilo_recibir.daemon = True 
            hilo_recibir.start()
        except:
            self.mostrar_mensaje("❌ No se pudo conectar al servidor. Asegúrate de encender 'servidor.py' primero.\n")

    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.cliente.recv(1024).decode('utf-8')
                if mensaje == 'NICK':
                    self.cliente.send(self.apodo.encode('utf-8'))
                else:
                    self.mostrar_mensaje(mensaje + "\n")
            except:
                self.mostrar_mensaje("⚠️ Conexión terminada.\n")
                self.cliente.close()
                break

    def enviar_mensaje(self):
        texto = self.entrada_mensaje.get()
        if texto.strip() != "":
            mensaje_completo = f'{self.apodo}: {texto}'
            try:
                self.cliente.send(mensaje_completo.encode('utf-8'))
                self.entrada_mensaje.delete(0, "end")
            except:
                self.mostrar_mensaje("❌ Error: No se pudo enviar el mensaje.\n")

    def mostrar_mensaje(self, mensaje):
        self.caja_chat.configure(state="normal")
        self.caja_chat.insert("end", mensaje)
        self.caja_chat.yview("end")
        self.caja_chat.configure(state="disabled")

    def cerrar_aplicacion(self):
        """Cierra el socket y destruye la ventana limpiamente."""
        try:
            self.cliente.close()
        except:
            pass
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = AplicacionChat()
    app.mainloop()
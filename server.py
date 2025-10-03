#!/usr/bin/env python3
"""
Servidor web simple para la aplicación Buddy Finanzas
Ejecuta este archivo y abre http://localhost:8000 en tu navegador
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Puerto del servidor
PORT = 8000

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Agregar headers para permitir CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Servidor iniciado en http://localhost:{PORT}")
            print(f"📱 Abre tu navegador y ve a: http://localhost:{PORT}/1.html")
            print("⏹️  Presiona Ctrl+C para detener el servidor")
            
            # Abrir automáticamente en el navegador
            webbrowser.open(f'http://localhost:{PORT}/1.html')
            
            # Iniciar el servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98:  # Puerto en uso
            print(f"❌ Puerto {PORT} ya está en uso")
            print("💡 Cierra otras aplicaciones que usen el puerto 8000")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()


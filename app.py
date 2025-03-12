from flask import Flask, jsonify, request
from flask_cors import CORS
from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

def send_email(subject, content):
    user = os.getenv('USER')
    app_password = os.getenv('APP_PASSWORD')

    em = EmailMessage()
    em['From'] = user
    em['To'] = "bazand25@gmail.com"
    em['Subject'] = subject
    em.set_content(content)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(user, app_password)
            smtp.sendmail(user, "bazand25@gmail.com", em.as_string())
    except Exception as e:
        return {'success': False, 'message': str(e)}
    
    return {'success': True, 'message': 'Correo enviado'}

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, true")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PATCH, DELETE")
    return response

@app.route('/', methods=['GET'])
def api_home():
    try:
        return {"success": True, "message": "Bienvenido"}
    except Exception as e:
        return {"success": False, "message": str(e)}, 500

@app.route('/correo', methods=['POST'])
def correo():
    correo = request.json.get("correo")
    nombre = request.json.get("nombre")
    texto = request.json.get("texto")

    subject = 'Un nuevo usuario quiere contactarse contigo'
    content = f"""
                INFORMACIÓN

                nombre del usuario: {nombre}
                correo: {correo}
                texto: {texto}
              """
    
    result = send_email(subject, content)
    return jsonify(result)

@app.route('/reclamo', methods=['POST'])
def reclamo():
    nombre = request.json.get("nombre")
    dni = request.json.get("dni")
    telefono = request.json.get("telefono")
    email = request.json.get("email")
    direccion = request.json.get("direccion")
    tipoReclamo = request.json.get("tipoReclamo")
    descripcion = request.json.get("descripcion")

    subject = 'Un cliente tiene una queja o reclamo'
    content = f"""
                INFORMACIÓN

                nombre del usuario: {nombre}
                DNI: {dni}
                Telefono: {telefono}
                Email: {email}
                Dirección: {direccion}
                Tipo de Reclamo: {tipoReclamo}
                Descripción: {descripcion}
              """

    result = send_email(subject, content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
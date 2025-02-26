import os  # Importa el módulo os para manejar variables de entorno y otras operaciones relacionadas con el sistema operativo.
from flask import Flask, request, jsonify  # Importa las clases necesarias de Flask para crear una aplicación web y manejar solicitudes.
from flask_cors import CORS  # Importa CORS para habilitar el intercambio de recursos entre dominios (Cross-Origin Resource Sharing).
from utils import APIException, generate_sitemap  # Importa excepciones personalizadas y una función para generar un sitemap (asegúrate de que estos archivos existan).
from datastructures import FamilyStructure  # Importa la clase FamilyStructure que contiene la lógica de la familia.

app = Flask(__name__)  # Crea una instancia de la aplicación Flask.
app.url_map.strict_slashes = False  # Desactiva la comprobación estricta de barras diagonales en las rutas.
CORS(app)  # Habilita CORS para permitir que los recursos de esta API sean accesibles desde otros orígenes.

# Crear el objeto de la familia Jackson con el apellido "Jackson"
jackson_family = FamilyStructure("Jackson")

# Manejar los errores de tipo APIException y devolverlos como JSON
@app.errorhandler(APIException)  # Captura los errores APIException.
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code  # Devuelve el error como un JSON con el código de estado correspondiente.

# Ruta para generar un mapa del sitio con todos los endpoints de la API
@app.route('/')
def sitemap():
    return generate_sitemap(app)  # Llama a la función para generar un sitemap de la aplicación.

# Endpoint para obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()  # Obtiene todos los miembros de la familia.
    if members:
        return jsonify(members), 200  # Si existen miembros, los devuelve con código 200 (OK).
    return jsonify({"error": "Members list not found"}), 400  # Si no se encuentran miembros, devuelve un error con código 400 (Bad Request).

# Endpoint para obtener un miembro específico de la familia mediante su ID
@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = jackson_family.get_member(member_id)  # Busca al miembro de la familia por ID.
    if member:
        return jsonify(member), 200  # Si el miembro existe, lo devuelve con código 200.
    return jsonify({"error": "Member not found"}), 400  # Si no se encuentra el miembro, devuelve un error con código 400.

# Endpoint para agregar un nuevo miembro a la familia
@app.route("/member", methods=["POST"])
def add_member():
    member_data = request.json  # Obtiene los datos del nuevo miembro en formato JSON desde el cuerpo de la solicitud.
    errors = {}  # Inicializa un diccionario para guardar posibles errores de validación.

    # Validación de los datos enviados por el cliente
    if not member_data.get("first_name"):  # Verifica si falta el primer nombre.
        errors["first_name"] = "First name is required"
    if not member_data.get("age"):  # Verifica si falta la edad.
        errors["age"] = "Age is required"
    if not member_data.get("lucky_numbers"):  # Verifica si falta la lista de números de la suerte.
        errors["lucky_numbers"] = "Lucky numbers are required"
    
    # Si existen errores en la validación, los devuelve con código 400.
    if errors:
        return jsonify({"error": errors}), 400
    
    jackson_family.add_member(member_data)  # Agrega el nuevo miembro a la familia.
    return jsonify({"message": "Member added successfully"}), 200  # Responde con éxito al agregar el miembro.

# Endpoint para eliminar un miembro específico de la familia por ID
@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)  # Busca el miembro de la familia por ID.
    if member:
        jackson_family.delete_member(member_id)  # Si el miembro existe, lo elimina de la familia.
        return jsonify({"done": True}), 200  # Responde con éxito al eliminar el miembro.
    return jsonify({"error": "Member not found"}), 404  # Si no se encuentra el miembro, devuelve un error con código 404 (Not Found).

# Ejecutar la aplicación solo si este archivo es el principal
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))  # Obtiene el puerto de la variable de entorno, o usa 3000 por defecto.
    app.run(host='0.0.0.0', port=PORT, debug=True)  # Inicia el servidor Flask, disponible en todas las interfaces y en el puerto especificado, con depuración habilitada.



class FamilyStructure:  # Define la clase FamilyStructure, que representa la estructura de una familia.
    
    def __init__(self, last_name):  # Método inicializador de la clase (constructor). Toma el apellido de la familia como argumento.
        self.last_name = last_name  # Asigna el apellido recibido a la propiedad `last_name` del objeto.
        self._next_id = 1  # Inicializa el siguiente ID disponible para los miembros de la familia.
        
        # Lista inicial de miembros de la familia con sus atributos
        self._members = [
            {"id": self._generateId(), "first_name": "John", "last_name": last_name, "age": 33, "lucky_numbers": [7, 13, 22]},
            {"id": self._generateId(), "first_name": "Jane", "last_name": last_name, "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": self._generateId(), "first_name": "Jimmy", "last_name": last_name, "age": 5, "lucky_numbers": [1]}
         ]

    def _generateId(self):  # Método privado que genera un ID único para los miembros de la familia.
        generated_id = self._next_id  # Toma el ID actual y lo guarda en una variable temporal.
        self._next_id += 1  # Incrementa el valor de `_next_id` para la siguiente vez que se llame a este método.
        return generated_id  # Devuelve el ID generado.

    def add_member(self, member):  # Método para agregar un nuevo miembro a la familia.
        # Verifica si el miembro tiene un id, si no lo genera
        if "id" not in member:  # Si el miembro no tiene un ID (es decir, no tiene la clave "id" en el diccionario),
            member["id"] = self._generateId()  # Llama a _generateId para asignarle un ID único.
        
        # Asignar el apellido automáticamente
        member["last_name"] = self.last_name  # Asigna el apellido de la familia al miembro.
        
        # Agregar el miembro a la lista
        self._members.append(member)  # Añade el nuevo miembro a la lista `_members`.

    def delete_member(self, id):  # Método para eliminar un miembro de la familia, dado su ID.
        # Elimina el miembro con el id proporcionado
        self._members = [member for member in self._members if member["id"] != id]  # Filtra la lista y elimina el miembro cuyo id coincida con el proporcionado.

    def get_member(self, id):  # Método para obtener un miembro de la familia por su ID.
        # Devuelve el miembro que tiene el id proporcionado
        for member in self._members:  # Recorre todos los miembros de la familia.
            if member["id"] == id:  # Si el id del miembro coincide con el proporcionado,
                return member  # Devuelve el miembro encontrado.
        return None  # Si no se encuentra un miembro con el ID dado, devuelve None.

    def get_all_members(self):  # Método para obtener todos los miembros de la familia.
        # Devuelve todos los miembros de la familia
        return self._members  # Retorna la lista completa de miembros de la familia.

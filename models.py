class Registro:
    def __init__(self, id, nombre, categoria, descripcion, precio=0, activo=True, destacado=False):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.activo = activo
        self.destacado = destacado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "activo": bool(self.activo),
            "destacado": bool(self.destacado)
        }
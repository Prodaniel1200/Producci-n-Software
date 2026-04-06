class ContactService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, nombre: str, correo: str, asunto: str, mensaje: str):
        if not nombre or not correo or not asunto:
            return {"ok": False, "error": "Nombre, correo y asunto son obligatorios"}
        self.repository.save(nombre, correo, asunto, mensaje)
        return {"ok": True}

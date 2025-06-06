# Se define una excepción personalizada para manejar la restricción de números negativos.
class NegativeNumberError(Exception):
    
    def __init__(self, message="Operación o resultado con número negativo no permitido."):
        self.message = message
        super().__init__(self.message)
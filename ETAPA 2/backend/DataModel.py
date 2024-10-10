from pydantic import BaseModel

class DataModel(BaseModel):

    Textos_espanol: str

    def columns(self):
        return ['Textos_espanol']
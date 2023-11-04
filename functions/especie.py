import json
from database import Especie
from shemas import EspecieRequestModel #Modelo para una peticion de usuario
from shemas import EspecieResponseModel

from fastapi import HTTPException #, Request

async def create_especie(especie_request: EspecieRequestModel):
    especie_request = Especie.create(
        especie = especie_request.especie
    )
    return especie_request

async def get_especie(especie_nombre):
    especie = Especie.select().where(Especie.especie == especie_nombre).first()

    if especie:    
        return EspecieResponseModel( id=especie.id ,especie=especie.especie)
    else:
        return HTTPException(404, 'Especie not found')

async def delete_especie(especie_nombre):
    especie = Especie.select().where(Especie.especie == especie_nombre).first()

    if especie:
        especie.delete_instance()  
        return True
    else:
        return HTTPException(404, 'Especie not found')

async def update_especie(especie_nombre, especie_request: EspecieRequestModel):
    especie = Especie.select().where(Especie.especie == especie_nombre).first()

    if especie:
        for index, item in especie_request:
            setattr(especie, index, item)
        especie.save()
        return True
    else:
        return HTTPException(404, 'Especie not found')
    
async def get_especies():
    especie = Especie.select()
    if especie:
        resultados = []
        for index in especie:
            spece = EspecieResponseModel(id=index.id ,especie=index.especie)
            modelo = {'id': spece.id, 'especie': spece.especie}
            resultados.append(modelo)
        json_result = json.dumps({'Especie': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Especie not found')
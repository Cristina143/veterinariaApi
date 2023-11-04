import json
from database import Raza
from shemas import RazaRequestModel #Modelo para una peticion de usuario
from shemas import RazaResponseModel

from fastapi import HTTPException #, Request

async def create_race(raza_request: RazaRequestModel):
    raza_request = Raza.create(
        raza = raza_request.raza,
        especie_nombre= raza_request.especie_nombre
    )
    return raza_request

async def get_race(raza_nombre):
    raza = Raza.select().where(Raza.raza == raza_nombre).first()

    if raza:    
        return RazaResponseModel( id=raza.id ,raza=raza.raza, especie_nombre=raza.especie_nombre.especie) 
    else:
        return HTTPException(404, 'Race not found')

async def get_races():
    raza = Raza.select()
    if raza:
        resultados = []
        for index in raza:
            race = RazaResponseModel(id=index.id ,raza=index.raza, especie_nombre=index.especie_nombre.especie)
            modelo = {'id': race.id, 'raza': race.raza, 'especie_nombre': race.especie_nombre}
            resultados.append(modelo)
        json_result = json.dumps({'Razas': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Races not found')

async def delete_race(raza_nombre):
    raza = Raza.select().where(Raza.raza == raza_nombre).first()

    if raza:
        raza.delete_instance()  
        return True
    else:
        return HTTPException(404, 'Race not found')

async def update_race(raza_nombre, raza_request: RazaRequestModel):
    raza = Raza.select().where(Raza.raza == raza_nombre).first()

    if raza:
        for index, item in raza_request:
            setattr(raza, index, item)
        raza.save()
        return True
    else:
        return HTTPException(404, 'Worker not found')


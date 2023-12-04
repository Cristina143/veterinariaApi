from database import Mascota
from shemas import MascotaRequestModel #Modelo para una peticion de usuario
from shemas import MascotaResponseModel
import json

from fastapi import HTTPException #, Request

async def create_pet(mascota_request: MascotaRequestModel):
    mascota_request = Mascota.create(
        nombre = mascota_request.nombre,
        genero= mascota_request.genero,
        comentario= mascota_request.comentario,
        estado= mascota_request.estado,
        clienteid= mascota_request.clienteid,
        raza_nombre= mascota_request.raza_nombre
    )
    return mascota_request

async def get_pet(mascota_mascota):
    mascota = Mascota.select().where(Mascota.nombre == mascota_mascota).first()

    if mascota:    
        return MascotaResponseModel( id=mascota.id, nombre=mascota.nombre, genero=mascota.genero, comentario=mascota.comentario, estado=mascota.estado, clienteid=mascota.clienteid.id, raza_nombre=mascota.raza_nombre.raza)
    else:
        return HTTPException(404, 'Pet not found')
    
async def get_petId(mascota_id):
    mascota = Mascota.select().where(Mascota.id == mascota_id).first()

    if mascota:    
        return MascotaResponseModel( id=mascota.id, nombre=mascota.nombre, genero=mascota.genero, comentario=mascota.comentario, estado=mascota.estado, clienteid=mascota.clienteid.id, raza_nombre=mascota.raza_nombre.raza)
    else:
        return HTTPException(404, 'Pet not found')

async def get_pets():
    pet = Mascota.select()
    if pet:
        resultados = []
        for index in pet:
            pet = MascotaResponseModel( id=index.id, nombre=index.nombre, genero=index.genero, comentario=index.comentario, estado=index.estado, clienteid=index.clienteid.id, raza_nombre=index.raza_nombre.raza)
            modelo = {'id': pet.id, 'nombre': pet.nombre, 'genero': pet.genero, 'comentario': pet.comentario, 'estado': pet.estado, 'clienteid': pet.clienteid, 'raza_nombre': pet.raza_nombre}
            resultados.append(modelo)
        json_result = json.dumps({'Mascotas': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Pets not found')

async def delete_pet(mascota_mascota):
    mascota = Mascota.select().where(Mascota.nombre == mascota_mascota).first()

    if mascota:
        mascota.delete_instance()  
        return True
    else:
        return HTTPException(404, 'Pet not found')

async def update_pet(mascota_mascota, mascota_request: MascotaRequestModel):
    mascota = Mascota.select().where(Mascota.nombre == mascota_mascota).first()

    if mascota:
        for index, item in mascota_request:
            setattr(mascota, index, item)
        mascota.save()
        return True
    else:
        return HTTPException(404, 'Pet not found')
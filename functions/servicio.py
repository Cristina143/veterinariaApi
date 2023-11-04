from database import Servicio
from shemas import ServicioRequestModel #Modelo para una peticion de usuario
from shemas import ServicioResponseModel
import json

from fastapi import HTTPException #, Request

async def create_servicio(servicio_request: ServicioRequestModel):
    servicio_request = Servicio.create(
        nombre = servicio_request.nombre,
        precio= servicio_request.precio
    )
    return servicio_request

async def get_servicio(servicio_nombre):
    servicio = Servicio.select().where(Servicio.nombre == servicio_nombre).first()

    if servicio:    
        return ServicioResponseModel( id=servicio.id ,nombre=servicio.nombre, precio=servicio.precio)
    else:
        return HTTPException(404, 'Servicio not found')

async def delete_servicio(servicio_nombre):
    servicio = Servicio.select().where(Servicio.nombre == servicio_nombre).first()

    if servicio:
        servicio.delete_instance()  
        return True
    else:
        return HTTPException(404, 'Servicio not found')

async def update_servicio(servicio_nombre, servicio_request: ServicioRequestModel):
    servicio = Servicio.select().where(Servicio.nombre == servicio_nombre).first()

    if servicio:
        for index, item in servicio_request:
            setattr(servicio, index, item)
        servicio.save()
        return True
    else:
        return HTTPException(404, 'Servicio not found')
    

async def get_servicios():
    servicio = Servicio.select()
    if servicio:
        resultados = []
        for index in servicio:
            service = ServicioResponseModel(id=index.id ,nombre=index.nombre,  precio=index.precio)
            modelo = {'id': service.id, 'nombre': service.nombre, 'precio': service.precio}
            resultados.append(modelo)
        json_result = json.dumps({'Servicio': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Service not found')
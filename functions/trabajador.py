from database import Trabajador
from shemas import TrabajadorRequestModel #Modelo para una peticion de usuario
from shemas import TrabajadorResponseModel, userBase, userCreate, userFinal, userUdatePass
import json
from datetime import date, timedelta, datetime
import jwt

from fastapi import HTTPException #, Request

import logging
logging.basicConfig(level=logging.DEBUG)
#class workers ():


SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 6


#TrabajadorRequestModel
async def create_worker(trabajodor_request: userCreate):
    trabajodor_request = Trabajador.create(
        nombre = trabajodor_request.nombre,
        telefono= trabajodor_request.telefono,
        fechaContrato= date.today(),#trabajodor_request.fechaContrato,
        password= trabajodor_request.password,
        correo= trabajodor_request.correo,
        tipoUsuario= trabajodor_request.tipoUsuario
    )
    return trabajodor_request

async def get_worker(trabajador_nombre):
    trabajador = Trabajador.select().where(Trabajador.nombre == trabajador_nombre).first()

    if trabajador:    
        return userFinal(
            id=trabajador.id,
            nombre=trabajador.nombre,
            telefono=trabajador.telefono,
            fechaContrato=trabajador.fechaContrato.strftime('%Y-%m-%d'),  # Asigna la cadena de fecha
            password=trabajador.password,
            correo=trabajador.correo,
            tipoUsuario=trabajador.tipoUsuario
        )
    else:
        raise HTTPException(status_code=404, detail='Worker not found')
    
async def get_workerID(trabajador_id):
    trabajador = Trabajador.select().where(Trabajador.id == trabajador_id).first()

    if trabajador:    
        return userFinal(
            id=trabajador.id,
            nombre=trabajador.nombre,
            telefono=trabajador.telefono,
            fechaContrato=trabajador.fechaContrato.strftime('%Y-%m-%d'),  # Asigna la cadena de fecha
            password=trabajador.password,
            correo=trabajador.correo,
            tipoUsuario=trabajador.tipoUsuario
        )
    else:
        raise HTTPException(status_code=404, detail='Worker not found')

async def get_login(trabajador_correo,trabajador_contra):
    trabajador = Trabajador.select().where(Trabajador.correo == trabajador_correo and Trabajador.password == trabajador_contra).first()

    if trabajador:
        usuario = userFinal(
            id=trabajador.id,
            nombre=trabajador.nombre,
            telefono=trabajador.telefono,
            fechaContrato=trabajador.fechaContrato.strftime('%Y-%m-%d'),
            password=trabajador.password,
            correo=trabajador.correo,
            tipoUsuario=trabajador.tipoUsuario
        )
        modelo = {
            'nombre': usuario.nombre, 
            'tipoUsuario': usuario.tipoUsuario
        }
        return modelo
    else:
        raise HTTPException(status_code=404, detail='Worker not found or incorrect password')


async def login2(request_login):
    email = request_login.username
    password = request_login.password
    print(email , " " , password )
    token = await authenticate_user(email, password)
    return {'access_token': token, 'token_type': 'bearer' }
#    return True

async def authenticate_user(email:str, password:str):
    trabajador= Trabajador.get_or_none(Trabajador.correo==email)
    
    if trabajador is None or not trabajador.password == password:
        raise HTTPException(status_code=404, detail='Worker not found or incorrect password')
    
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": trabajador.correo,
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    

    return access_token


async def get_workers():
    trabajador = Trabajador.select()
    if trabajador:
        resultados = []
        for index in trabajador:
            worker = userFinal(
            id=index.id,
            nombre=index.nombre,
            telefono=index.telefono,
            fechaContrato=index.fechaContrato.strftime('%Y-%m-%d'),  # Asigna la cadena de fecha
            #password=index.password,
            correo=index.correo,
            tipoUsuario=index.tipoUsuario
        )
            #TrabajadorResponseModel(id=index.id ,nombre=index.nombre, telefono=index.telefono, fechaContrato=index.fechaContrato, password=index.password, correo=index.correo, tipoUsuario=index.tipoUsuario)
            modelo = {'id': worker.id, 
                    'nombre': worker.nombre, 
                    'telefono': worker.telefono, 
                    'fechaContrato': worker.fechaContrato, 
                    #'password': worker.password, 
                    'correo': worker.correo, 
                    'tipoUsuario': worker.tipoUsuario}
            resultados.append(modelo)
        json_result = json.dumps({'Trabajadores': resultados})
        data = json.loads(json_result)
        return data
    else:
        raise HTTPException(status_code=404, detail='Worker not found')

async def delete_worker(trabajador_nombre):
    trabajador = Trabajador.select().where(Trabajador.nombre == trabajador_nombre).first()

    if trabajador:
        trabajador.delete_instance()  
        return True
    else:
        raise HTTPException(status_code=404, detail='Worker not found')

async def update_worker(trabajador_nombre, trabajodor_request: userUdatePass):
    trabajador = Trabajador.select().where(Trabajador.nombre == trabajador_nombre).first()

    if trabajador:
        for index, item in trabajodor_request:
            setattr(trabajador, index, item)
        trabajador.save()
        return True
    else:
        raise HTTPException(status_code=404, detail='Worker not found')

async def update_pass(trabajador_correo, trabajodor_request: userUdatePass):
    trabajador = Trabajador.select().where(Trabajador.correo == trabajador_correo).first()

    if trabajador:
        setattr(trabajador, 'password', trabajodor_request.password)
        trabajador.save()
        return True
    else:
        raise HTTPException(status_code=404, detail='Trabajador not found')





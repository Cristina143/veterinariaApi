import json
from database import Cliente
from shemas import ClienteRequestModel #Modelo para una peticion de usuario
from shemas import ClienteResponseModel


from fastapi import HTTPException #, Request

async def create_cliente(cliente_request: ClienteRequestModel):
    cliente_request = Cliente.create(
        nombre = cliente_request.nombre,
        correo= cliente_request.correo,
        telefono= cliente_request.telefono,
        direccion= cliente_request.direccion,
        estado= cliente_request.estado
    )
    return cliente_request

async def get_cliente(cliente_nombre):
    cliente = Cliente.select().where(Cliente.nombre == cliente_nombre).first()

    if cliente:    
        return ClienteResponseModel( id=cliente.id ,nombre=cliente.nombre, correo=cliente.correo, telefono=cliente.telefono, direccion=cliente.direccion, estado=cliente.estado)
    else:
        return HTTPException(404, 'Cliente not found')

async def delete_cliente(cliente_nombre):
    cliente = Cliente.select().where(Cliente.nombre == cliente_nombre).first()

    if cliente:
        cliente.delete_instance()  
        return True
    else:
        return HTTPException(404, 'Cliente not found')

async def update_cliente(cliente_nombre, cliente_request: ClienteRequestModel):
    cliente = Cliente.select().where(Cliente.nombre == cliente_nombre).first()

    if cliente:
        for index, item in cliente_request:
            setattr(cliente, index, item)
        cliente.save()
        return True
    else:
        return HTTPException(404, 'Cliente not found')

async def get_clientes():
    cliente = Cliente.select()
    if cliente:
        resultados = []
        for index in cliente:
            client = ClienteResponseModel(id=index.id ,nombre=index.nombre,  correo=index.correo, telefono=index.telefono, direccion=index.direccion, estado=index.estado)
            modelo = {'id': client.id, 'nombre': client.nombre, 'correo': client.correo, 'telefono': client.telefono, 'direccion': client.direccion, 'estado': client.estado}
            resultados.append(modelo)
        json_result = json.dumps({'Clientes': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Clients not found')
    
async def down_cliente(cliente_nombre):
    cliente = Cliente.select().where(Cliente.nombre == cliente_nombre).first()
    if cliente:
        setattr(cliente, 'estado', 'inactivo')
        cliente.save()
        return 'Se ha dado un cliente de baja con exito'
    return 'Error: No se ha podido dar de baja al cliente'
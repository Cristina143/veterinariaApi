from fastapi import FastAPI, HTTPException, Depends #, Request
from database import DB as connection
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import Trabajador, Mascota, Cliente, Servicio, Especie, Raza, Cita, DetalleVenta, Cajero,llavesmaestra
from shemas import TrabajadorRequestModel,userCreate, userUdatePass #Modelo para una peticion de usuario
#from shemas import TrabajadorResponseModel

#from database import Cliente
from shemas import ClienteRequestModel #Modelo para una peticion de usuario
#from shemas import ClienteResponseModel

#from database import Servicio
from shemas import ServicioRequestModel #Modelo para una peticion de usuario
#from shemas import ServicioResponseModel

#from database import Especie
from shemas import EspecieRequestModel #Modelo para una peticion de usuario
#from shemas import EspecieResponseModel

from shemas import RazaRequestModel

from shemas import MascotaRequestModel, DetalleVentaRequestModel, citaBaseEntrada, citaPay, cajaAbre, cajaCierra

import functions.trabajador as Worker
import functions.cliente as Client
import functions.servicio as Service
import functions.especie as Species
import functions.raza as Race
import functions.mascota as Pet
import functions.cita as Date
import functions.cajero as Cashier
import functions.correo as Email

import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    if not connection.table_exists(Trabajador):
        connection.create_tables([Trabajador])
    if not connection.table_exists(Cliente):
        connection.create_tables([Cliente])
    if not connection.table_exists(Servicio): 
        connection.create_tables([Servicio])
    if not connection.table_exists(Especie):
        connection.create_tables([Especie], safe=True)
    if not connection.table_exists(Raza):
        connection.create_tables([Raza], safe=True)
    if not connection.table_exists(Mascota):
        connection.create_tables([Mascota])
    if not connection.table_exists(Cita):
        connection.create_tables([Cita])
    if not connection.table_exists(DetalleVenta):
        connection.create_tables([DetalleVenta])
    if not connection.table_exists(Cajero):
        connection.create_tables([Cajero])
    if not connection.table_exists(llavesmaestra):
        connection.create_tables([llavesmaestra])

    #connection.create_tables([Trabajador])
#    connection.create_tables([Cliente])
#    connection.create_tables([Servicio])
#    connection.create_tables([Especie])
#    connection.create_tables([Raza])

#    connection.create_tables([Mascota])
#    connection.create_tables([Cita])
#    connection.create_tables([DetalleVenta])
#    connection.create_tables([Cajero])



@app.on_event('shutdown')
def shutdown():
    if connection.is_closed():
        connection.close()

@app.get('/')
async def index():
    return 'hola, funciono'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "loginn")


#trabajador
#agregar datos a la tabla trabajador en la BD    TrabajadorRequestModel
#@app.post('/trabajador', tags=['trabajador'])
#async def create_worker(trabajodor_request: userCreate, request_login: str = Depends(oauth2_scheme)):
#    return await Worker.create_worker(trabajodor_request)

@app.post('/trabajador', tags=['trabajador'])
async def create_worker(trabajodor_request: userCreate):
    return await Worker.create_worker(trabajodor_request)

#consultar un trabajador
@app.get('/trabajador/{trabajador_nombre}', tags=['trabajador'])
async def get_worker(trabajador_nombre):
    return await Worker.get_worker(trabajador_nombre)
    #return Trabajador.select().where(Trabajador.id == trabajador_id).first()

#consultar un trabajador
@app.get('/trabajadorId/{trabajador_id}', tags=['trabajador'])
async def get_worker(trabajador_id):
    return await Worker.get_workerID(trabajador_id)
    #return Trabajador.select().where(Trabajador.id == trabajador_id).first()

@app.get('/logIn', tags=['trabajador'])
async def get_login(trabajador_correo:str,trabajador_contra:str ):
    return await Worker.get_login(trabajador_correo,trabajador_contra)
    

@app.post('/loginn', tags=['trabajador'])
async def login(request_login: OAuth2PasswordRequestForm = Depends()):
    return await Worker.login2(request_login)

@app.get('/nombre', tags=['trabajador'])
async def nombre(request_login: str = Depends(oauth2_scheme)):
    return "hola funciona"

    
#borrar un trabajador
@app.delete('/trabajador/{trabajador_nombre}', tags=['trabajador'])
async def delete_worker(trabajador_nombre):
    return await Worker.delete_worker(trabajador_nombre)


@app.put('/trabajador/{trabajador_nombre}', tags=['trabajador'])
async def update_worker(trabajador_nombre, trabajodor_request: userCreate):
    return await Worker.update_worker(trabajador_nombre, trabajodor_request)

@app.post('/trabajador/{trabajador_correo}', tags=['trabajador'])
async def update_worker(trabajador_correo, trabajodor_request: userUdatePass): 
    return await Worker.update_pass(trabajador_correo, trabajodor_request) 

@app.get('/trabajadores', tags=['trabajador'])
async def get_workers():
    return await Worker.get_workers()



#Cliente
#agregar datos a la tabla cliente en la BD
@app.post('/cliente', tags=['cliente'])
async def create_cliente(cliente_request: ClienteRequestModel):
    return await Client.create_cliente(cliente_request)

#consultar un cliente
@app.get('/cliente/{cliente_nombre}', tags=['cliente'])
async def get_cliente(cliente_nombre):
    return await Client.get_cliente(cliente_nombre)

#borrar un trabajador
@app.delete('/cliente/{cliente_nombre}', tags=['cliente'])
async def delete_cliente(cliente_nombre):
    return await Client.delete_cliente(cliente_nombre)

@app.put('/cliente/{cliente_nombre}', tags=['cliente'])
async def update_cliente(cliente_nombre, cliente_request: ClienteRequestModel):
    return await Client.update_cliente(cliente_nombre, cliente_request)

#dar de baja a un cliente por la casilla de estado
@app.put('/clienteBaja/{cliente_nombre}', tags=['cliente'])
async def down_cliente(cliente_nombre):
    return await Client.down_cliente(cliente_nombre)

@app.get('/clientes', tags=['cliente'])
async def get_clientes():
    return await Client.get_clientes()

#Servicio
#agregar datos a la tabla servicio en la BD
@app.post('/servicio', tags=['servicio'])
async def create_servicio(servicio_request: ServicioRequestModel):
    return await Service.create_servicio(servicio_request)

#consultar un servicio
@app.get('/servicio/{servicio_nombre}', tags=['servicio'])
async def get_servicio(servicio_nombre):
    return await Service.get_servicio(servicio_nombre)

#borrar un servicio
@app.delete('/servicio/{servicio_nombre}', tags=['servicio'])
async def delete_servicio(servicio_nombre):
    return await Service.delete_servicio(servicio_nombre)

@app.put('/servicio/{servicio_nombre}', tags=['servicio'])
async def update_servicio(servicio_nombre, servicio_request: ServicioRequestModel):
    return await Service.update_servicio(servicio_nombre, servicio_request)

@app.get('/servicios', tags=['servicio'])
async def get_servicios():
    return await Service.get_servicios()

#especie
#agregar datos a la tabla especie en la BD
@app.post('/especie', tags=['especie'])
async def create_especie(especie_request: EspecieRequestModel):
    return await Species.create_especie(especie_request)

#consultar un especie
@app.get('/especie/{especie_nombre}', tags=['especie'])
async def get_especie(especie_nombre):
    return await Species.get_especie(especie_nombre)

#borrar un especie
@app.delete('/especie/{especie_nombre}', tags=['especie'])
async def delete_especie(especie_nombre):
    return await Species.delete_especie(especie_nombre)


@app.put('/especie/{especie_nombre}', tags=['especie'])
async def update_especie(especie_nombre, especie_request: EspecieRequestModel):
    return await Species.update_especie(especie_nombre, especie_request)

@app.get('/especies', tags=['especie'])
async def get_especies():
    return await Species.get_especies()

#raza
@app.post('/raza', tags=['raza'])
async def create_race(raza_request: RazaRequestModel):
    return await Race.create_race(raza_request)

#consultar un raza
@app.get('/raza/{raza_nombre}', tags=['raza'])
async def get_race(raza_nombre):
    return await Race.get_race(raza_nombre)

#borrar un raza
@app.delete('/raza/{raza_nombre}', tags=['raza'])
async def delete_race(raza_nombre):
    return await Race.delete_race(raza_nombre)

@app.put('/raza/{raza_nombre}', tags=['raza'])
async def update_race(raza_nombre, raza_request: RazaRequestModel):
    return await Race.update_race(raza_nombre, raza_request)

@app.get('/razas', tags=['raza'])
async def get_races():
    return await Race.get_races()

#mascota
@app.post('/mascota', tags=['mascota'])
async def create_pet(mascota_request: MascotaRequestModel):
    return await Pet.create_pet(mascota_request)

#consultar un raza
@app.get('/mascota/{mascota_nombre}', tags=['mascota'])
async def get_pet(mascota_nombre):
    return await Pet.get_pet(mascota_nombre)

#consultar un raza
@app.get('/mascotaId/{mascota_id}', tags=['mascota'])
async def get_pet(mascota_id):
    return await Pet.get_petId(mascota_id)

#borrar un raza
@app.delete('/mascota/{mascota_nombre}', tags=['mascota'])
async def delete_pet(mascota_nombre):
    return await Pet.delete_pet(mascota_nombre)

@app.put('/mascota/{mascota_nombre}', tags=['mascota'])
async def update_pet(mascota_nombre, mascota_request: MascotaRequestModel):
    return await Pet.update_pet(mascota_nombre, mascota_request)

@app.get('/mascotas', tags=['mascota'])
async def get_pets():
    return await Pet.get_pets()

#DetalleVenta
@app.post('/detalleventa', tags=['detalleventa'])
async def create_detalle(detalle_request: DetalleVentaRequestModel):
    return await Date.create_detalleVenta(detalle_request)

#consultar un raza
@app.get('/detalleventa/{detalle_id}', tags=['detalleventa'])
async def get_detalle(detalle_id):
    return await Date.get_detalleVenta(detalle_id)

@app.put('/detalleventa/{detalle_id}', tags=['detalleventa'])
async def update_detalle(detalle_id, detalle_request: DetalleVentaRequestModel):
    return await Date.update_detalleVenta(detalle_id, detalle_request)

@app.get('/detalleventa', tags=['detalleventa'])
async def get_detalles():
    return await Date.get_detalleVentas()

#cita
@app.post('/cita', tags=['cita'])
async def create_cita(cita_request: citaBaseEntrada):
    return await Date.create_cita(cita_request)

@app.get('/citaid/{cita_id}', tags=['cita'])
async def get_citaid(cita_id):
    return await Date.get_citaid(cita_id)

#No funciona
@app.get('/citadoctor/{nombre_doctor}', tags=['cita'])
async def get_citadoctor(nombre_doctor):
    return await Date.get_citadoctor(nombre_doctor)

@app.put('/cita/{cita_id}', tags=['cita'])
async def update_cita(cita_id, cita_request: citaBaseEntrada):
    return await Date.update_cita(cita_id, cita_request)

@app.get('/citaactiva', tags=['cita'])
async def get_citaactivas():
    return await Date.get_citaactivas()

@app.get('/cita/{cita_dia}', tags=['cita'])
async def get_citadia(cita_dia):
    return await Date.get_citadia(cita_dia)

@app.post('/cita/{cita_id}', tags=['cita'])
async def create_pago(cita_id, pago_request: citaPay):
    return await Date.create_pago(cita_id, pago_request)

@app.get('/historial/{nombre_mascota}', tags=['cita'])
async def get_historial(nombre_mascota):
    return await Date.get_historial(nombre_mascota)

#caja
@app.post('/caja', tags=['caja'])
async def abrir_caja(caja_request: cajaAbre):
    return await Cashier.abrir_caja(caja_request)

@app.post('/caja/{caja_id}', tags=['caja'])
async def cerrar_caja(caja_id, caja_request: cajaCierra):
    return await Cashier.cerrar_caja(caja_id, caja_request)

@app.get('/caja/{caja_fecha}', tags=['caja'])
async def get_caja(caja_fecha):
    return await Cashier.get_caja(caja_fecha)


@app.post("/email", tags=['email'])
async def SendEmail(correo):
    return await Email.SendEmail(correo)

@app.post("/compara", tags=['email'])
async def Compara(codigo):
    return await Email.Compara(codigo)

#py -m venv env
#env\Scripts\activate.bat   *
#pip install fastapi
#pip install uvicorn
#uvicorn main:app --reload          *
#Thunder Client

#pip install bcrypt
from pydantic import BaseModel, EmailStr
from typing import Optional

#Trabajadores
class userBase(BaseModel):
    nombre: str
    telefono:str
    correo: EmailStr
    tipoUsuario:str

class userCreate(userBase):
    contraseña:str

class userFinal(userBase):
    id:int
    fechaContrato:str
    
class userUdatePass(BaseModel):
    contraseña:str


#Modelo de la tabla trabajador para meter datos
class TrabajadorRequestModel(BaseModel):
    #nombre: str
    #telefono: str
    fechaContrato: str
    contraseña: str
    #correo: EmailStr
    #tipoUsuario: str

#Modelo de la tabla trabajador para consultar datos
class TrabajadorResponseModel(TrabajadorRequestModel):
    id: int 

class TrabajadorChangeModel(BaseModel):
    nombre: str
    telefono: str
    correo: EmailStr
    tipoUsuario: str

#Modelo de la tabla cliente para meter datos
class ClienteRequestModel(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    estado: str
    

#Modelo de la tabla cliente para consultar datos
class ClienteResponseModel(ClienteRequestModel):
    id: int 

#servicio
#Modelo de la tabla servicio para meter datos
class ServicioRequestModel(BaseModel):
    nombre: str
    precio: float
    
#Modelo de la tabla servicio para consultar datos
class ServicioResponseModel(ServicioRequestModel):
    id: int 

#especie
#Modelo de la tabla especie para meter datos
class EspecieRequestModel(BaseModel):
    especie: str
    
#Modelo de la tabla especie para consultar datos
class EspecieResponseModel(EspecieRequestModel):
    id: int 

#raza
#Modelo de la tabla raza para meter datos
class RazaRequestModel(BaseModel):
    raza: str
    especie_nombre: str
    
#Modelo de la tabla raza para consultar datos
class RazaResponseModel(RazaRequestModel):
    id: int 

#mascota
#Modelo de la tabla raza para meter datos
class MascotaRequestModel(BaseModel):
    nombre: str
    genero: str
    comentario: str
    estado: str
    clienteid: int
    razaid: int
    
#Modelo de la tabla especie para consultar datos
class MascotaResponseModel(MascotaRequestModel):
    id: int 

#detalleventa
#Modelo de la tabla raza para meter datos
class DetalleVentaRequestModel(BaseModel):
    precioservicio: float
    serviciosid: int
    citaid: int

#Modelo de la tabla especie para consultar datos
class DetalleVentaResponseModel(DetalleVentaRequestModel):
    id: int 

#Cita
class citaBaseEntrada(BaseModel):
    fecha: str
    hora:str
    comentario: str
    estado:str
    trabajadorId: int
    servicioId: int
    mascotaId: int

#class citaCreate(userBase):
#    contraseña:str

class citaFinal(citaBaseEntrada):
    id:int
    fechaActual:str
    
class citaPay(BaseModel):
#    total: Optional[float] 
    fechaPago: Optional[str]  
#    detalleVentaId: Optional[int] 






#Caja
class cajaAbre(BaseModel):
    horaIncio: str
    dineroInicial:float
    trabajadorId: int


class cajaCierra(BaseModel):
    dineroFinal: float
    horaFinal:str


#class citaCreate(userBase):
#    contraseña:str

class cajaTotal(BaseModel):
    id:int
    fecha:str
    horaIncio: str
    dineroInicial:float
    trabajadorId: int
    dineroFinal: float
    horaFinal:str
    
#class citaPay(BaseModel):
#    total: Optional[float] 
#    fechaPago: Optional[str]  
#    detalleVentaId: Optional[int] 
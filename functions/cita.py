#Cita y DetalleVenta
from datetime import date
from database import Cita, DetalleVenta, Mascota
from database import Trabajador
from shemas import DetalleVentaRequestModel, DetalleVentaResponseModel #Modelo para una peticion de usuario
from shemas import citaBaseEntrada, citaFinal, citaPay
import json

from fastapi import HTTPException #, Request
from peewee import DoesNotExist


#Historial
async def get_historial(id_mascota):
    
        mascota = Mascota.select().where(Mascota.id == id_mascota).first()

        cita = Cita.select().where(Cita.mascotaid == mascota.id)
        if cita:
            resultados = []
            for index in cita:
                
                modelo = {'id': index.id, 'fechaActual': index.fechaActual,
                            'fecha': index.fecha, #'hora': index.hora, 'comentario': index.comentario,
                            'estado': index.estado, 
                            'trabajadorId': index.trabajadorId.id, 
                            'trabajadorNombre': index.trabajadorId.nombre, 
                            'servicioId': index.servicioid.id, 
                            'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id,
                            'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 
                            'fechaPago': index.FechaPago } #'detalleVentaId': None, 'detalleVentaPrecio': None,
                resultados.append(modelo)
            return resultados
        else:
            return HTTPException(404, 'Cita not found')

#pagar
async def create_pago(cita_id, pago_request: citaPay):
    #detalle = create_detalleVenta(detalle_request)
    detalle = DetalleVenta.select().where(DetalleVenta.citaid == cita_id)
#    detalle = DetalleVenta.get(DetalleVenta.citaid == cita_id)
    
    suma = 0.0
    #resultados = []
    for index in detalle:
        suma = suma + float(index.precioservicio)

    cita = Cita.get(Cita.id == cita_id)

    if cita:
        #for index, item in pago_request:
        cita.estado = 'realizado'
        setattr(cita, 'estado', 'realizado')
        setattr(cita, 'total', suma)
        setattr(cita, 'FechaPago', pago_request.fechaPago)
        cita.save()
        return True
    else:
        return HTTPException(404, 'Cita not found')
    #return suma

#DetalleVenta
async def create_detalleVenta(detalle_request: DetalleVentaRequestModel):
    
    detalle_request = DetalleVenta.create(
#        id = 1,
        precioservicio = detalle_request.precioservicio,
        serviciosid= detalle_request.serviciosid,
        citaid = detalle_request.citaid
    )
    return detalle_request

async def get_detalleVenta(dellate_id):
    detalle = DetalleVenta.select().where(DetalleVenta.id == dellate_id).first()

    if detalle:    
        return DetalleVentaResponseModel( id=detalle.id ,precioservicio=detalle.precioservicio, serviciosid=detalle.serviciosid.id)
    else:
        return HTTPException(404, 'Detalle Venta not found')

async def update_detalleVenta(dellate_id, detalle_request: DetalleVentaRequestModel):
    detalle = DetalleVenta.select().where(DetalleVenta.id == dellate_id).first()

    if detalle:
        for index, item in detalle_request:
            setattr(detalle, index, item)
        detalle.save()
        return True
    else:
        return HTTPException(404, 'Detalle Venta not found')

async def get_detalleVentas():
    detalle = DetalleVenta.select()
    if detalle:
        resultados = []
        for index in detalle:
            detail = DetalleVentaResponseModel(id=index.id ,precioservicio=index.precioservicio, serviciosid=index.serviciosid.id)
            modelo = {'id': detail.id, 'precioservicio': detail.precioservicio, 'servicioid': detail.serviciosid}
            resultados.append(modelo)
        json_result = json.dumps({'DetalleVenta': resultados})
        data = json.loads(json_result)
        return data
    else:
        return HTTPException(404, 'Detalle Venta not found')

#Cita
async def create_cita(cita_request: citaBaseEntrada):
    #print("rgkjndfklbnkled")
    #print(cita_request)
    #print("rgkjndfklbnkled")
    #t1=Trabajador(id=3)
    #X=t1.insert(id=3)
    #print(X)
    #X.execute()
    x = Cita()
    w= x.insert(
        fechaActual= date.today(),
        fecha = cita_request.fecha,
        hora= cita_request.hora,
        comentario = cita_request.comentario,
        estado = cita_request.estado,
        trabajadorId = cita_request.trabajadorId,
        servicioid = cita_request.servicioId,
        mascotaid = cita_request.mascotaId
    )
    return w.execute()

async def get_citaid(cita_id):
    #cita = Cita.select().where(Cita.id == cita_id).first()
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #return cita.detalleventaid
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #return True
    #return cita
    #if cita:    
    #    return citaPay( id=cita.id ,fechaActual=cita.fechaActual, fecha=cita.fecha, hora=cita.hora, comentario=cita.comentario, estado=cita.estado, trabajadorId=cita.trabajadorId.id, servicioId=cita.servicioid.id, mascotaId=cita.mascotaid.id, total=cita.total, fechaPago=cita.FechaPago, detalleVentaId=cita.detalleventaid.id)
    #else:
    #    return HTTPException(404, 'Cita not found')
    try:
        cita = Cita.get(Cita.id == cita_id)
        #modelo = []
        if cita.total == None:
            modelo = {'id': cita.id, 'fechaActual': cita.fechaActual, 'fecha': cita.fecha, 'hora': cita.hora, 'comentario': cita.comentario, 'estado': cita.estado, 'trabajadorId': cita.trabajadorId.id, 'trabajadorNombre': cita.trabajadorId.nombre, 'servicioId': cita.servicioid.id, 'servicioNombre': cita.servicioid.nombre, 'mascotaId': cita.mascotaid.id, 'mascotaNombre': cita.mascotaid.nombre, 'total': cita.total, 'fechaPago': cita.FechaPago } #'detalleVentaId': None, 'detalleVentaPrecio': None,
        else:
            modelo = {'id': cita.id, 'fechaActual': cita.fechaActual, 'fecha': cita.fecha, 'hora': cita.hora, 'comentario': cita.comentario, 'estado': cita.estado, 'trabajadorId': cita.trabajadorId.id, 'trabajadorNombre': cita.trabajadorId.nombre, 'servicioId': cita.servicioid.id, 'servicioNombre': cita.servicioid.nombre, 'mascotaId': cita.mascotaid.id, 'mascotaNombre': cita.mascotaid.nombre, 'total': cita.total, 'fechaPago': cita.FechaPago } #'detalleVentaId': cita.detalleventaid.id, 'detalleVentaPrecio': cita.detalleventaid.precioservicio,
    #citaPay(id=cita.id, fechaActual=cita.fechaActual, fecha=cita.fecha, hora=cita.hora, comentario=cita.comentario, estado=cita.estado, trabajadorId=cita.trabajadorId.id, servicioId=cita.servicioid.id, mascotaId=cita.mascotaid.id, total=cita.total, fechaPago=cita.FechaPago)
        return modelo

    except DoesNotExist:
        return HTTPException(404, 'Cita not found')

#editar
async def update_cita(cita_id, cita_request: citaBaseEntrada):
    cita = Cita.get(Cita.id == cita_id)

    if cita:
        for index, item in cita_request:
            setattr(cita, index, item)
        cita.save()
        return True
    else:
        return HTTPException(404, 'Cita not found')

#Correcto
async def get_citadoctor(cita_doctor):
    #cita = Cita.select().where(Cita.id == cita_id).first()
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #return cita.detalleventaid
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #return True
    #return cita
    #if cita:    
    #    return citaPay( id=cita.id ,fechaActual=cita.fechaActual, fecha=cita.fecha, hora=cita.hora, comentario=cita.comentario, estado=cita.estado, trabajadorId=cita.trabajadorId.id, servicioId=cita.servicioid.id, mascotaId=cita.mascotaid.id, total=cita.total, fechaPago=cita.FechaPago, detalleVentaId=cita.detalleventaid.id)
    #else:
    #    return HTTPException(404, 'Cita not found')
    #try:
        trabajador = Trabajador.select().where(Trabajador.nombre == cita_doctor).first()

        cita = Cita.select().where(Cita.trabajadorId == trabajador.id)
        if cita:
            resultados = []
            for index in cita:
                #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                #print(index.id)
                if index.total == None:
                    modelo = {'id': index.id, 'fechaActual': index.fechaActual,
                                'fecha': index.fecha, 'hora': index.hora, 
                                'comentario': index.comentario, 'estado': index.estado, 
                                'trabajadorId': index.trabajadorId.id, 
                                'trabajadorNombre': index.trabajadorId.nombre, 
                                'servicioId': index.servicioid.id, 
                                'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id,
                                'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 
                                'fechaPago': index.FechaPago } #'detalleVentaId': None, 'detalleVentaPrecio': None,
                else:
                    modelo = {'id': index.id, 'fechaActual': index.fechaActual, 'fecha': index.fecha, 
                                'hora': index.hora, 'comentario': index.comentario, 'estado': index.estado, 
                                'trabajadorId': index.trabajadorId.id, 
                                'trabajadorNombre': index.trabajadorId.nombre, 'servicioId': index.servicioid.id, 
                                'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id, 
                                'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 
                                'fechaPago': index.FechaPago } #'detalleVentaId': cita.detalleventaid.id, 'detalleVentaPrecio': cita.detalleventaid.precioservicio,
                resultados.append(modelo)
                # print(modelo)
            #json_result = json.dumps({'Cita': resultados})
            #data = json.loads(json_result)
            return resultados
            #return index
        #return trabajador
        else:
            return HTTPException(404, 'Cita not found')
    
    #except DoesNotExist:
    #    return HTTPException(404, 'Cita no not found')
    

async def get_citaactivas():
        cita = Cita.select().where(Cita.estado == "activo")
        if cita:
            resultados = []
            for index in cita:
                
                if index.total == None:
                    modelo = {'id': index.id, 'fechaActual': index.fechaActual, 'fecha': index.fecha, 'hora': index.hora, 
                                'comentario': index.comentario, 'estado': index.estado, 'trabajadorId': index.trabajadorId.id, 
                                'trabajadorNombre': index.trabajadorId.nombre, 'servicioId': index.servicioid.id, 
                                'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id, 
                                'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 'fechaPago': index.FechaPago } #'detalleVentaId': None, 'detalleVentaPrecio': None,
                else:
                    modelo = {'id': index.id, 'fechaActual': index.fechaActual, 'fecha': index.fecha, 'hora': index.hora, 
                                'comentario': index.comentario, 'estado': index.estado, 'trabajadorId': index.trabajadorId.id, 
                                'trabajadorNombre': index.trabajadorId.nombre, 'servicioId': index.servicioid.id, 
                                'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id, 
                                'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 'fechaPago': index.FechaPago } #'detalleVentaId': cita.detalleventaid.id, 'detalleVentaPrecio': cita.detalleventaid.precioservicio,
                resultados.append(modelo)
            #json_result = json.dumps({'Cita': resultados})
            #data = json.loads(json_result)
            return resultados
        else:
            return HTTPException(404, 'Cita not found')

async def get_citadia(cita_dia):
#        print(cita_dia)
#        return cita_dia
    cita = Cita.select().where(Cita.fecha == cita_dia)
    if not cita:
        return HTTPException(404, 'Cita not found')
    if cita:
        resultados = []
        for index in cita:            
            if index.total == None:
                modelo = {'id': index.id, 'fechaActual': index.fechaActual, 'fecha': index.fecha, 'hora': index.hora, 
                            'comentario': index.comentario, 'estado': index.estado, 'trabajadorId': index.trabajadorId.id, 
                            'trabajadorNombre': index.trabajadorId.nombre, 'servicioId': index.servicioid.id, 
                            'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id, 
                            'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 'fechaPago': index.FechaPago } 
            else:
                modelo = {'id': index.id, 'fechaActual': index.fechaActual, 'fecha': index.fecha, 'hora': index.hora, 
                            'comentario': index.comentario, 'estado': index.estado, 'trabajadorId': index.trabajadorId.id, 
                            'trabajadorNombre': index.trabajadorId.nombre, 'servicioId': index.servicioid.id, 
                            'servicioNombre': index.servicioid.nombre, 'mascotaId': index.mascotaid.id, 
                            'mascotaNombre': index.mascotaid.nombre, 'total': index.total, 'fechaPago': index.FechaPago }
            resultados.append(modelo)
        #json_result = json.dumps({'Cita': resultados})
        #data = json.loads(json_result)
        return resultados
    else:
        return HTTPException(404, 'Cita not found')



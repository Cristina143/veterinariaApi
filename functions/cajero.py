from datetime import date
from database import Cajero
from shemas import cajaAbre,cajaCierra,cajaTotal 
import json

from fastapi import HTTPException #, Request

async def abrir_caja(caja_request: cajaAbre):
    x = Cajero()
    w= x.insert(
        fecha= date.today(),
        horaIncio = caja_request.horaIncio,
        dineroInicial= caja_request.dineroInicial,
        trabajadorId = caja_request.trabajadorId
    )
    return w.execute()

async def cerrar_caja(caja_id,caja_request: cajaCierra):
    caja = Cajero.get(Cajero.id == caja_id)
    if caja:
        setattr(caja, 'dineroFinal', caja_request.dineroFinal)
        setattr(caja, 'horaFinal', caja_request.horaFinal)

        caja.save()
        return True
    else:
        return HTTPException(404, 'Caja not found')

async def get_caja(caja_fecha):
        caja = Cajero.select().where(Cajero.fecha == caja_fecha)
        if caja:
            resultados = []
            for index in caja:
                
                if index.horaFinal == None:
                    modelo = {'id': index.id, 'fecha': index.fecha, 'horaIncio': index.horaIncio, 'trabajadorId': index.trabajadorId, 
                                'dineroFinal': None, 'horaFinal': None} #'detalleVentaId': None, 'detalleVentaPrecio': None,
                else:
                    modelo = {'id': index.id, 'fecha': index.fecha, 'horaIncio': index.horaIncio, 'trabajadorId': index.trabajadorId, 
                                'dineroFinal': index.dineroFinal, 'horaFinal': index.horaFinal} #'detalleVentaId': cita.detalleventaid.id, 'detalleVentaPrecio': cita.detalleventaid.precioservicio,
                resultados.append(modelo)
            return resultados
        else:
            return HTTPException(404, 'Caja not found')
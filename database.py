from peewee import * 
#from data

DB = MySQLDatabase(
    'veterinaria',
    user='root', password='1234',host='localhost', port=3306
)

#DB = MySQLDatabase(
#    'bijvvabu08kdtvu6jmrh',
#    user='uysu7x5mzm3etwer', password='2CMtDvpuiVUuVwhXCOii',host='bijvvabu08kdtvu6jmrh-mysql.services.clever-cloud.com', port=3306
#)

#modelos para representar una tabla
#trabajador
class Trabajador(Model):
    id = AutoField()
    nombre= CharField(max_length=80)
    telefono=CharField(max_length=45)
    fechaContrato= DateField() #DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])  #CharField(max_length=45) 
    password=CharField(max_length=45)
    correo=CharField(45)
    tipoUsuario=CharField(45)

#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'trabajador'

#cliente
class Cliente(Model):
    id = AutoField()#IntegerField()
    nombre= CharField(max_length=80)
    correo=CharField(45)
    telefono=CharField(max_length=45)
    direccion=CharField(max_length=45)
    estado=CharField(max_length=45)

#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'cliente'

#servicio
class Servicio(Model):
    id = AutoField() #IntegerField()
    nombre= CharField(max_length=80)
    precio=FloatField()

#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'servicio'

#especie
class Especie(Model):
    id = AutoField()#IntegerField()
    especie = CharField(max_length=80, unique=True)

#sobreescribir el archivo str
    def __str__(self):
        return self.especie
    
    class Meta:
        database = DB
        table_name = 'especie'

#raza
class Raza(Model):
    id = AutoField()#IntegerField()
    raza= CharField(max_length=80, unique=True)
    especie_nombre = ForeignKeyField(Especie, backref='especie_animal', column_name = 'especie_nombre', to_field='especie')

#sobreescribir el archivo str
    def __str__(self):
        return self.raza
    
    class Meta:
        database = DB
        table_name = 'raza'

#mascota
class Mascota(Model):
    id = AutoField() #IntegerField(PrimaryKey=True)
    nombre= CharField(max_length=80)
    genero= CharField(max_length=45, null=True)
    comentario= CharField(max_length=200, null=True)
    estado= CharField(max_length=45)
    clienteid = ForeignKeyField(Cliente, field='id', backref='mascota', column_name='clienteid')
    raza_nombre = ForeignKeyField(Raza, backref='raza_animal', column_name = 'raza_nombre', to_field='raza')

#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'mascota'


#falta
#Cita
class Cita(Model):
    id = AutoField()#IntegerField()
    fechaActual = DateField()
    fecha= CharField(max_length=45)
    hora= CharField(max_length=45)
    comentario= CharField(max_length=200, null=True)
    estado= CharField(max_length=45)
    trabajadorId = ForeignKeyField(Trabajador, field="id", column_name='trabajadorId')
    servicioid = ForeignKeyField(model=Servicio, field='id', column_name='serviciosid')
    mascotaid = ForeignKeyField(model=Mascota, field='id', column_name='mascotasid')
    total = FloatField(null=True)
    FechaPago=CharField(max_length=45,null=True)
#    detalleventaid = ForeignKeyField(model=DetalleVenta, field='id', backref='cita', column_name='detalleventaid')

#sobreescribir el archivo str
    def __str__(self):
        return self.id
    
    class Meta:
        database = DB
        table_name = 'cita'

#DetalleVenta
class DetalleVenta(Model):
    id = AutoField() #IntegerField(PrimaryKey=True)
    precioservicio= FloatField(null=True)
    serviciosid = ForeignKeyField(Servicio, field='id', backref='detalleventa', column_name='serviciosid')
    citaid =  ForeignKeyField(Cita, field='id', backref='detalleventa', column_name='citaid')

#sobreescribir el archivo str
    def __str__(self):
        return self.nombre
    
    class Meta:
        database = DB
        table_name = 'detalleventa'

#cajero
class Cajero(Model):
    id = AutoField() #IntegerField(PrimaryKey=True)
    fecha= DateField()
    horaIncio= CharField(max_length=45)
    dineroInicial= FloatField()
    dineroFinal= FloatField(null=True)
    horaFinal = CharField(max_length=45, null=True)
    trabajadorid = ForeignKeyField(Trabajador, field="id", backref='mascota', column_name='trabajadorId')

#sobreescribir el archivo str
    def __str__(self):
        return self.fecha
    
    class Meta:
        database = DB
        table_name = 'cajero'


class llavesmaestra(Model):
    id = AutoField()
    llave= TextField()
    experacion=DateTimeField()

#sobreescribir el archivo str
    def __str__(self):
        return self.id
    
    class Meta:
        database = DB
        table_name = 'llavesmaestra'
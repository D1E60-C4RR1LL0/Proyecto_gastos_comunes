from . import db

# Modelo de Acceso
class Acceso(db.Model):
    __tablename__ = 'acceso'
    username = db.Column('username', db.String(50), primary_key=True)
    password = db.Column('password', db.String(100), nullable=False)
    fechaCreacion = db.Column('fechacreacion', db.DateTime, nullable=False)
    fechaUltimoAcceso = db.Column('fechaultimoacceso', db.DateTime)
    Rut = db.Column('rut', db.String(12), unique=True, nullable=False)
    Tipo = db.Column('tipo', db.String(20), nullable=False)  # Rol del usuario: "administrador", "arrendatario", etc.

    # Relación con los departamentos asignados
    departamentos = db.relationship('Departamento', backref='usuario', primaryjoin="Departamento.RutArre == Acceso.Rut")


# Modelo de Propietarios
class Propietario(db.Model):
    __tablename__ = 'propietarios'
    RutProp = db.Column('rutprop', db.String(12), primary_key=True)
    Nombre = db.Column('nombre', db.String(50), nullable=False)
    ApePat = db.Column('apepat', db.String(50))
    ApeMat = db.Column('apemat', db.String(50))
    Email = db.Column('email', db.String(100), nullable=False)
    Fono1 = db.Column('fono1', db.String(15))
    Fono2 = db.Column('fono2', db.String(15))
    Estado = db.Column('estado', db.Boolean, nullable=False)

# Modelo de Arrendatarios
class Arrendatario(db.Model):
    __tablename__ = 'arrendatarios'
    RutArre = db.Column('rutarre', db.String(12), primary_key=True)
    Nombre = db.Column('nombre', db.String(50), nullable=False)
    ApePat = db.Column('apepat', db.String(50))
    ApeMat = db.Column('apemat', db.String(50))
    Email = db.Column('email', db.String(100), nullable=False)
    Fono1 = db.Column('fono1', db.String(15))
    Fono2 = db.Column('fono2', db.String(15))
    Estado = db.Column('estado', db.Boolean, nullable=False)

# Modelo de Personal
class Personal(db.Model):
    __tablename__ = 'personal'
    RutPersonal = db.Column('rutpersonal', db.String(12), primary_key=True)
    Nombre = db.Column('nombre', db.String(50), nullable=False)
    ApePat = db.Column('apepat', db.String(50))
    ApeMat = db.Column('apemat', db.String(50))
    Email = db.Column('email', db.String(100), nullable=False)
    Fono1 = db.Column('fono1', db.String(15))
    Fono2 = db.Column('fono2', db.String(15))
    Estado = db.Column('estado', db.Boolean, nullable=False)
    IDCargo = db.Column('idcargo', db.Integer, db.ForeignKey('cargos.idcargo'))
    HoraInicioJ = db.Column('horainicioj', db.Time)
    FechaFinJ = db.Column('fechafinj', db.Date)

# Modelo de Edificios
class Edificio(db.Model):
    __tablename__ = 'edificios'
    Cod = db.Column('cod', db.Integer, primary_key=True)
    Nombre = db.Column('nombre', db.String(100))
    Direccion = db.Column('direccion', db.String(200))
    Inmobiliaria = db.Column('inmobiliaria', db.String(100))
    Lat = db.Column('lat', db.Float)
    Log = db.Column('log', db.Float)
    Estado = db.Column('estado', db.Boolean, nullable=False)
    NPisos = db.Column('npisos', db.Integer, nullable=False)
    ValorGastoComun = db.Column('valorgastocomun', db.Float, nullable=False)

# Modelo de Departamentos
class Departamento(db.Model):
    __tablename__ = 'departamentos'
    Numero = db.Column('numero', db.Integer, primary_key=True)  # Clave primaria
    Piso = db.Column('piso', db.Integer, nullable=False)
    Arrendado = db.Column('arrendado', db.Boolean, nullable=False, default=False)
    RutProp = db.Column('rutprop', db.String(12), db.ForeignKey('propietarios.rutprop'))
    RutArre = db.Column('rutarre', db.String(12), db.ForeignKey('acceso.rut'))  # Relación con el modelo Acceso
    Estado = db.Column('estado', db.Boolean, nullable=False, default=True)
    FechaIniC = db.Column('fechainic', db.Date, nullable=True)
    FechaFinC = db.Column('fechafinc', db.Date, nullable=True)
    Observacion = db.Column('observacion', db.Text, nullable=True)
    NumHab = db.Column('numhab', db.Integer, nullable=True)
    NumBaños = db.Column('numbaños', db.Integer, nullable=True)

    # Relación con Acceso (usuarios)
    arrendatario = db.relationship('Acceso', backref='departamento', foreign_keys=[RutArre])




# Modelo de Reclamos
class Reclamo(db.Model):
    __tablename__ = 'reclamos'
    IDReclamo = db.Column('idreclamo', db.Integer, primary_key=True)
    FechaReclamo = db.Column('fechareclamo', db.Date, nullable=False)
    TextoReclamo = db.Column('textoreclamo', db.Text, nullable=False)
    IdTipoReclamo = db.Column('idtiporeclamo', db.Integer, db.ForeignKey('tiposreclamo.idtiporeclamo'))
    RutArre = db.Column('rutarre', db.String(12), db.ForeignKey('arrendatarios.rutarre'))
    Visto = db.Column('visto', db.Boolean, default=False)
    FechaVisto = db.Column('fechavisto', db.Date)
    Estado = db.Column('estado', db.String(20), default="Pendiente")  # Cambiar a String

# Modelo de CuotasGC
class CuotaGC(db.Model):
    __tablename__ = 'cuotasgc'
    IdCuotaGC = db.Column('idcuotagc', db.Integer, primary_key=True)
    CodDepto = db.Column('coddepto', db.Integer, db.ForeignKey('departamentos.numero'))
    Mes = db.Column('mes', db.Integer, nullable=False)
    Año = db.Column('año', db.Integer, nullable=False)
    ValorPagado = db.Column('valorpagado', db.Float, default=0.0)
    FechaPago = db.Column('fechapago', db.Date)
    Atrasado = db.Column('atrasado', db.Boolean, default=False)
    Estado = db.Column('estado', db.String(20), default="pendiente")  # Estados: "pendiente", "pagado", "atrasado"
    ValorCobrado = db.Column('valorcobrado', db.Float, nullable=False, default=0.0)  # Campo ajustado



# Modelo de Proyecto
class Proyecto(db.Model):
    __tablename__ = 'proyecto'
    IdProy = db.Column('idproy', db.Integer, primary_key=True)
    Motivo = db.Column('motivo', db.Text, nullable=False)
    Valor = db.Column('valor', db.Float, nullable=False)
    FechaInicioCobros = db.Column('fechainiciocobros', db.Date, nullable=False)
    FechaFinCobros = db.Column('fechafincobros', db.Date)
    Estado = db.Column('estado', db.Boolean, nullable=False)

# Modelo de ProyectoDepto
class ProyectoDepto(db.Model):
    __tablename__ = 'proyectodepto'
    IdProy = db.Column('idproy', db.Integer, db.ForeignKey('proyecto.idproy'), primary_key=True)
    CodDepto = db.Column('coddepto', db.Integer, db.ForeignKey('departamentos.numero'), primary_key=True)
    FechaPago = db.Column('fechapago', db.Date)
    ValorPagado = db.Column('valorpagado', db.Float)

# Modelo de Cargos
class Cargo(db.Model):
    __tablename__ = 'cargos'
    IDCargo = db.Column('idcargo', db.Integer, primary_key=True)
    NombreCargo = db.Column('nombrecargo', db.String(50), nullable=False)

# Modelo de TiposReclamo
class TipoReclamo(db.Model):
    __tablename__ = 'tiposreclamo'
    IDTipoReclamo = db.Column('idtiporeclamo', db.Integer, primary_key=True)
    Descripcion = db.Column('descripcion', db.Text, nullable=False)

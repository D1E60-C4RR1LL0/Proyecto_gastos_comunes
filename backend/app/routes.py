from flask import Blueprint, jsonify, request
from datetime import datetime, time
from .models import db, Acceso, Propietario, Arrendatario, Personal, Departamento, CuotaGC, Reclamo, Proyecto, ProyectoDepto, Cargo, TipoReclamo, Edificio

# Definir el Blueprint para las rutas
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de gestión de gastos comunes"}), 200

# --- ACCESO (GESTIÓN DE USUARIOS) ---
@main.route('/acceso', methods=['POST'])
def create_access():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ["username", "password", "Tipo"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Verificar si el usuario ya existe
        if Acceso.query.filter_by(username=data['username']).first():
            return jsonify({"error": "El nombre de usuario ya está registrado"}), 409

        # Crear un nuevo usuario
        nuevo_acceso = Acceso(
            username=data['username'],
            password=data['password'], 
            fechaCreacion=datetime.now(),
            Tipo=data['Tipo'],
            Rut=data.get('Rut') 
        )

        # Agregar a la base de datos
        db.session.add(nuevo_acceso)
        db.session.commit()

        return jsonify({"message": "Usuario registrado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/acceso/login', methods=['POST'])
def login():
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validar existencia del usuario
        acceso = Acceso.query.filter_by(username=username).first()
        if not acceso or acceso.password != password:  # Compara hash en producción
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Actualizar la fecha de último acceso
        acceso.fechaUltimoAcceso = datetime.now()
        db.session.commit()

        return jsonify({"message": "Autenticación exitosa", "Tipo": acceso.Tipo}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/acceso', methods=['GET'])
def get_all_users():
    try:
        usuarios = Acceso.query.all()
        return jsonify([{
            "username": usuario.username,
            "Tipo": usuario.Tipo,
            "fechaCreacion": usuario.fechaCreacion.strftime('%Y-%m-%d %H:%M:%S'),
            "fechaUltimoAcceso": usuario.fechaUltimoAcceso.strftime('%Y-%m-%d %H:%M:%S') if usuario.fechaUltimoAcceso else None
        } for usuario in usuarios]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/acceso/<username>', methods=['GET'])
def get_user(username):
    try:
        usuario = Acceso.query.filter_by(username=username).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "username": usuario.username,
            "Tipo": usuario.Tipo,
            "fechaCreacion": usuario.fechaCreacion.strftime('%Y-%m-%d %H:%M:%S'),
            "fechaUltimoAcceso": usuario.fechaUltimoAcceso.strftime('%Y-%m-%d %H:%M:%S') if usuario.fechaUltimoAcceso else None
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/acceso/<username>', methods=['PUT'])
def update_user(username):
    try:
        # Buscar el usuario
        usuario = Acceso.query.filter_by(username=username).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar los campos permitidos
        data = request.get_json()
        if "password" in data:
            usuario.password = data['password']  # Recuerda aplicar hash en producción
        if "Tipo" in data:
            usuario.Tipo = data['Tipo']
        if "Rut" in data:
            usuario.Rut = data['Rut']

        db.session.commit()
        return jsonify({"message": "Usuario actualizado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/acceso/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        # Buscar el usuario
        usuario = Acceso.query.filter_by(username=username).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --- PROPIETARIOS ---
@main.route('/propietarios', methods=['POST'])
def create_propietario():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()

        # Verificar que se envíen todos los datos requeridos
        if not data or 'RutProp' not in data or 'Nombre' not in data or 'Email' not in data or 'Estado' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Crear un nuevo propietario
        nuevo_propietario = Propietario(
            RutProp=data['RutProp'],
            Nombre=data['Nombre'],
            ApePat=data.get('ApePat'),
            ApeMat=data.get('ApeMat'),
            Email=data['Email'],
            Fono1=data.get('Fono1'),
            Fono2=data.get('Fono2'),
            Estado=data['Estado']
        )

        # Agregarlo a la base de datos
        db.session.add(nuevo_propietario)
        db.session.commit()

        return jsonify({"message": "Propietario creado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/propietarios/<RutProp>', methods=['GET'])
def get_propietario(RutProp):
    propietario = Propietario.query.filter_by(RutProp=RutProp).first()
    if not propietario:
        return jsonify({"error": "Propietario no encontrado"}), 404
    return jsonify({
        "RutProp": propietario.RutProp,
        "Nombre": propietario.Nombre,
        "ApePat": propietario.ApePat,
        "ApeMat": propietario.ApeMat,
        "Email": propietario.Email,
        "Fono1": propietario.Fono1,
        "Fono2": propietario.Fono2,
        "Estado": propietario.Estado
    }), 200
    
@main.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([{
        "RutProp": propietario.RutProp,
        "Nombre": propietario.Nombre,
        "ApePat": propietario.ApePat,
        "ApeMat": propietario.ApeMat,
        "Email": propietario.Email,
        "Fono1": propietario.Fono1,
        "Fono2": propietario.Fono2,
        "Estado": propietario.Estado
    } for propietario in propietarios]), 200



@main.route('/propietarios/<RutProp>', methods=['PUT'])
def update_propietario(RutProp):
    data = request.get_json()
    propietario = Propietario.query.filter_by(RutProp=RutProp).first()
    if not propietario:
        return jsonify({"error": "Propietario no encontrado"}), 404
    for key, value in data.items():
        setattr(propietario, key, value)
    db.session.commit()
    return jsonify({"message": "Propietario actualizado con éxito"}), 200

@main.route('/propietarios/<RutProp>', methods=['DELETE'])
def delete_propietario(RutProp):
    propietario = Propietario.query.filter_by(RutProp=RutProp).first()
    if not propietario:
        return jsonify({"error": "Propietario no encontrado"}), 404
    db.session.delete(propietario)
    db.session.commit()
    return jsonify({"message": "Propietario eliminado"}), 200


# --- ARRENDATARIOS ---
@main.route('/arrendatarios', methods=['POST'])
def create_arrendatario():
    try:
        # Obtener los datos enviados en la solicitud
        data = request.get_json()

        # Verificar que se envíen todos los datos requeridos
        if not data or 'RutArre' not in data or 'Nombre' not in data or 'Email' not in data or 'Estado' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Crear un nuevo arrendatario
        nuevo_arrendatario = Arrendatario(
            RutArre=data['RutArre'],
            Nombre=data['Nombre'],
            ApePat=data.get('ApePat'),
            ApeMat=data.get('ApeMat'),
            Email=data['Email'],
            Fono1=data.get('Fono1'),
            Fono2=data.get('Fono2'),
            Estado=data['Estado']
        )

        # Guardar en la base de datos
        db.session.add(nuevo_arrendatario)
        db.session.commit()

        return jsonify({"message": "Arrendatario registrado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/arrendatarios', methods=['GET'])
def get_all_arrendatarios():
    try:
        # Consultar todos los arrendatarios en la base de datos
        arrendatarios = Arrendatario.query.all()

        # Crear una lista de arrendatarios en formato JSON
        resultado = []
        for arrendatario in arrendatarios:
            resultado.append({
                "RutArre": arrendatario.RutArre,
                "Nombre": arrendatario.Nombre,
                "ApePat": arrendatario.ApePat,
                "ApeMat": arrendatario.ApeMat,
                "Email": arrendatario.Email,
                "Fono1": arrendatario.Fono1,
                "Fono2": arrendatario.Fono2,
                "Estado": arrendatario.Estado
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@main.route('/arrendatarios/<RutArre>', methods=['GET'])
def get_arrendatario(RutArre):
    arrendatario = Arrendatario.query.filter_by(RutArre=RutArre).first()
    if not arrendatario:
        return jsonify({"error": "Arrendatario no encontrado"}), 404
    return jsonify({
        "RutArre": arrendatario.RutArre,
        "Nombre": arrendatario.Nombre,
        "ApePat": arrendatario.ApePat,
        "Email": arrendatario.Email,
        "Estado": arrendatario.Estado
    })

@main.route('/arrendatarios/<RutArre>', methods=['PUT'])
def update_arrendatario(RutArre):
    data = request.get_json()
    arrendatario = Arrendatario.query.filter_by(RutArre=RutArre).first()
    if not arrendatario:
        return jsonify({"error": "Arrendatario no encontrado"}), 404
    for key, value in data.items():
        setattr(arrendatario, key, value)
    db.session.commit()
    return jsonify({"message": "Arrendatario actualizado con éxito"}), 200

@main.route('/arrendatarios/<RutArre>', methods=['DELETE'])
def delete_arrendatario(RutArre):
    arrendatario = Arrendatario.query.filter_by(RutArre=RutArre).first()
    if not arrendatario:
        return jsonify({"error": "Arrendatario no encontrado"}), 404
    db.session.delete(arrendatario)
    db.session.commit()
    return jsonify({"message": "Arrendatario eliminado"}), 200

# --- PERSONAL ---
@main.route('/personal', methods=['GET'])
def get_all_personal():
    try:
        personal_list = Personal.query.all()
        return jsonify([
            {
                "RutPersonal": person.RutPersonal,
                "Nombre": person.Nombre,
                "ApePat": person.ApePat,
                "ApeMat": person.ApeMat,
                "Email": person.Email,
                "Fono1": person.Fono1,
                "Fono2": person.Fono2,
                "Estado": person.Estado,
                "IDCargo": person.IDCargo,
                "HoraInicioJ": person.HoraInicioJ.strftime('%H:%M:%S') if person.HoraInicioJ else None,
                "FechaFinJ": person.FechaFinJ.strftime('%Y-%m-%d') if person.FechaFinJ else None
            } for person in personal_list
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@main.route('/personal/<RutPersonal>', methods=['GET'])
def get_personal(RutPersonal):
    try:
        # Buscar el registro en la base de datos
        personal = Personal.query.filter_by(RutPersonal=RutPersonal).first()
        if not personal:
            return jsonify({"error": "Personal no encontrado"}), 404

        # Convertir los campos time y date a strings
        hora_inicio = personal.HoraInicioJ.strftime('%H:%M:%S') if personal.HoraInicioJ else None
        fecha_fin = personal.FechaFinJ.strftime('%Y-%m-%d') if personal.FechaFinJ else None

        # Construir la respuesta
        return jsonify({
            "RutPersonal": personal.RutPersonal,
            "Nombre": personal.Nombre,
            "ApePat": personal.ApePat,
            "ApeMat": personal.ApeMat,
            "Email": personal.Email,
            "Fono1": personal.Fono1,
            "Fono2": personal.Fono2,
            "Estado": personal.Estado,
            "IDCargo": personal.IDCargo,
            "HoraInicioJ": hora_inicio,
            "FechaFinJ": fecha_fin
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/personal/<RutPersonal>', methods=['PUT'])
def update_personal(RutPersonal):
    try:
        data = request.get_json()
        personal = Personal.query.filter_by(RutPersonal=RutPersonal).first()
        if not personal:
            return jsonify({"error": "Personal no encontrado"}), 404

        for key, value in data.items():
            setattr(personal, key, value)
        db.session.commit()
        return jsonify({"message": "Personal actualizado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/personal/<RutPersonal>', methods=['DELETE'])
def delete_personal(RutPersonal):
    try:
        personal = Personal.query.filter_by(RutPersonal=RutPersonal).first()
        if not personal:
            return jsonify({"error": "Personal no encontrado"}), 404

        db.session.delete(personal)
        db.session.commit()
        return jsonify({"message": "Personal eliminado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --- PROYECTOS ---
@main.route('/proyectos', methods=['POST'])
def create_proyecto():
    try:
        # Obtener datos enviados en la solicitud
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ["Motivo", "Valor", "FechaInicioCobros"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar que el valor sea positivo
        if data["Valor"] <= 0:
            return jsonify({"error": "El valor del proyecto debe ser positivo"}), 400

        # Validar fechas
        fecha_inicio = datetime.strptime(data["FechaInicioCobros"], '%Y-%m-%d')
        fecha_fin = datetime.strptime(data.get("FechaFinCobros", "2099-12-31"), '%Y-%m-%d')
        if fecha_inicio > fecha_fin:
            return jsonify({"error": "La fecha de inicio no puede ser posterior a la fecha de fin"}), 400

        # Crear el proyecto
        nuevo_proyecto = Proyecto(
            Motivo=data["Motivo"],
            Valor=data["Valor"],
            FechaInicioCobros=fecha_inicio,
            FechaFinCobros=fecha_fin if "FechaFinCobros" in data else None,
            Estado=data.get("Estado", "Activo")
        )
        db.session.add(nuevo_proyecto)
        db.session.commit()

        return jsonify({"message": "Proyecto creado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/proyectos/<int:IdProy>', methods=['GET'])
def get_proyecto(IdProy):
    try:
        proyecto = Proyecto.query.filter_by(IdProy=IdProy).first()
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        return jsonify({
            "IdProy": proyecto.IdProy,
            "Motivo": proyecto.Motivo,
            "Valor": proyecto.Valor,
            "FechaInicioCobros": proyecto.FechaInicioCobros.strftime('%Y-%m-%d') if proyecto.FechaInicioCobros else None,
            "FechaFinCobros": proyecto.FechaFinCobros.strftime('%Y-%m-%d') if proyecto.FechaFinCobros else None,
            "Estado": proyecto.Estado
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/proyectos', methods=['GET'])
def get_all_proyectos():
    try:
        proyectos = Proyecto.query.all()
        return jsonify([{
            "IdProy": proyecto.IdProy,
            "Motivo": proyecto.Motivo,
            "Valor": proyecto.Valor,
            "FechaInicioCobros": proyecto.FechaInicioCobros.strftime('%Y-%m-%d') if proyecto.FechaInicioCobros else None,
            "FechaFinCobros": proyecto.FechaFinCobros.strftime('%Y-%m-%d') if proyecto.FechaFinCobros else None,
            "Estado": proyecto.Estado
        } for proyecto in proyectos]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/proyectos/<int:IdProy>', methods=['PUT'])
def update_proyecto(IdProy):
    try:
        data = request.get_json()
        proyecto = Proyecto.query.filter_by(IdProy=IdProy).first()
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404

        # Actualizar los campos permitidos
        for key, value in data.items():
            if hasattr(proyecto, key):
                setattr(proyecto, key, value)

        db.session.commit()
        return jsonify({"message": "Proyecto actualizado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/proyectos/<int:IdProy>', methods=['DELETE'])
def delete_proyecto(IdProy):
    try:
        proyecto = Proyecto.query.filter_by(IdProy=IdProy).first()
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado"}), 404

        db.session.delete(proyecto)
        db.session.commit()
        return jsonify({"message": "Proyecto eliminado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# --- DEPARTAMENTOS ---
@main.route('/departamentos', methods=['POST'])
def create_departamento():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que se proporcionen los campos requeridos
        required_fields = ["Piso", "Numero", "Arrendado", "Estado"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Verificar si el departamento está arrendado
        arrendado = data["Arrendado"]
        if arrendado:
            # Si está arrendado, los campos relacionados con el arrendatario son obligatorios
            additional_required_fields = ["RutArre", "FechaIniC", "FechaFinC"]
            missing_additional_fields = [field for field in additional_required_fields if field not in data]
            if missing_additional_fields:
                return jsonify({"error": f"Faltan campos requeridos para un departamento arrendado: {', '.join(missing_additional_fields)}"}), 400

        # Crear un nuevo departamento
        nuevo_departamento = Departamento(
            Numero=data["Numero"],  # Usamos Numero como clave primaria
            Piso=data["Piso"],
            Arrendado=arrendado,
            RutProp=data.get("RutProp"),
            RutArre=data.get("RutArre") if arrendado else None,
            Estado=data["Estado"],
            FechaIniC=data.get("FechaIniC") if arrendado else None,
            FechaFinC=data.get("FechaFinC") if arrendado else None,
            Observacion=data.get("Observacion"),
            NumHab=data.get("NumHab"),
            NumBaños=data.get("NumBaños")
        )

        # Agregar el departamento a la base de datos
        db.session.add(nuevo_departamento)
        db.session.commit()

        return jsonify({"message": "Departamento creado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/departamentos/<int:Numero>', methods=['GET'])
def get_departamento(Numero):
    departamento = Departamento.query.filter_by(Numero=Numero).first()
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404
    return jsonify({
        "Numero": departamento.Numero,
        "Piso": departamento.Piso,
        "Arrendado": departamento.Arrendado,
        "RutProp": departamento.RutProp,
        "RutArre": departamento.RutArre,
        "Estado": departamento.Estado,
        "FechaIniC": departamento.FechaIniC,
        "FechaFinC": departamento.FechaFinC,
        "Observacion": departamento.Observacion,
        "NumHab": departamento.NumHab,
        "NumBaños": departamento.NumBaños
    }), 200
    
@main.route('/mis_departamentos', methods=['GET'])
def mis_departamentos():
    rut = request.args.get('rut')  # Obtener el rut desde el token en un sistema completo
    usuario = Acceso.query.filter_by(Rut=rut).first()

    if not usuario or usuario.Tipo != "arrendatario":
        return jsonify({"error": "Acceso no autorizado"}), 403

    departamentos = Departamento.query.filter_by(RutArre=usuario.Rut).all()

    return jsonify([{
        "Numero": depto.Numero,
        "Piso": depto.Piso,
        "Estado": depto.Estado,
        "Arrendado": depto.Arrendado
    } for depto in departamentos]), 200




@main.route('/departamentos/<int:Numero>', methods=['PUT'])
def update_departamento(Numero):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        departamento = Departamento.query.filter_by(Numero=Numero).first()
        if not departamento:
            return jsonify({"error": "Departamento no encontrado"}), 404

        # Actualizar los campos permitidos
        for key, value in data.items():
            if hasattr(departamento, key):
                setattr(departamento, key, value)

        db.session.commit()
        return jsonify({"message": "Departamento actualizado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/departamentos/<int:Numero>', methods=['DELETE'])
def delete_departamento(Numero):
    try:
        departamento = Departamento.query.filter_by(Numero=Numero).first()
        if not departamento:
            return jsonify({"error": "Departamento no encontrado"}), 404

        db.session.delete(departamento)
        db.session.commit()
        return jsonify({"message": "Departamento eliminado"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/departamentos/<int:Numero>/asignar', methods=['PUT'])
def asignar_departamento(Numero):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        departamento = Departamento.query.filter_by(Numero=Numero).first()
        if not departamento:
            return jsonify({"error": "Departamento no encontrado"}), 404

        # Asignar propietario o arrendatario al departamento
        if "RutProp" in data:
            departamento.RutProp = data["RutProp"]
        if "RutArre" in data:
            departamento.RutArre = data["RutArre"]

        db.session.commit()
        return jsonify({"message": "Departamento asignado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




# --- CUOTAS DE GASTOS COMUNES ---
@main.route('/cuotasgc', methods=['POST'])
def create_cuota_gc():
    try:
        # Obtener los datos enviados en la solicitud
        data = request.get_json()

        # Validar que se envíen Mes, Año y Monto
        required_fields = ["Mes", "Año", "Monto"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Extraer datos
        mes = data["Mes"]
        año = data["Año"]
        monto = float(data["Monto"])  # Convertir a flotante

        # Obtener todos los departamentos
        departamentos = Departamento.query.all()
        if not departamentos:
            return jsonify({"error": "No se encontraron departamentos registrados"}), 404

        # Generar gastos comunes para todos los departamentos
        cuotas_generadas = []
        for depto in departamentos:
            nueva_cuota = CuotaGC(
                CodDepto=depto.Numero,
                Mes=mes,
                Año=año,
                ValorPagado=0.0,
                Estado="Pendiente",
                ValorCobrado=monto  # Nuevo campo para almacenar el monto
            )
            db.session.add(nueva_cuota)
            cuotas_generadas.append({
                "CodDepto": depto.Numero,
                "Mes": mes,
                "Año": año,
                "Monto": monto,
                "Estado": "Pendiente",
                "ValorPagado": 0.0
            })

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Respuesta con las cuotas generadas
        return jsonify({
            "message": "Gastos generados para todos los departamentos",
            "cuotas": cuotas_generadas
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/generar_gastos_comunes', methods=['POST'])
def generar_gastos_por_periodo():
    try:
        data = request.get_json()

        # Validar campos obligatorios
        required_fields = ["Mes", "Año", "Monto"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Filtros opcionales
        cod_depto = data.get("CodDepto")  # Para un departamento específico (opcional)

        if cod_depto:
            departamentos = Departamento.query.filter_by(Numero=cod_depto).all()
        else:
            departamentos = Departamento.query.all()

        if not departamentos:
            return jsonify({"error": "No se encontraron departamentos"}), 404

        # Crear las cuotas
        cuotas_generadas = []
        for depto in departamentos:
            nueva_cuota = CuotaGC(
                CodDepto=depto.Numero,
                Mes=data["Mes"],
                Año=data["Año"],
                ValorCobrado=data["Monto"],
                ValorPagado=0.0,
                Estado="Pendiente"
            )
            db.session.add(nueva_cuota)
            cuotas_generadas.append({
                "CodDepto": depto.Numero,
                "Mes": data["Mes"],
                "Año": data["Año"],
                "Monto": data["Monto"],
                "Estado": "Pendiente"
            })

        db.session.commit()
        return jsonify({"message": "Gastos comunes generados con éxito", "cuotas": cuotas_generadas}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@main.route('/mis_gastos_comunes', methods=['GET'])
def mis_gastos_comunes():
    try:
        rut = request.args.get('Rut')  # Obtenemos el RUT del usuario desde la solicitud.

        # Validar que el usuario exista y sea un arrendatario
        usuario = Acceso.query.filter_by(Rut=rut, Tipo="arrendatario").first()
        if not usuario:
            return jsonify({"error": "Usuario no autorizado"}), 403

        # Obtener los departamentos asignados al usuario
        departamentos = Departamento.query.filter_by(RutArre=rut).all()

        if not departamentos:
            return jsonify({"mensaje": "No tiene departamentos asignados"}), 404

        # Obtener los gastos comunes asociados a esos departamentos
        resultados = []
        for depto in departamentos:
            cuotas = CuotaGC.query.filter_by(CodDepto=depto.Numero).all()
            for cuota in cuotas:
                resultados.append({
                    "Departamento": depto.Numero,
                    "Mes": cuota.Mes,
                    "Año": cuota.Año,
                    "ValorCobrado": cuota.ValorCobrado,
                    "ValorPagado": cuota.ValorPagado,
                    "Estado": cuota.Estado,
                    "FechaPago": cuota.FechaPago.strftime('%Y-%m-%d') if cuota.FechaPago else None
                })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@main.route('/cuotasgc/<int:IdCuotaGC>', methods=['GET'])
def get_cuota_by_id(IdCuotaGC):
    try:
        cuota = CuotaGC.query.filter_by(IdCuotaGC=IdCuotaGC).first()
        if not cuota:
            return jsonify({"error": "Cuota no encontrada"}), 404

        return jsonify({
            "IdCuotaGC": cuota.IdCuotaGC,
            "CodDepto": cuota.CodDepto,
            "Mes": cuota.Mes,
            "Año": cuota.Año,
            "ValorPagado": cuota.ValorPagado,
            "FechaPago": cuota.FechaPago.strftime('%Y-%m-%d') if cuota.FechaPago else None,
            "Atrasado": cuota.Atrasado,
            "Estado": cuota.Estado
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/cuotasgc/departamento/<int:CodDepto>', methods=['GET'])
def get_cuotas_by_departamento(CodDepto):
    try:
        cuotas = CuotaGC.query.filter_by(CodDepto=CodDepto).order_by(CuotaGC.Año, CuotaGC.Mes).all()
        if not cuotas:
            return jsonify({"mensaje": "No se encontraron cuotas para este departamento"}), 404
        return jsonify([{
            "IdCuotaGC": cuota.IdCuotaGC,
            "Mes": cuota.Mes,
            "Año": cuota.Año,
            "ValorPagado": cuota.ValorPagado,
            "Estado": cuota.Estado
        } for cuota in cuotas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/cuotasgc/pendientes', methods=['GET'])
def get_cuotas_pendientes():
    try:
        hasta_mes = request.args.get('hasta_mes', type=int)
        hasta_año = request.args.get('hasta_año', type=int)

        if not hasta_mes or not hasta_año:
            return jsonify({"error": "Faltan los parámetros 'hasta_mes' y 'hasta_año'"}), 400

        pendientes = CuotaGC.query.filter(
            CuotaGC.ValorPagado == 0,
            (CuotaGC.Año < hasta_año) | 
            ((CuotaGC.Año == hasta_año) & (CuotaGC.Mes <= hasta_mes))
        ).order_by(CuotaGC.Año.asc(), CuotaGC.Mes.asc()).all()

        if not pendientes:
            return jsonify({"mensaje": "No hay cuotas pendientes"}), 200

        return jsonify([{
            "IdCuotaGC": cuota.IdCuotaGC,
            "CodDepto": cuota.CodDepto,
            "Mes": cuota.Mes,
            "Año": cuota.Año,
            "ValorPagado": cuota.ValorPagado,
            "Atrasado": cuota.Atrasado,
            "Estado": cuota.Estado  
        } for cuota in pendientes]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/cuotasgc', methods=['GET'])
def get_cuotas():
    cod_depto = request.args.get('CodDepto', type=int)
    mes = request.args.get('Mes', type=int)
    año = request.args.get('Año', type=int)

    query = CuotaGC.query
    if cod_depto:
        query = query.filter_by(CodDepto=cod_depto)
    if mes:
        query = query.filter_by(Mes=mes)
    if año:
        query = query.filter_by(Año=año)

    cuotas = query.order_by(CuotaGC.Año, CuotaGC.Mes).all()
    return jsonify([{
        "IdCuotaGC": cuota.IdCuotaGC,
        "CodDepto": cuota.CodDepto,
        "Mes": cuota.Mes,
        "Año": cuota.Año,
        "ValorPagado": cuota.ValorPagado,
        "Estado": cuota.Estado
    } for cuota in cuotas]), 200


    
@main.route('/cuotasgc/buscar', methods=['GET'])
def buscar_cuota():
    try:
        # Obtener los parámetros de la solicitud
        cod_depto = request.args.get('CodDepto', type=int)
        mes = request.args.get('Mes', type=int)
        año = request.args.get('Año', type=int)

        # Validar que los parámetros requeridos estén presentes
        if not cod_depto or not mes or not año:
            return jsonify({"error": "Faltan parámetros requeridos: CodDepto, Mes, Año"}), 400

        # Buscar la cuota en la base de datos
        cuota = CuotaGC.query.filter_by(CodDepto=cod_depto, Mes=mes, Año=año).first()

        # Verificar si la cuota fue encontrada
        if not cuota:
            return jsonify({"error": "No se encontró una cuota para los criterios proporcionados"}), 404

        # Construir la respuesta en formato JSON
        resultado = {
            "IdCuotaGC": cuota.IdCuotaGC,
            "CodDepto": cuota.CodDepto,
            "Mes": cuota.Mes,
            "Año": cuota.Año,
            "ValorPagado": cuota.ValorPagado,
            "FechaPago": cuota.FechaPago.strftime('%Y-%m-%d') if cuota.FechaPago else None,
            "Atrasado": cuota.Atrasado,
            "Estado": cuota.Estado
        }
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/cuotasgc/editar', methods=['PUT'])
def editar_cuota():
    try:
        # Obtener los parámetros de la solicitud
        cod_depto = request.args.get('CodDepto', type=int)
        mes = request.args.get('Mes', type=int)
        año = request.args.get('Año', type=int)

        # Validar que los parámetros requeridos estén presentes
        if not cod_depto or not mes or not año:
            return jsonify({"error": "Faltan parámetros requeridos: CodDepto, Mes, Año"}), 400

        # Buscar la cuota en la base de datos
        cuota = CuotaGC.query.filter_by(CodDepto=cod_depto, Mes=mes, Año=año).first()

        # Verificar si la cuota fue encontrada
        if not cuota:
            return jsonify({"error": "No se encontró una cuota para los criterios proporcionados"}), 404

        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()

        # Validar y actualizar los campos permitidos
        campos_actualizables = ["ValorPagado", "FechaPago", "Atrasado", "Estado"]
        for key, value in data.items():
            if key in campos_actualizables:
                setattr(cuota, key, value)

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Construir la respuesta en formato JSON
        resultado = {
            "IdCuotaGC": cuota.IdCuotaGC,
            "CodDepto": cuota.CodDepto,
            "Mes": cuota.Mes,
            "Año": cuota.Año,
            "ValorPagado": cuota.ValorPagado,
            "FechaPago": cuota.FechaPago.strftime('%Y-%m-%d') if cuota.FechaPago else None,
            "Atrasado": cuota.Atrasado,
            "Estado": cuota.Estado
        }
        return jsonify({"message": "Cuota actualizada con éxito", "cuota": resultado}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --- RECLAMOS ---
@main.route('/reclamos', methods=['POST'])
def create_reclamo():
    try:
        # Obtener datos enviados
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ["TextoReclamo", "FechaReclamo", "IdTipoReclamo", "RutArre"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Crear el reclamo
        nuevo_reclamo = Reclamo(
            FechaReclamo=data["FechaReclamo"],
            TextoReclamo=data["TextoReclamo"],
            IdTipoReclamo=data["IdTipoReclamo"],
            RutArre=data["RutArre"],
            Visto=data.get("Visto", False),
            FechaVisto=data.get("FechaVisto"),
            Estado=data.get("Estado", "Pendiente") 
        )

        # Guardar en la base de datos
        db.session.add(nuevo_reclamo)
        db.session.commit()

        return jsonify({"message": "Reclamo creado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@main.route('/reclamos/<IDReclamo>', methods=['GET'])
def get_reclamo(IDReclamo):
    reclamo = Reclamo.query.filter_by(IDReclamo=IDReclamo).first()
    if not reclamo:
        return jsonify({"error": "Reclamo no encontrado"}), 404
    return jsonify({
        "IDReclamo": reclamo.IDReclamo,
        "FechaReclamo": reclamo.FechaReclamo.strftime('%Y-%m-%d') if reclamo.FechaReclamo else None,
        "TextoReclamo": reclamo.TextoReclamo,
        "IdTipoReclamo": reclamo.IdTipoReclamo,
        "RutArre": reclamo.RutArre,
        "Visto": reclamo.Visto,
        "FechaVisto": reclamo.FechaVisto.strftime('%Y-%m-%d') if reclamo.FechaVisto else None,
        "Estado": reclamo.Estado
    }), 200
    
@main.route('/reclamos', methods=['GET'])
def get_all_reclamos():
    try:
        # Consulta todos los reclamos en la base de datos
        reclamos = Reclamo.query.all()

        # Devuelve una lista de reclamos en formato JSON
        return jsonify([
            {
                "IDReclamo": reclamo.IDReclamo,
                "FechaReclamo": reclamo.FechaReclamo.strftime('%Y-%m-%d') if reclamo.FechaReclamo else None,
                "TextoReclamo": reclamo.TextoReclamo,
                "IdTipoReclamo": reclamo.IdTipoReclamo,
                "RutArre": reclamo.RutArre,
                "Visto": reclamo.Visto,
                "FechaVisto": reclamo.FechaVisto.strftime('%Y-%m-%d') if reclamo.FechaVisto else None,
                "Estado": reclamo.Estado
            } for reclamo in reclamos
        ]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/reclamos/pendientes', methods=['GET'])
def get_reclamos_pendientes():
    try:
        # Obtener todos los reclamos con estado "Pendiente"
        reclamos_pendientes = Reclamo.query.filter_by(Estado="Pendiente").all()

        if not reclamos_pendientes:
            return jsonify({"mensaje": "No hay reclamos pendientes"}), 200

        # Formatear los resultados en una respuesta JSON
        resultado = [{
            "IDReclamo": reclamo.IDReclamo,
            "FechaReclamo": reclamo.FechaReclamo.strftime('%Y-%m-%d') if reclamo.FechaReclamo else None,
            "TextoReclamo": reclamo.TextoReclamo,
            "IdTipoReclamo": reclamo.IdTipoReclamo,
            "RutArre": reclamo.RutArre,
            "Visto": reclamo.Visto,
            "FechaVisto": reclamo.FechaVisto.strftime('%Y-%m-%d') if reclamo.FechaVisto else None,
            "Estado": reclamo.Estado
        } for reclamo in reclamos_pendientes]

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@main.route('/informes/reclamos', methods=['GET'])
def generar_informe_reclamos():
    try:
        reclamos = Reclamo.query.all()
        return jsonify([{
            "IdReclamo": reclamo.IDReclamo,
            "TextoReclamo": reclamo.TextoReclamo,
            "Estado": reclamo.Estado,
            "FechaReclamo": reclamo.FechaReclamo.strftime('%Y-%m-%d'),
        } for reclamo in reclamos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@main.route('/reclamos/<IDReclamo>/visto', methods=['PUT'])
def marcar_reclamo_visto(IDReclamo):
    try:
        # Buscar el reclamo
        reclamo = Reclamo.query.filter_by(IDReclamo=IDReclamo).first()
        if not reclamo:
            return jsonify({"error": "Reclamo no encontrado"}), 404

        # Marcar como visto y registrar la fecha
        reclamo.Visto = True
        reclamo.FechaVisto = datetime.now().strftime('%Y-%m-%d')  # Fecha actual
        reclamo.Estado = "Resuelto"  # Cambiar el estado a "Resuelto"
        
        db.session.commit()
        return jsonify({"message": "Reclamo marcado como visto"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/reclamos/<int:IDReclamo>', methods=['DELETE'])
def delete_reclamo(IDReclamo):
    try:
        # Buscar el reclamo en la base de datos
        reclamo = Reclamo.query.filter_by(IDReclamo=IDReclamo).first()
        
        if not reclamo:
            return jsonify({"error": "Reclamo no encontrado"}), 404

        # Eliminar el reclamo de la base de datos
        db.session.delete(reclamo)
        db.session.commit()
        
        return jsonify({"message": "Reclamo eliminado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# --- PROYECTO-DEPARTAMENTO ---

@main.route('/proyectodepto', methods=['POST'])
def create_proyecto_depto():
    try:
        # Obtener datos enviados en la solicitud
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ["IdProy", "CodDepto"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar que el proyecto exista
        proyecto = Proyecto.query.filter_by(IdProy=data["IdProy"]).first()
        if not proyecto:
            return jsonify({"error": f"El proyecto con IdProy={data['IdProy']} no existe"}), 404

        # Validar que el departamento exista
        departamento = Departamento.query.filter_by(Numero=data["CodDepto"]).first()
        if not departamento:
            return jsonify({"error": f"El departamento con CodDepto={data['CodDepto']} no existe"}), 404

        # Validar si ya existe la asignación
        existe_asignacion = ProyectoDepto.query.filter_by(IdProy=data["IdProy"], CodDepto=data["CodDepto"]).first()
        if existe_asignacion:
            return jsonify({"error": "Esta asignación ya existe"}), 400

        # Crear la relación Proyecto-Departamento
        nuevo_proyecto_depto = ProyectoDepto(
            IdProy=data["IdProy"],
            CodDepto=data["CodDepto"],
            FechaPago=data.get("FechaPago"),
            ValorPagado=data.get("ValorPagado", 0.0)
        )

        # Guardar en la base de datos
        db.session.add(nuevo_proyecto_depto)
        db.session.commit()

        return jsonify({"message": "Proyecto asignado al departamento con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/proyectodepto/<int:IdProy>/<int:CodDepto>', methods=['GET'])
def get_proyecto_depto(IdProy, CodDepto):
    try:
        # Buscar la asignación en la base de datos
        proyecto_depto = ProyectoDepto.query.filter_by(IdProy=IdProy, CodDepto=CodDepto).first()
        if not proyecto_depto:
            return jsonify({"error": "Asignación no encontrada"}), 404

        # Construir la respuesta
        return jsonify({
            "IdProy": proyecto_depto.IdProy,
            "CodDepto": proyecto_depto.CodDepto,
            "FechaPago": proyecto_depto.FechaPago.strftime('%Y-%m-%d') if proyecto_depto.FechaPago else None,
            "ValorPagado": proyecto_depto.ValorPagado
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/proyectodepto', methods=['GET'])
def get_all_proyecto_depto():
    try:
        proyectos_departamentos = ProyectoDepto.query.all()
        if not proyectos_departamentos:
            return jsonify({"mensaje": "No se encontraron proyectos asignados a departamentos"}), 404
        
        return jsonify([{
            "IdProy": pd.IdProy,
            "CodDepto": pd.CodDepto,
            "FechaPago": pd.FechaPago.strftime('%Y-%m-%d') if pd.FechaPago else None,
            "ValorPagado": pd.ValorPagado
        } for pd in proyectos_departamentos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --- CARGOS ---
@main.route('/cargos', methods=['POST'])
def create_cargo():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Verificar que los datos requeridos están presentes
        if not data or 'NombreCargo' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Crear un nuevo cargo
        nuevo_cargo = Cargo(NombreCargo=data['NombreCargo'])

        # Agregar el cargo a la base de datos
        db.session.add(nuevo_cargo)
        db.session.commit()

        return jsonify({"message": "Cargo creado con éxito"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/cargos', methods=['GET'])
def get_cargos():
    try:
        # Consultar todos los cargos
        cargos = Cargo.query.all()

        # Formatear la respuesta como JSON
        resultado = [{"IDCargo": cargo.IDCargo, "NombreCargo": cargo.NombreCargo} for cargo in cargos]
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/cargos/<int:IDCargo>', methods=['PUT'])
def update_cargo(IDCargo):
    try:
        data = request.get_json()
        cargo = Cargo.query.filter_by(IDCargo=IDCargo).first()

        if not cargo:
            return jsonify({"error": "Cargo no encontrado"}), 404

        cargo.NombreCargo = data.get('NombreCargo', cargo.NombreCargo)
        db.session.commit()

        return jsonify({"message": "Cargo actualizado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/cargos/<int:IDCargo>', methods=['DELETE'])
def delete_cargo(IDCargo):
    try:
        cargo = Cargo.query.filter_by(IDCargo=IDCargo).first()

        if not cargo:
            return jsonify({"error": "Cargo no encontrado"}), 404

        db.session.delete(cargo)
        db.session.commit()

        return jsonify({"message": "Cargo eliminado con éxito"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- TIPOSRECLAMOS ---

@main.route('/tiposreclamo', methods=['POST'])
def create_tipo_reclamo():
    try:
        data = request.get_json()
        if not data or 'Descripcion' not in data:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        nuevo_tipo_reclamo = TipoReclamo(Descripcion=data['Descripcion'])
        db.session.add(nuevo_tipo_reclamo)
        db.session.commit()
        return jsonify({"message": "Tipo de reclamo creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/tiposreclamo', methods=['GET'])
def get_tipos_reclamo():
    try:
        tipos_reclamos = TipoReclamo.query.all()
        if not tipos_reclamos:
            return jsonify({"mensaje": "No se encontraron tipos de reclamos"}), 404

        return jsonify([{
            "IdTipoReclamo": tr.IDTipoReclamo,
            "Descripcion": tr.Descripcion
        } for tr in tipos_reclamos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/tiposreclamo/<int:IDTipoReclamo>', methods=['PUT'])
def update_tipo_reclamo(IDTipoReclamo):
    try:
        data = request.get_json()
        tipo = TipoReclamo.query.filter_by(IDTipoReclamo=IDTipoReclamo).first()
        if not tipo:
            return jsonify({"error": "Tipo de reclamo no encontrado"}), 404
        tipo.Descripcion = data.get('Descripcion', tipo.Descripcion)
        db.session.commit()
        return jsonify({"message": "Tipo de reclamo actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/tiposreclamo/<int:IDTipoReclamo>', methods=['DELETE'])
def delete_tipo_reclamo(IDTipoReclamo):
    try:
        tipo = TipoReclamo.query.filter_by(IDTipoReclamo=IDTipoReclamo).first()
        if not tipo:
            return jsonify({"error": "Tipo de reclamo no encontrado"}), 404
        db.session.delete(tipo)
        db.session.commit()
        return jsonify({"message": "Tipo de reclamo eliminado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- EDIFICIOS ---
@main.route('/edificios', methods=['POST'])
def create_edificio():
    try:
        data = request.get_json()
        required_fields = ['Nombre', 'Direccion', 'NPisos', 'ValorGastoComun', 'Estado']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        nuevo_edificio = Edificio(
            Nombre=data['Nombre'],
            Direccion=data['Direccion'],
            Inmobiliaria=data.get('Inmobiliaria'),
            Lat=data.get('Lat'),
            Log=data.get('Log'),
            Estado=data['Estado'],
            NPisos=data['NPisos'],
            ValorGastoComun=data['ValorGastoComun']
        )
        db.session.add(nuevo_edificio)
        db.session.commit()
        return jsonify({"message": "Edificio creado con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/edificios', methods=['GET'])
def get_edificios():
    try:
        edificios = Edificio.query.all()
        return jsonify([{
            "Cod": edificio.Cod,
            "Nombre": edificio.Nombre,
            "Direccion": edificio.Direccion,
            "Inmobiliaria": edificio.Inmobiliaria,
            "Lat": edificio.Lat,
            "Log": edificio.Log,
            "Estado": edificio.Estado,
            "NPisos": edificio.NPisos,
            "ValorGastoComun": edificio.ValorGastoComun
        } for edificio in edificios]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/edificios/<int:Cod>', methods=['GET'])
def get_edificio(Cod):
    try:
        edificio = Edificio.query.filter_by(Cod=Cod).first()
        if not edificio:
            return jsonify({"error": "Edificio no encontrado"}), 404
        return jsonify({
            "Cod": edificio.Cod,
            "Nombre": edificio.Nombre,
            "Direccion": edificio.Direccion,
            "Inmobiliaria": edificio.Inmobiliaria,
            "Lat": edificio.Lat,
            "Log": edificio.Log,
            "Estado": edificio.Estado,
            "NPisos": edificio.NPisos,
            "ValorGastoComun": edificio.ValorGastoComun
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/edificios/<int:Cod>', methods=['PUT'])
def update_edificio(Cod):
    try:
        data = request.get_json()
        edificio = Edificio.query.filter_by(Cod=Cod).first()
        if not edificio:
            return jsonify({"error": "Edificio no encontrado"}), 404
        for key, value in data.items():
            if hasattr(edificio, key):
                setattr(edificio, key, value)
        db.session.commit()
        return jsonify({"message": "Edificio actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route('/edificios/<int:Cod>', methods=['DELETE'])
def delete_edificio(Cod):
    try:
        edificio = Edificio.query.filter_by(Cod=Cod).first()
        if not edificio:
            return jsonify({"error": "Edificio no encontrado"}), 404
        db.session.delete(edificio)
        db.session.commit()
        return jsonify({"message": "Edificio eliminado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- FUNCIONES PARA LISTAR ----
@main.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Acceso.query.all()
    return jsonify([{
        "username": usuario.username,
        "Rut": usuario.Rut,
        "Tipo": usuario.Tipo,
        "fechaCreacion": usuario.fechaCreacion.strftime('%Y-%m-%d %H:%M:%S'),
        "fechaUltimoAcceso": usuario.fechaUltimoAcceso.strftime('%Y-%m-%d %H:%M:%S') if usuario.fechaUltimoAcceso else "Nunca"
    } for usuario in usuarios]), 200

@main.route('/departamentos', methods=['GET'])
def listar_departamentos():
    try:
        # Obtén el parámetro opcional 'arrendado'
        arrendado = request.args.get('arrendado')

        # Si el parámetro no está presente, devuelve todos los departamentos
        if arrendado is None:
            departamentos = Departamento.query.all()
        else:
            # Si el parámetro está presente, valida y filtra
            if arrendado.lower() not in ['true', 'false']:
                return jsonify({"error": "El parámetro 'arrendado' debe ser 'true' o 'false'"}), 400
            arrendado = arrendado.lower() == 'true'
            departamentos = Departamento.query.filter_by(Arrendado=arrendado).all()

        # Verifica si hay departamentos en la base de datos
        if not departamentos:
            return jsonify({"mensaje": "No se encontraron departamentos"}), 404

        # Devuelve los departamentos en formato JSON
        return jsonify([{
            "Numero": depto.Numero,
            "Piso": depto.Piso,
            "Arrendado": depto.Arrendado,
            "Estado": depto.Estado,
            "Observacion": depto.Observacion
        } for depto in departamentos]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@main.route('/asociar_departamento', methods=['POST'])
def asociar_departamento():
    data = request.get_json()

    # Validar datos requeridos
    required_fields = ["RutArre", "Numero"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

    # Verificar que el usuario exista y sea arrendatario
    usuario = Acceso.query.filter_by(Rut=data["RutArre"], Tipo="arrendatario").first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado o no es un arrendatario"}), 404

    # Verificar que el departamento exista
    departamento = Departamento.query.filter_by(Numero=data["Numero"]).first()
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404

    # Asociar usuario con el departamento
    departamento.RutArre = usuario.Rut
    departamento.Arrendado = True
    db.session.commit()

    return jsonify({"message": "Departamento asociado con éxito"}), 200

@main.route('/editar_departamento/<int:numero>', methods=['PUT'])
def editar_departamento(numero):
    data = request.get_json()

    # Verificar que el departamento exista
    departamento = Departamento.query.filter_by(Numero=numero).first()
    if not departamento:
        return jsonify({"error": "Departamento no encontrado"}), 404

    # Actualizar los campos editables
    campos_editables = ["Piso", "Estado", "FechaIniC", "FechaFinC", "Observacion", "NumHab", "NumBaños"]
    for key, value in data.items():
        if key in campos_editables:
            setattr(departamento, key, value)

    db.session.commit()
    return jsonify({"message": "Departamento actualizado con éxito"}), 200


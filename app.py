#importacion de flask
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session

#inicializar el framework
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#conexion a la BD
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='elgaraje'

#token de seguridad
app.secret_key='mysecretkey'
mysql=MySQL(app)

class user():
    def __init__(self,idmed, nombre, rol)->None:
        self.idmed = idmed
        self.nombre = nombre
        self.rol = rol

class user1():
    def __init__(self,idmed, nombre, rol)->None:
        self.idmed = idmed
        self.nombre = nombre
        self.rol = rol

#RUTAS GENERALES
@app.route('/')
def log():
    return render_template('login.html')

#LOGIN USUARIO
@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        usuario = request.form['txtuser']
        pas = request.form['txtpassword']
        cursor = mysql.connection.cursor()
        cursor.execute('select * from registrouser where status =1 and nombreUser = %s and password = %s', (usuario, pas,))
        mysql.connection.commit()
        account = cursor.fetchall()
        if account:
            User = user(account[0][0],account[0][1],account[0][3])
            session['id'] = account[0][0]
            session['usuario'] = account[0][1]
            session['pas'] = account[0][3]
            print(usuario)
            if(account[0][5] == 2):
                return render_template('menuAdmin.html')
            else:
                return render_template('index.html')                       
        else:
            flash('Datos incorrectos')
            return render_template('login.html')
        
        
@app.route('/index/<string:id>')
def index(id):
    if session['id'] == None:
        return render_template('login.html')
    else:
        return render_template('index.html', user = user)  

@app.route('/logout')
def logout():
    session['id']=None
    return render_template('login.html')  
 

@app.route('/membresias/<string:id>')
def membresias(id):
    return render_template('membresia.html', user = user)

@app.route('/establecimientos/<string:id>')
def establecimientos(id):
    return render_template('establecimiento.html', user = user)

@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    #Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'id' in session and ruta != "/" and ruta != "/login"  and not ruta.startswith("/static"):
     return redirect(url_for('/'))

#--------------------------------------------

#RUTAS DE USUARIO
@app.route('/registrarte')
def registrarte():
        return render_template('CrearUsu.html')  

@app.route('/crearusu', methods=['POST'])
def crearusu():
    if request.method=='POST':
        nombre = request.form['txtnombre']
        email = request.form['txtemail']
        password = request.form['txtpass']
        confpass = request.form['txtconfpass']

        if password == confpass:

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO registrouser(nombreUser,email,password,confir_password,rol,status) VALUES(%s,%s,%s,%s,1,1)',(nombre,email,password,confpass))
            mysql.connection.commit()
            flash('¡Ingresa ahora!')            
            return redirect(url_for('log'))
        else:
            flash('Contraseñas no coinciden')
            return render_template('CrearUsu.html')


#RUTAS VEHICULOS
@app.route('/formregistro/<string:id>')
def formVehiculos(id):
    return render_template('registrar_Vehiculos.html', user = user)  

@app.route('/registrarVehiculo/<string:id>', methods=['POST'])
def registrar(id):
    if request.method == 'POST':
        vnombre = request.form['txtNombre']
        vapellidos = request.form['txtApellidos']
        vmodelo = request.form['txtModelo']
        vnumlic = request.form['txtNumlic']
        vtopcion = request.form['txtTopcion']
        veopcion = request.form['txtEopcion']
        vnumplacas = request.form['txtNumplacas']
        vcolor = request.form['txtColor']
        vcaract = request.form['txtCaract']
    
        idusu = id
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO registrarvehiculo(idusuario,nombre,apellidos,modeloAuto,numLicencia,tipoAuto,establecimiento,numeroPLacas,colorAuto,caracteristicas,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)',(idusu,vnombre,vapellidos,vmodelo,vnumlic,vtopcion,veopcion,vnumplacas,vcolor,vcaract))
        mysql.connection.commit()
    
        flash('Se ha registrado el vehiculo') 
        return render_template('registrar_Vehiculos.html', user = user)

@app.route('/editar/<string:id>')
def editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from registrarvehiculo where id_vehiculo = %s',[id,])
    consulta = cursor.fetchall()
    
    return  render_template('editar_Vehiculos.html', vehiculos = consulta[0])

@app.route('/update', methods=['POST'])
def update():
 if request.method == 'POST':
    vid = request.form['txtId']
    vnombre = request.form['txtNombre']
    vapellidos = request.form['txtApellidos']
    vmodelo = request.form['txtModelo']
    vnumlic = request.form['txtNumlic']
    vnombre = request.form['txtNombre']
    vtopcion = request.form['txtTopcion']
    veopcion = request.form['txtEopcion']
    vnumplacas = request.form['txtNumplacas']
    vcolor = request.form['txtColor']
    vcaract = request.form['txtCaract']

    cursor = mysql.connection.cursor()
    cursor.execute('update registrarvehiculo set nombre = %s,apellidos = %s,modeloAuto = %s,numLicencia = %s,tipoAuto = %s,establecimiento = %s,numeroPLacas = %s,colorAuto = %s,caracteristicas = %s where id_vehiculo = %s', (vnombre,vapellidos,vmodelo,vnumlic,vtopcion,veopcion,vnumplacas,vcolor,vcaract,vid))
    mysql.connection.commit()
    
    flash('Vehiculo actualizado en la base de datos') 
    return redirect(url_for('consultaVehiculos', id = id))   

@app.route('/eliminar/<string:id>')
def eliminar(id):   
    cursor = mysql.connection.cursor()
    cursor.execute('delete from registrarvehiculo where id_vehiculo={0}'.format(id))
    mysql.connection.commit()

    flash('Vehiculo elminado')
    return redirect(url_for('consultaVehiculos', id = id))

#---------------------------RUTAS ADMINISTRADOR----------------------------

@app.route('/inicio/<string:id>')
def inicio(id):
    return render_template('menuAdmin.html')

#CONSULTA VEHICULOS
@app.route('/consultaVehiculos/<string:id>', methods=['GET','POST'])
def consultaVehiculos(id):
    cursor = mysql.connection.cursor()
    if request.method == "POST" and 'txtcate' in request.form:
            cursor.execute("SELECT * FROM registrarvehiculo WHERE status = 1 and nombre and apellidos like '%" + request.form['txtcate'] + "%'")
    else: 
        cursor.execute('select * from registrarvehiculo where status=1')
    consulta = cursor.fetchall()
    return render_template('consultar_Vehiculos.html',vehiculos=consulta) 

#CONSULTA USUARIO
@app.route('/consultausu/<string:id>', methods=['GET','POST'])
def consultausu(id):
    cursor = mysql.connection.cursor()
    if request.method == "POST" and 'txtcategoria' in request.form:
            cursor.execute("SELECT * FROM registrouser WHERE status = 1 and nombreUser like '%" + request.form['txtcategoria'] + "%'")
    else:        
        cursor.execute('select * from registrouser where status=1')
    consulta = cursor.fetchall()
    return render_template('consultaUsu.html',usuarios = consulta)    

@app.route('/editarusu/<string:id>')
def editarusu(id):
    cursor = mysql.connection.cursor()
    cursor.execute('Select * from registrouser where id_user=%s',[id])
    consulta = cursor.fetchall()
    return render_template('editarUsu.html', usuarios = consulta[0])

@app.route('/actualizarusu/<string:id>', methods = ['POST'])
def actualizarusu(id):
    if request.method=='POST':
        nombre = request.form['txtnombre']
        email = request.form['txtemail']
        password = request.form['txtpass']
        confpass = request.form['txtconfpass']
        if password == confpass:
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE registrouser set nombreUser = %s, email = %s, password = %s, confir_password=%s where id_user=%s',(nombre,email,password,confpass,id))
            mysql.connection.commit()
            flash('Usuario Editado en la Base de Datos')
            return redirect(url_for('consultausu', id = id))
        else: 
            flash('Contraseñas no coinciden')
            return render_template('editarUsu.html')

@app.route('/elimiarusu/<string:id>')
def elimiarusu(id):
    cursor = mysql.connection.cursor()
    cursor.execute('update registrouser set status=0 where id_user={0}'.format(id))
    mysql.connection.commit()
    flash('Usuario Eliminado de la base de Datos')
    return redirect(url_for('consultausu', id = id))

#Registrar Admin
@app.route('/registrar')
def registrarAdmin():
        return render_template('CrearUsuAdmin.html')  

@app.route('/crearusuAdmin', methods=['POST'])
def crearusuAdmin():
    if request.method=='POST':
        nombre = request.form['txtnombre']
        email = request.form['txtemail']
        password = request.form['txtpass']
        confpass = request.form['txtconfpass']

        if password == confpass:

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO registrouser(nombreUser,email,password,confir_password,rol,status) VALUES(%s,%s,%s,%s,2,1)',(nombre,email,password,confpass))
            mysql.connection.commit()
            flash('Usuario registrado')
            return render_template('CrearUsuAdmin.html')
        else:
            flash('Contraseñas no coinciden')
            return render_template('CrearUsuAdmin.html')

#-----------------------------------------------------------------------


@app.route('/actualizarMicuenta/<string:id>', methods = ['POST'])
def actualizarMicuenta(id):
    if request.method=='POST':
        mi1 = request.form['Miemail']
        mi2 = request.form['Miname']
        mi3 = request.form['Mipass']
        mi4 = request.form['Mipass2']
        if mi3 == mi4:
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE registrouser set nombreUser = %s, email = %s, password = %s, confir_password=%s where id_user=%s',(mi1,mi2,mi3,mi4,id))
            mysql.connection.commit()
            flash('Datos editados correctamente')
            return redirect(url_for('consultaMicuenta', id = id))
        else: 
            flash('Contraseñas no coinciden')
            return redirect(url_for('consultaMicuenta', id = id))

@app.route('/consultaMicuenta/<string:id>')
def consultaMicuenta(id):
        cursor = mysql.connection.cursor()
        
        cursor.execute('select * from registrarvehiculo where status=1 and idusuario = %s', [id,])
        consulta = cursor.fetchall()
        
        cursor.execute('Select * from registrouser where id_user=%s',[id])
        consulta1 = cursor.fetchall()
        
        return render_template('micuentaUsuario.html',vehi=consulta, usu = consulta1[0])

#----------------------------------------------------------------------
#RUTA MEMBRESIA
@app.route('/insertMem/<string:id>/<string:memb>')
def insertMem(id,memb):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from registrouser where id_user=%s',[id,])
    usuariom = cursor.fetchone()
    print(usuariom[6])

    if usuariom[6] == None:
        cursor.execute('call membresia(%s,%s)',(memb,id))
        mysql.connection.commit()
        flash('Se ha agregado la membresia')
        return redirect(url_for('membresias',id=id))
    else:        
        flash('Ya cuentas con una membresia')
        return redirect(url_for('membresias',id=id))




#levantamos el server flask
if __name__=='__main__':
    app.run(port=3000, debug= True)
    

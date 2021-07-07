from django.contrib import messages
from django.shortcuts import redirect, render
from app.models import User
import bcrypt

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")
    


def index(request):

    if 'usuario' not in request.session:
        return redirect("/login")

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


def pancho(request):
    print(request.session['usuario'])

    if 'usuario' not in request.session:
        return redirect("/login")

    if request.session['usuario']['rol'] != "ADMIN":
        messages.error(request, "El usuaro no es administrador, es de tipo :"+ request.session['usuario']['rol'])
        return redirect("/")


    return render(request, 'pancho.html')

def horas(request):

    if 'usuario' not in request.session:
        return redirect("/login")

    if request.session['usuario']['rol'] != "ADMIN":
        messages.error(request, "El usuaro no es administrador, es de tipo :"+ request.session['usuario']['rol'])
        return redirect("/")


    return render(request, 'horas.html')


def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                usuario = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    "rol": log_user.rol
                }

                request.session['usuario'] = usuario
                messages.success(request, "Logeado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  malas.")
        else:
            messages.error(request, "Email o password malas.")



        return redirect("/login")
    else:

        if 'usuario'  in request.session:
            messages.error(request, "Usted ya está logeado.")
            return redirect("/")

        return render(request, 'login.html')

def registro(request):
    if request.method == "POST":
        print(request.POST)

        errors = User.objects.validador_basico(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['registro_nombre'] =  request.POST['nombre']
            request.session['registro_apellido'] =  request.POST['apellido']
            request.session['registro_email'] =  request.POST['email']

        else:
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                 firstname = request.POST['nombre'],
                lastname=request.POST['apellido'],
                email=request.POST['email'],
                password=password_encryp
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

        return redirect("/registro")
    else:
        return render(request, 'registro.html')



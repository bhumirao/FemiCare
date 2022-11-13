from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template , Context

import pyrebase
# Create your views here.

config = {
    "apiKey": "AIzaSyCz4_TIzBI2JTyAgeOvwAmabBe8cOzo6uk",
    "authDomain": "femicare-1bd20.firebaseapp.com",
    "databaseURL":"https://femicare-1bd20-default-rtdb.firebaseio.com/",
    "projectId": "femicare-1bd20",
    "storageBucket": "femicare-1bd20.appspot.com",
    "messagingSenderId": "814003542467",
    "appId": "1:814003542467:web:6a7447906a9d822adb0576",
    
}
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()


def signIn(request):
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user= authe.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "login.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "home.html", {"email": email})


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "login.html")


def signUp(request):
    return render(request, "registration.html")


def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email, passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
    except:
        return render(request, "registration.html")
    return render(request, "login.html")

# RESET PASSWORD 

def reset(request):
    return render(request, "reset.html")
 
def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message  = "A email to reset password is successfully sent"
        return render(request, "reset.html", {"msg":message})
    except:
        message  = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "reset.html", {"msg":message})
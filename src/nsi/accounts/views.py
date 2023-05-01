import random
import string

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app-index')
    elif request.user.is_authenticated:
        return redirect('app-index')

    return render(request, 'accounts/login.html')


def logout_page(request):
    logout(request)
    return redirect('index')


def create_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            User.objects.create_user(username=email,
                                     email=email,
                                     password=password,
                                     first_name=name)
        except IntegrityError:
            return render(request, 'accounts/new.html')

        user = authenticate(username=email, password=password)
        login(request, user)

        send_mail(subject='Bienvenue sur BlinkURL',
                  message='',
                  html_message=f"<h2>Bienvenue sur BlinkURL !</h2>"
                               f"<p>Bienvenue {user.first_name},</p><p>Le monde est rempli "
                               f"de surprises et aujourd'hui, vous venez de découvrir l'une d'entre elles : notre "
                               f"site web ! Nous sommes ravis de vous accueillir dans notre communauté et espérons "
                               f"que vous y trouverez tout ce dont vous avez besoin pour raccourcir vos "
                               f"liens.</p><p>Mais avant de commencer, il est important de lire et de respecter nos "
                               f"CGU, qui garantissent un fonctionnement optimal et juste de notre service. Nous "
                               f"travaillons dur pour rendre l'expérience utilisateur la plus agréable possible, "
                               f"et c'est en respectant ces règles que nous pourrons continuer à le faire.</p><p>Nous "
                               f"vous souhaitons une excellente utilisation de notre site web et restons à votre "
                               f"disposition si vous avez la moindre question ou suggestion.</p><p>Bien à vous,"
                               f"</p><p>L'équipe de BlinkURL</p>",
                  from_email='notifications@pazu444.fr',
                  recipient_list=(user.email,))

        return redirect('app-index')

    elif request.user.is_authenticated:
        return redirect('app-index')

    return render(request, 'accounts/new.html')


def account_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')

            user = User.objects.get(username=request.user.username)
            user.first_name = name

            if len(User.objects.all().filter(username=email)) == 0:
                user.username, user.email = email, email

            user.save()

            return redirect('app-index')

        return render(request, 'accounts/account.html')
    else:
        return redirect('login')


def delete_page(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user.delete()

        send_mail(subject='À bientôt sur BlinkURL !',
                  message='',
                  html_message=f"<h2>BlinkURL</h2><p>Bonjour {user.first_name},</p><p>Nous avons bien reçu votre "
                               f"demande de suppression de votre compte BlinkURL et nous sommes navrés de vous voir "
                               f"partir. Nous espérons que votre expérience avec notre service de raccourcissement "
                               f"d'URL a été à la hauteur de vos attentes.</p><p>Nous souhaitons vous remercier pour "
                               f"la confiance que vous nous avez accordée en utilisant notre service. Si vous changez "
                               f"d'avis et que vous souhaitez recréer un compte à l'avenir, sachez que nous serons "
                               f"heureux de vous accueillir à nouveau.</p><p>Sachez également que si vous avez des "
                               f"commentaires ou des suggestions sur notre service, n'hésitez pas à nous les faire "
                               f"savoir. Nous sommes toujours à la recherche de moyens pour améliorer l'expérience de "
                               f"nos utilisateurs.</p><p>Nous vous souhaitons bonne continuation dans vos futurs "
                               f"projets et nous espérons que vous garderez un bon souvenir de votre passage sur "
                               f"BlinkURL.</p><p>Bien à vous,</p><p>L'équipe de BlinkURL</p>",
                  from_email='notifications@pazu444.fr',
                  recipient_list=(user.email,))

        return redirect('index')
    else:
        return redirect('login')


def new_password_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('password')
            new_password = request.POST.get('new-password')

            if password == new_password and len(password) >= 8:
                user = User.objects.get(username=request.user.username)
                user.set_password(password)
                user.save()

                send_mail(subject='Changement de mot de passe confirmé !',
                          message='',
                          html_message=f"<h2>BlinkURL</h2>"
                                       f"<p>Bonjour {user.first_name},</p><p>Nous venons de recevoir votre demande de "
                                       f"changement de mot de passe et nous sommes ravis de vous confirmer que la "
                                       f"modification a bien été prise en compte. Votre sécurité en ligne est une de "
                                       f"nos priorités et nous sommes heureux que vous ayez pris l'initiative de "
                                       f"mettre à jour votre mot de passe.</p><p>Nous vous rappelons qu'il est "
                                       f"important de choisir un mot de passe sécurisé et de ne jamais le communiquer "
                                       f"à qui que ce soit. Nous vous invitons également à consulter régulièrement "
                                       f"nos CGU pour vous tenir informé des dernières mises à jour et ainsi garantir "
                                       f"une utilisation optimale de nos services.</p><p>Nous restons à votre "
                                       f"disposition pour toute question ou préoccupation concernant votre "
                                       f"compte.</p><p>Bien à vous,</p><p>L'équipe de BlinkURL</p>",
                          from_email='notifications@pazu444.fr',
                          recipient_list=(user.email,))

                return redirect('login')

        return render(request, 'accounts/new_password.html')
    else:
        return redirect('login')


def forgot_password_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.all().filter(username=email)

        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        if len(user) == 1:
            user = user[0]
            print(user)
            user.set_password(new_password)
            user.save()

            send_mail(subject='Réinitialisation de votre mot de passe !',
                      message='',
                      html_message=f"<h2>BlinkURL</h2><p>Bonjour, {user.first_name}</p><p>Nous avons récemment reçu "
                                   f"une demande de réinitialisation de votre mot de passe pour BlinkURL. Nous avons "
                                   f"donc réinitialisé votre mot de passe et vous envoyons un nouveau mot de passe "
                                   f"temporaire.</p><p>Votre nouveau mot de passe temporaire est: <span "
                                   f"style='font-weight=bold;'>{new_password}</span></p><p>Nous vous recommandons de "
                                   f"changer votre mot de passe temporaire dès que possible pour des raisons de "
                                   f"sécurité.</p><p>Si vous avez des questions ou des préoccupations, n'hésitez pas "
                                   f"à nous contacter.</p><p>Bien à vous,</p><p>L'équipe de BlinkURL</p>",
                      from_email='notifications@pazu444.fr',
                      recipient_list=(user.email,))

        return redirect('login')
    return render(request, 'accounts/forgot_password.html')

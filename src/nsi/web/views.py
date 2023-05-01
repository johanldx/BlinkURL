from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from app.models import Url


def index_page(request):
    return render(request, 'web/index.html')


def sitemap_page(request):
    return render(request, 'web/sitemap.xml', content_type="application/xhtml+xml")

def contact_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(subject='Nouveau message de contact !',
                  message='',
                  html_message=f"<p>Nouveau message de : {email}</p><p>Message : {message}</p>",
                  from_email='notifications@pazu444.fr',
                  recipient_list=('blinkurl@pazu444.fr',))

    return render(request, 'web/contact.html')


def cgu_page(request):
    return render(request, 'web/cgu.html')


def a_propos_page(request):
    return render(request, 'web/a_propos.html')


def url_page(request, key):
    url = Url.objects.all().filter(key=key)
    if len(url) == 1:
        url = url[0]
        redirect_url = url.url

        try:
            validate = URLValidator()
            validate(redirect_url)
            url.statistics += 1
            url.save()

            if url.statistics == 100 or url.statistics == 1000:
                send_mail(subject=f"Bravo votre lien à atteint {url.statistics} cliques !",
                          message='',
                          html_message=f"<p>Cher utilisateur,</p><p>Nous sommes ravis de vous annoncer que votre lien vers {url.url} a été cliqué plus de {url.statistics} fois ! Nous sommes vraiment fiers de voir que notre service de raccourcissement d'URL a aidé à promouvoir votre contenu.</p><p>Nous espérons que cela vous a été bénéfique et nous vous encourageons à continuer à partager vos liens. Avec notre service, vous pouvez atteindre encore plus de personnes en toute simplicité.</p><p>Nous vous remercions de votre confiance et nous espérons que notre service continuera à vous être utile. N'hésitez pas à nous contacter si vous avez des questions ou des commentaires.</p><p>Bien à vous,</p><p>L'équipe de BlinkURL.</p>",
                          from_email='notifications@pazu444.fr',
                          recipient_list=(url.user.email,))

            return redirect(redirect_url)
        except ValidationError:
            return render(request, 'web/error.html', {'title': 'Lien incorrect !', 'message': "Le lien renseigné par l'auteur ne correspond pas à un site web."})

    else:
        return redirect('index')


def page_not_found(request, exception):
    return render(request, 'web/404.html', status=404)

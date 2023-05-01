import string
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.models import Url


def app_page(request):
    if request.user.is_authenticated:
        user_urls = []
        edit_url = None

        for url in Url.objects.all().filter(user=request.user):
            user_urls.append(url)

        if 'edit-url' in request.session:
            if len(Url.objects.all().filter(id=request.session['edit-url'])) != 0:
                edit_url = Url.objects.get(id=request.session['edit-url'])
            else:
                del request.session['edit-url']
        elif len(user_urls) != 0:
            edit_url = user_urls[0]
        else:
            edit_url = None

        if request.method == 'POST':
            name = request.POST.get('name')
            link = request.POST.get('link')

            edit_url.name = name
            edit_url.url = link

            edit_url.save()

        return render(request, 'app/panel.html', {'urls': user_urls, 'edit_url': edit_url})
    else:
        return redirect('login')


def edit_page(request, url):
    if request.user.is_authenticated:
        url = Url.objects.get(id=url)
        if url is not None and url.user == request.user:
            request.session['edit-url'] = url.id

    return redirect('app-index')


def delete_page(request, url):
    if request.user.is_authenticated:
        url = Url.objects.get(id=url)
        if url is not None and url.user == request.user:
            url.delete()

    return redirect('app-index')


def add_page(request):
    if request.user.is_authenticated:
        new_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

        all_keys = []
        for key in Url.objects.all():
            all_keys.append(key)

        while True:
            if new_key in all_keys:
                new_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
            else:
                break

        Url.objects.create(name='Nouveau lien',
                           url='',
                           key=new_key,
                           user=request.user)

    return redirect('app-index')

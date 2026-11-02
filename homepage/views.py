from django.http import HttpResponse
from django.shortcuts import render

def page(title, content):
    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    </head>
    <body>
        <nav class="nav p-3 bg-light mb-4">
            <a class="nav-link" href="/">Главная</a>
            <a class="nav-link" href="/actors/">Актеры</a>
        </nav>
        <main class="container">{content}</main>
    </body>
    </html>"""


def index(request):
    return render(request, "homepage/index.html")

def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
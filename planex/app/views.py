from django.http import HttpResponse


def robots(request):
    content = "\n".join(["User-Agent: *", "Disallow: /admin/", "Disallow: /wagtail/", "Disallow: /test/"])
    return HttpResponse(content, content_type="text/plain")

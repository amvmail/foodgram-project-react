from django.shortcuts import render


def bad_request(request, exception=None):
    return render(request,
                  'error/400.html',
                  status=400)


def permissions_denied(request, exception=None):
    context = {'path': request.path}
    return render(request,
                  'error/403.html',
                  context,
                  status=403)


def page_not_found(request, exception=None):
    context = {'path': request.path}
    return render(request,
                  'error/404.html',
                  context,
                  status=404)


def server_error(request):
    return render(request,
                  'error/500.html',
                  status=500)

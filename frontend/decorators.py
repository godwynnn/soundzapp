from django.http import HttpResponse
from django.shortcuts import redirect, render

def authenticated_user(view_func):
    def verify_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request,*args,**kwargs)
    return verify_func
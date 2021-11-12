from django.db.models import query
from django.forms.utils import from_current_timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .decorators import *


import stripe
import os
# Create your views here.

@authenticated_user
def Landing_Page(request):
    # print('SESSIONS: ', request.session )
    return render(request,'sound/landing.html')

def Index_Page(request):
    return render(request,'sound/index.html')

def Shop_Page(request):
    paginate=Paginator(Beat.objects.all(),8)
    p=request.GET.get('page')
    beats = paginate.get_page(p)

    context={'beats':beats}
    return render(request,'sound/shop.html',context)

def Create_Page(request):
    form=BeatForm(request.POST or None,request.FILES)
    if request.method=='POST':
        if form.is_valid():
            obj=form.save(commit=False)
            obj.slug=slugify(obj.title+'-'+obj.description[:11])
            obj.save()
            form=BeatForm()
            return redirect('shop')
    template='sound/create.html'
    context ={'form': form}
    return render(request,template,context)

def Detail_Page(request,slug):
    beat=Beat.objects.get(slug=slug)
    carted=False
    
    try:
        customer=request.user.customer
        order_qs=Order.objects.filter(customer=customer,ordered=False)
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        
        order_qs=Order.objects.filter(customer=customer,ordered=False)
        
    if order_qs.exists():
        order=order_qs[0]
        if order.beats.filter(beat__slug=beat.slug).exists():
            carted=True
    
    bought=OrderBeat.objects.filter(is_ordered=True,beat__slug=beat.slug,customer=customer)
    purchased=False
    if bought.exists():
        purchased=True
    
    context={'beat':beat,'carted':carted,'purchased':purchased}
    return render(request,'sound/detail.html',context)
            

def Update_Page(request):
    pass

def Delete_Page(request):
    pass


def Signup_Page(request):
    form=CreateUserForm(request.POST or None)
    if request.method== 'POST':
        if form.is_valid():
            user=form.save()
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']

            Customer.objects.create(
                user=user,
                first_name=first_name,
                second_name=last_name,
                email=email,  
            )


        form=CreateUserForm()
        return redirect('login')


    template='sound/signup.html'
    context={'form':form}
    return render (request,template,context)
        

def Login_Page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if 'next' in request.POST:
                return redirect (request.POST.get('next'))
            else:
                return redirect('index')
        else:
            messages.info(request,'Username Or Password is Incorrect')
    return render(request,'sound/login.html')

def Logout_Page(request):
    logout(request)
    return redirect('landing')

def Search_Page(request):
    q=request.POST.get('q' or None)
    query=Beat.objects.filter(
        Q(title__icontains=q)|
        Q(genre__icontains=q)|
        Q(description__icontains=q)|
        Q(slug__icontains=q)
    )
    context={'query':query}
    return render(request,'sound/shop.html',context)



def Add_to_cart(request,slug): 
    if request.method=='POST':
        beat=get_object_or_404(Beat,slug=slug)
        if request.user.is_authenticated:
            customer=request.user.customer
            beat_order,created=OrderBeat.objects.get_or_create(
                customer=customer,
                beat=beat,
                session=request.session.session_key
            )
            order_qs=Order.objects.filter(customer=customer,ordered=False)
                
        if request.user.is_anonymous:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

            beat_order,created=OrderBeat.objects.get_or_create(
                    customer=customer,
                    beat=beat,
                    session=request.session.session_key
                )
            order_qs=Order.objects.filter(customer=customer,ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            if order.beats.filter(beat__slug=beat.slug).exists():
                messages.info(request,'your already have this beat')
                return HttpResponseRedirect(reverse('detail',kwargs={'slug':beat.slug}))
            else:
                order.beats.add(beat_order)
                return HttpResponseRedirect(reverse('detail',kwargs={'slug':beat.slug}))
        else:
            order=Order.objects.create(customer=customer,ordered=False,session=request.session.session_key)
            order.beats.add(beat_order)
            return HttpResponseRedirect(reverse('detail',kwargs={'slug':beat.slug}))
            # else:
            #     order=Order.objects.create(customer=customer,ordered=False)
            #     order.beats.add(beat_order)
            #     return HttpResponseRedirect(reverse('detail',kwargs={'slug':beat.slug}))



def Remove_from_cart(request,slug):
    
    beat=get_object_or_404(Beat,slug=slug)
    try:
        customer=request.user.customer
        
        
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device) 
        
    order_qs=Order.objects.filter(customer=customer,ordered=False)                   
    if order_qs.exists():
        order=order_qs[0]
        if order.beats.filter(beat__slug=beat.slug).exists():
            beat_order=OrderBeat.objects.filter(customer=customer,
            is_ordered=False,
            beat=beat
            )[0]

            order.beats.remove(beat_order)
            beat_order.delete()
            messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(reverse('cart'))

            
        else:
            messages.info(request, "This beat was not in your cart")
            return HttpResponseRedirect(reverse('cart',))
    else:
        messages.info(request, "you don't have any active order")
        return HttpResponseRedirect(reverse('cart'))


def CartFlow(request):


    try:
        customer=request.user.customer
        
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        # orders= Order.objects.filter(customer__device=customer,ordered=False)[0]


    beats_order=OrderBeat.objects.filter(customer=customer,is_ordered=False,)
    orders= Order.objects.filter(customer=customer,ordered=False).first()
    total=orders.get_total_price()

    carted=False
    for beat in beats_order:
        if beat in orders.beats.all():
            carted=True
        else:
            carted=False
    else:
        pass
        
    

    context={'orders':orders,'total':total,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            'beats_order':beats_order,'carted':carted}

    return render(request,'sound/cart.html',context)


@login_required(login_url='login')
def Create_Checkout_session(request,session):
  

    customer=request.user.customer
    orders= Order.objects.get(session=session,ordered=False)
    # beat_order=OrderBeat.objects.get_or_create(customer=customer,is_ordered=False)

    # for beat in beat_order:
    #     if beat in orders.beats.all():
    #         pass
    #     else:
    #         orders.beats.add(beat)
 
    for order in orders.beats.all():
        beat_name=order.beat.title
        
    total=orders.get_total_price()
    DOMAIN='soundz-demo.herokuapp.com/'
    # DOMAIN='http://127.0.0.1:8000/soundz/'
    stripe.api_key=settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': 'beat_name',
            },
            'unit_amount': total*100,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url=DOMAIN+'success',
        cancel_url=DOMAIN+'cancel',
    )

    return redirect(session.url)


def Success_Page(request):



    beats_order=OrderBeat.objects.filter(customer=request.user.customer,is_ordered=False)
    orders=Order.objects.filter(customer=request.user.customer,ordered=False,)[0]

    for beat_order in beats_order:
        if beat_order in orders.beats.all():
            beat_order.is_ordered=True
            beat_order.save()
            orders.ordered=True
            orders.save()
    try:
        beat_order=OrderBeat.objects.filter(customer=request.user.customer,is_ordered=False)
        orders=Order.objects.filter(customer=request.user.customer,ordered=False,)[0]
        for beat_order in orders.beats.all():
            orders.beats.remove(beat_order)
    except Exception as e:
        print(e)
    
    
    return render(request,"sound/success.html")



def Cancel_Page(request):
    return render(request,'sound/cancel.html')



def User_Dashboard(request):
    customer=request.user.customer
    beat_order=OrderBeat.objects.filter(customer=customer,is_ordered=True)
    context={'beat_order':beat_order}
    return render(request,'sound/user_dashboard.html', context)
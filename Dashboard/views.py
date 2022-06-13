from django.http import HttpResponse
from django.shortcuts import render, redirect
from API.FirebaseConsole import get_all_users, create_user, add_item, get_all_products, get_all_invoices, get_single_invoice
from django.contrib import messages


def home(request):
    try:
        if request.session['username']:
            print('ALL OK')
        else:
            return redirect('User:login')
    except:
        return redirect('User:login')
    return render(request, 'dashboard/dashboard.html')

def check_login(request):
    try:
        if request.session['username']:
            print('ALL OK')
        else:
            return redirect('Dashboard:login')
    except:
        return redirect('Dashboard:login')

def all_user(request):
    user_list = get_all_users()
    context = {
        'user_list': user_list
    }

    return render(request, 'user/view_user.html', context=context)

def add_user(request):

    if request.method == 'POST':
        try:
            Username = request.POST.get('Username')
            Password = request.POST.get('Password')

            fb = create_user(Username, Password)
            if fb:
                messages.add_message(request, messages.SUCCESS, 'User Created')
            else:
                messages.add_message(request, messages.SUCCESS, 'User Exist')
        except:
            messages.add_message(request, messages.ERROR, 'Input Error')


    context = {
    }

    return render(request, 'user/add_user.html', context=context)

def create_item(request):

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            cost = float(request.POST.get('cost'))

            add_item(name, cost)

            messages.add_message(request, messages.SUCCESS, 'Product Added')

        except:
            messages.add_message(request, messages.ERROR, 'Input Error')


    context = {
    }

    return render(request, 'clinic/add_item.html', context=context)

def all_products_view(request):
    product_list = get_all_products()
    context = {
        'product_list': product_list
    }

    return render(request, 'clinic/view_items.html', context=context)

def all_invoice_list(request):
    invoice_list = get_all_invoices()

    context = {
        'invoice_list':invoice_list
    }

    return render(request, 'Clinic/all_invoices.html', context=context)

def single_invoice(request, id):
    invoice = get_single_invoice(id)

    if not invoice == None:

        context = {
            'invoice': invoice
        }
        print(invoice)
        return render(request, 'Clinic/invoice.html', context=context)
    else:
        return render(request, 'Clinic/not_found.html')

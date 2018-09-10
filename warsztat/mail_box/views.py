from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from mail_box.models import *


class NewContact(View):
    def get(self, request):
        return render(request, "new_contact.html")

    def post(self, request):
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        description = request.POST.get('desc')
        new_contact = Person.objects.create(name=name, lastname=lastname, description=description)
        return HttpResponseRedirect(f'show/{new_contact.id}')


class ShowContact(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        return render(request, "show_contact.html", locals())


class ModifyContact(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        return render(request, "modify_contact.html", locals())

    def post(self, request, id):
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        description = request.POST.get('desc')
        edit_contact = Person.objects.get(pk=id)
        edit_contact.name = name
        edit_contact.lastname = lastname
        edit_contact.description = description
        edit_contact.save()
        return HttpResponseRedirect(f'/show/{edit_contact.id}')


class DeleteContact(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        contact.delete()
        return HttpResponseRedirect('/')


class ShowAll(View):
    def get(self, request):
        contacts = Person.objects.all().order_by('lastname')
        return render(request, "show_all.html", locals())


class AddAddress(View):
    def post(self, request, id):
        city = request.POST.get('city')
        street = request.POST.get('street')
        house_no = request.POST.get('house_no')
        flat_no = request.POST.get('flat_no')
        new_address = Address.objects.create\
            (city=city, street=street, house_no=house_no, flat_no=flat_no)
        contact = Person.objects.get(pk=id)
        contact.address = new_address
        contact.save()
        return HttpResponseRedirect(f'/show/{contact.id}')


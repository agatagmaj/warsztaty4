from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from mail_box.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class NewContact(View):
    def get(self, request):
        return render(request, "new_contact.html")

    def post(self, request):
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        description = request.POST.get('desc')
        # photo = request.FILES['file']
        # <form> attribute -> enctype = "multipart/form-data"
        new_contact = Person.objects.create(name=name, lastname=lastname, description=description)
        return HttpResponseRedirect(f'show/{new_contact.id}')


class ShowContact(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        contacts = contact.phone_set.all()
        emails = contact.email_set.all()
        # cnx = {
        #     "name": contact.name,
        #     "lastname": contact.lastname,
        #     "description": contact.description,
        #     "city": contact.address.city,
        #     "street": contact.address.street,
        #     "house_no": contact.address.house_no,
        #     "flat_no": contact.address.flat_no,
        #     "id": contact.id,
        #     "contacts": contact.phone_set.all(),
        #     "emails": contact.email_set.all()
        # }
        return render(request, "show_contact.html", locals())


class ModifyContact(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        cnx = {
            "name": contact.name,
            "lastname": contact.lastname,
            "description": contact.description,
            "id": contact.id,
        }
        return render(request, "modify_contact.html", cnx)

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
        new_address = Address.objects.create \
            (city=city, street=street, house_no=house_no, flat_no=flat_no)
        contact = Person.objects.get(pk=id)
        contact.address = new_address
        contact.save()
        return HttpResponseRedirect(f'/show/{contact.id}')


class AddPhone(View):
    def post(self, request, id):
        no = request.POST.get('no')
        no_type = request.POST.get('no_type')
        contact = Person.objects.get(pk=id)
        new_phone = Phone()
        new_phone.no = no
        new_phone.no_type = no_type
        new_phone.owner = contact
        new_phone.save()
        return HttpResponseRedirect(f'/show/{contact.id}')


class AddEmail(View):
    def post(self, request, id):
        email = request.POST.get('email')
        email_type = request.POST.get('email_type')
        contact = Person.objects.get(pk=id)
        new_email = Email()
        new_email.email = email
        new_email.email_type = email_type
        new_email.owner = contact
        new_email.save()
        return HttpResponseRedirect(f'/show/{contact.id}')


class AddGroup(View):
    def get(self, request):
        return render(request, "add_group.html")

    def post(self, request):
        name = request.POST.get('name')
        new_group = Groups.objects.create(name=name)
        return HttpResponseRedirect('/groups')


class GroupList(View):
    def get(self, request):
        groups = Groups.objects.all().order_by('name')
        return render(request, "show_groups.html", locals())

    def post(self, request):
        grp = Groups.objects.all()
        search = request.POST.get('search').split(' ')
        search = [x.lower() for x in search]
        groups = []
        for g in grp:
            for a in g.person.all():
                if len(search) > 1:
                    if (search[0] == a.name.lower() and search[1] == a.lastname.lower()) \
                            or (search[1] == a.name.lower() and search[0] == a.lastname.lower()):
                        groups.append(g)
                elif len(search) == 1:
                    if search[0] == (a.name.lower() or a.lastname.lower()):
                        groups.append(g)
        if len(groups) > 0:
            return render(request, "show_groups.html", locals())
        else:
            return HttpResponse("Wskazana osoba nie została dodana do żadnej grupy")


class ShowGroup(View):
    def get(self, request, id):
        group = Groups.objects.get(pk=id)
        cnx = {
            "name": group.name,
            "participants": group.person.all()
        }
        return render(request, "show_group.html", cnx)


class AddParticipant(View):
    def get(self, request, id):
        cnx = {
            "groups": Groups.objects.all()
        }
        return render(request, "add_participants.html", cnx)

    def post(self, request, id):
        contact = Person.objects.get(pk=id)
        groups = request.POST.getlist('groups')
        for g in groups:
            a = Groups.objects.get(id=int(g))
            a.person.add(contact)
        return HttpResponseRedirect('/groups')


class DeletePhone(View):
    def get(self, request, id):
        phone = Phone.objects.get(pk=id)
        p_id = phone.owner.id
        phone.delete()
        return HttpResponseRedirect(f'/show/{p_id}')


class DeleteEmail(View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        p_id = email.owner.id
        email.delete()
        return HttpResponseRedirect(f'/show/{p_id}')


class DeleteAddress(View):
    def get(self, request, id):
        contact = Person.objects.get(pk=id)
        p_id = contact.id
        address_id = int(contact.address.id)
        address = Address.objects.get(id=address_id)
        address.delete()
        return HttpResponseRedirect(f'/show/{p_id}')


class simple_upload(View):
    def post(self, request):
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'core/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request, 'core/simple_upload.html')

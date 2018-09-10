from django.db import models

TYPE_CHOICES = (
    (0, 'nie zdefiniowany'),
    (1, 'prywatny'),
    (2, 'służbowy'),
    (3, 'inny'),
)

class Person(models.Model):
    name = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='mail_box/photos', blank=True)
    address = models.ForeignKey("Address", on_delete=models.PROTECT, null=True)


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64, null=True)
    house_no = models.CharField(max_length=32, null=True)
    flat_no = models.CharField(max_length=32, null=True)

class Phone(models.Model):
    no = models.CharField(max_length=32)
    no_type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE)

class Email(models.Model):
    email = models.CharField(max_length=32)
    email_type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE)

class Groups(models.Model):
    name = models.CharField(max_length=32)
    person = models.ManyToManyField(Person)

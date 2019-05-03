from django.db import models

# Create your models here.


class Interview(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    begin_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

class Adult(models.Model):
    GENRE_OPTIONS = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    interview = models.OneToOneField(Interview, on_delete = models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 50)
    age = models.IntegerField()
    address = models.CharField(max_length = 150)
    occupation = models.CharField(max_length = 30)
    scholarship = models.CharField(max_length = 30)
    marital_status = models.CharField(max_length = 30)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    genre = models.CharField(max_length = 1, choices = GENRE_OPTIONS)
    nationality = models.CharField(max_length = 25, blank=True, null=True)
    religion = models.CharField(max_length = 30, blank=True, null=True)
    birth_location = models.CharField(max_length = 80)
    adults_shared_location = models.IntegerField()
    relationship_adults = models.CharField(max_length=120)

class Context(models.Model):
    KNOW_PERSON_OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
    )
    interview = models.OneToOneField(Interview, on_delete = models.CASCADE, primary_key=True)
    how = models.CharField(max_length = 100)
    know_person = models.CharField(max_length = 2, choices = KNOW_PERSON_OPTIONS)
    when_know = models.CharField(max_length = 20)
    specification = models.CharField(max_length = 300)
    services = models.CharField(max_length = 300)
    actions = models.CharField(max_length = 300)

class Tutor(models.Model):
    adult = models.OneToOneField(Adult, on_delete = models.CASCADE, primary_key = True)
    name = models.CharField(max_length = 50)
    relationship = models.CharField(max_length = 15)
    phone = models.CharField(max_length = 20)
    office_phone = models.CharField(max_length = 20)
    cellphone = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 80, blank=True, null=True)
    address = models.CharField(max_length = 150)
    how = models.CharField(max_length = 300)
    responsibilities = models.CharField(max_length = 300, blank=True, null=True)


class Caregiver(models.Model):
    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
    )
    adult = models.ForeignKey(Adult, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50)
    relationship = models.CharField(max_length = 15)
    phone = models.CharField(max_length = 20)
    office_phone = models.CharField(max_length = 20)
    cellphone = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 80)
    marital_status = models.CharField(max_length = 30)
    religion = models.CharField(max_length = 50)
    address = models.CharField(max_length = 150)
    occupation = models.CharField(max_length = 30)
    can_locate = models.CharField(max_length = 2, choices = OPTIONS)
    how_locate = models.CharField(max_length = 100)
    time = models.CharField(max_length = 100)
    house_time = models.IntegerField()
    why = models.CharField(max_length = 100)
    needs = models.CharField(max_length = 300)
    is_helped = models.CharField(max_length = 2, choices = OPTIONS)
    who_helps = models.CharField(max_length = 150)
    is_regular = models.CharField(max_length = 2, choices = OPTIONS)
    specify = models.CharField(max_length = 50)
    alternative_person = models.CharField(max_length = 50)
    alternative_person_why = models.CharField(max_length = 200, blank=True, null=True)
    alternative_person_phone = models.CharField(max_length = 20)
    alternative_person_email = models.EmailField(max_length = 80)
    where_alternative_person = models.CharField(max_length = 50)
    margin = models.CharField(max_length = 50)
    arguments = models.CharField(max_length = 100)
    leave_caregiver = models.CharField(max_length = 2, choices = OPTIONS)
    why_leave = models.CharField(max_length = 100)

# class Familiogram(models.Model):
#     interview = models.ForeignKey(Interview, on_delete = models.CASCADE)

class Process(models.Model):
    OPTIONS = (
        ('si', 'Si'),
        ('no', 'No'),
    )
    ATENTION = (
        ('1','Temprana'),
        ('2','Intermedia'),
        ('3','Tardía'),
    )
    interview = models.OneToOneField(Interview, on_delete = models.CASCADE, primary_key=True)
    family_rate = models.IntegerField()
    family_why = models.CharField(max_length = 300)
    disease = models.CharField(max_length = 300)
    actions = models.CharField(max_length = 300)
    reunion = models.CharField(max_length = 2, choices = OPTIONS)
    reunion_agreements = models.CharField(max_length = 300)
    not_reunion = models.CharField(max_length = 300)
    indications = models.CharField(max_length = 300)
    conceive = models.CharField(max_length = 150)
    represent = models.CharField(max_length = 300)
    feelings = models.CharField(max_length = 300)
    situation = models.CharField(max_length = 300)
    comments = models.CharField(max_length = 300)
    alternatives = models.CharField(max_length = 200)
    motivation = models.CharField(max_length = 200)
    atention = models.CharField(max_length = 3, choices = ATENTION)
    atention_why = models.CharField(max_length = 100)
    therapy = models.CharField(max_length = 2, choices = OPTIONS)
    therapy_why = models.CharField(max_length = 200)
    talk = models.CharField(max_length = 2, choices = OPTIONS)
    talk_how = models.CharField(max_length = 20)
    hard_part = models.CharField(max_length = 200)
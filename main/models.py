from django.db import models


class Document(models.Model):
    choices = ((0, 'Награда или благодарность'), (1, 'Сертификат или лицензиия'))
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')


class Leader(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')


class Project(models.Model):
    choices = ((0, 'Текущий проект'), (1, 'Сданный объект'))

    group = models.IntegerField(default=0, choices=choices)
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=255)
    short_description = models.TextField(default='')
    # start_date = models.DateField()
    # end_date = models.DateField()
    description = models.TextField()
    storeys = models.IntegerField()
    construction_year = models.IntegerField()


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()


class JobSeeker(models.Model):
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    summary = models.FileField(null=True, upload_to='files/')
    answer = models.TextField(null=True)


class PracticeSeeker(models.Model):
    file = models.FileField(upload_to='files/')


class Question(models.Model):
    name = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    text = models.TextField()
    answer = models.TextField(null=True)

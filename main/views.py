import json
import os
import shutil
from base64 import b64decode, b64encode

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from MosJilStroy import settings
from main.forms import *
from main.models import *

# import datetime


def get_file_size(size):
    if size > 10 ** 6:
        return f'{round(size / 10 ** 6, 1)} MB'
    elif size > 10 ** 3:
        return f'{round(size / 10 ** 3, 1)} KB'
    else:
        return f'{round(size, 1)} B'


def get_contacts_from_json():
    with open('contacts.json', 'r') as file:
        data = json.load(file)
    info = {
        'phone': b64decode(data['phone']).decode(),
        'mail': b64decode(data['mail']).decode(),
        'address': b64decode(data['address']).decode(),
        'office_image': b64decode(data['office_image']).decode()
    }
    return info


def get_about_from_json():
    with open('contacts.json', 'r') as file:
        data = json.load(file)
    about_ctx = {
        'text': b64decode(data['about']['text']).decode(),
        'image': b64decode(data['about']['image']).decode()
    }
    return about_ctx


def get_notify_mail_from_json():
    with open('contacts.json', 'r') as file:
        data = json.load(file)
    return b64decode(data['notifications']).decode()


def send_answer(data):
    body = f'''Здравствуйте, {data.name}!
<h4>Вы задали вопрос компании МосЖилСтрой на сайте mosjilstroy.ru</h4>

Тема: {data.theme}
Вопрос: {data.text}
Ответ: {data.answer}
'''
    html = f'''<h2>Здравствуйте, {data.name}!</h2>
<h4>Вы задали вопрос компании МосЖилСтрой на сайте <a href="mosjilstroy.ru">mosjilstroy.ru</a></h4>

<strong>Тема:</strong> {data.theme} <br><br>
<strong>Вопрос:</strong> {data.text} <br><br>
<strong>Ответ:</strong> {data.answer} <br><br>
'''
    send_mail('Ответ на вопрос "МосЖилСтрой"',
              body, 'questions@mosjilstroy.ru', [data.mail], html_message=html)


def send_notification(title):
    text = 'новое уведомление'
    if title == 'practice':
        text = 'новая заявка на практику'
    elif title == 'vacancy':
        text = 'новая заявка на вакансию'
    elif title == 'question':
        text = 'новый вопрос'
    body = f'''Уважаемая администрация,
на сайте mosjilstroy.ru {text}!
Ознакомиться с этой новостью можно в панели адмминистратора mosjilstroy.ru/admin/
'''
    html = f'''<h2>Уважаемая администрация,</h2>
<h4>на сайте <a href="mosjilstroy.ru">mosjilstroy.ru</a> {text}!</h4>
<p>Ознакомиться с этой новостью можно в панели адмминистратора <a href="mosjilstroy.ru/admin/">mosjilstroy.ru/admin/</a></p>
'''
    send_mail('Уведомление с сайта "МосЖилСтрой"',
              body, 'questions@mosjilstroy.ru',
              [get_notify_mail_from_json()], html_message=html)


#  USER

def root(request):
    info = get_contacts_from_json()
    about_ctx = get_about_from_json()
    return render(request, 'pages/root.html', {'contacts': info,
                                               'about': about_ctx})


def about(request):
    info = get_contacts_from_json()
    snippets = Document.objects.all()
    about_ctx = get_about_from_json()
    docs = []
    for snippet in snippets:
        docs.append({
            'title': snippet.title,
            'image': snippet.image.url,
            'id': snippet.id
        })
    return render(request, 'pages/about.html', {'contacts': info,
                                                'about': about_ctx,
                                                'documents': docs})


def leadership(request):
    info = get_contacts_from_json()
    snippets = Leader.objects.all()
    leaders = []
    for snippet in snippets:
        obj = {
            'name': snippet.name,
            'position': snippet.position,
            'image': snippet.image.url,
        }
        leaders.append(obj)
    return render(request, 'pages/leadership.html', {'contacts': info,
                                                     'leaders': leaders})


def projects(request):
    info = get_contacts_from_json()
    snippets = Project.objects.all()
    current = []
    past = []
    for snippet in snippets:
        obj = {
            'id': snippet.id,
            'image': snippet.image.url,
            'address': snippet.address,
            'short_description': snippet.short_description,
            # 'start_date': snippet.start_date.strftime('%d.%m.%Y'),
            # 'end_date': snippet.end_date.strftime('%d.%m.%Y'),
        }
        if snippet.group == 0:
            current.append(obj)
        elif snippet.group == 1:
            past.append(obj)
    return render(request, 'pages/projects.html', {'contacts': info,
                                                   'current': current,
                                                   'past': past})


def project(request, proj_id):
    try:
        snippet = Project.objects.get(id=proj_id)
    except Project.DoesNotExist:
        return render(request, '404.html')
    info = get_contacts_from_json()
    obj = {
        'status': snippet.choices[snippet.group][1],
        'id': snippet.id,
        'image': snippet.image.url,
        'address': snippet.address,
        'short_description': snippet.short_description,
        'description': snippet.description,
        # 'start_date': snippet.start_date.strftime('%d.%m.%Y'),
        # 'end_date': snippet.end_date.strftime('%d.%m.%Y'),
        'storeys': snippet.storeys,
        'construction_year': snippet.construction_year,
    }
    photos = []
    for i, photo in enumerate(Photo.objects.filter(project_id=proj_id)):
        photos.append({
            'number': i+1,
            'image': photo.image.url,
        })
    return render(request, 'pages/project.html', {'contacts': info,
                                                  'project': obj,
                                                  'photos': photos})


def services(request):
    info = get_contacts_from_json()
    return render(request, 'pages/services.html', {'contacts': info})


def vacancies(request):
    info = get_contacts_from_json()
    snippets = Vacancy.objects.all()
    objects = []
    for snippet in snippets:
        objects.append({
            'id': snippet.id,
            'title': snippet.title,
            'description': snippet.description,
            'salary': snippet.salary,
        })
    with open('contacts.json', 'r') as f:
        questionnaire = b64decode(json.load(f)['questionnaire']).decode()
    return render(request, 'pages/vacancies.html', {
                                                    'questionnaire': questionnaire,
                                                    'contacts': info,
                                                    'vacancies': objects[::-1],
                                                    'form': VacancyForm(),
                                                    'practice_form': PracticeForm()})


def contacts(request):
    info = get_contacts_from_json()
    return render(request, 'pages/contacts.html', {'contacts': info,
                                                   'form': QuestionForm()})


def practice(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/vacancies/')
    file = request.FILES['file']
    practice_form = PracticeForm(request.POST, request.FILES)
    if practice_form.is_valid():
        snippet = PracticeSeeker(file=file)
        snippet.save()
    send_notification('practice')
    return HttpResponseRedirect('/vacancies/')


def respond(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/vacancies/')
    seeker = request.POST.dict()
    seeker_form = VacancyForm(request.POST, request.FILES)
    if seeker_form.is_valid():
        for key in seeker.keys():
            seeker[key] = seeker[key].strip()
        seeker['vacancy_id'] = int(seeker['vacancy_id'])
        seeker['summary'] = request.FILES['summary']
        try:
            Vacancy.objects.get(id=seeker['vacancy_id'])
        except Vacancy.DoesNotExist:
            return HttpResponseRedirect('/vacancies/')
        snippet = JobSeeker(vacancy_id=seeker['vacancy_id'],
                            name=seeker['name'],
                            phone=seeker['phone'],
                            summary=seeker['summary'],
                            answer=seeker['answer'])
        snippet.save()
    send_notification('vacancy')
    return HttpResponseRedirect('/vacancies/')


def question(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/vacancies/')
    quest = request.POST.dict()
    question_form = QuestionForm(request.POST, request.FILES)
    if question_form.is_valid():
        for key in quest.keys():
            quest[key] = quest[key].strip()
        snippet = Question(name=quest['name'],
                           mail=quest['mail'],
                           theme=quest['theme'],
                           text=quest['text'])
        snippet.save()
    send_notification('question')
    return HttpResponseRedirect('/contacts/')


#  ADMIN


def admin_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/admin/')
        info = get_contacts_from_json()
        return render(request, 'admin/login.html', {'contacts': info,
                                                    'form': LoginForm()})
    elif request.method == 'POST':
        login_form = LoginForm(request.POST, request.FILES)
        if not login_form.is_valid():
            return HttpResponseRedirect('/admin/')
        data = request.POST.dict()
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return HttpResponseRedirect('/admin/')
        login(request, user)
        return HttpResponseRedirect('/admin/')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/admin/login/')


def admin_documents(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method == 'GET':
        documents = Document.objects.all()
        docs = []
        form = DocumentForm()
        for snippet in documents:
            docs.append({
                'title': snippet.title,
                'image': snippet.image.url,
                'id': snippet.id
            })
        user = User.objects.get(id=request.user.id)
        return render(request, 'admin/pages/documents.html', {'user': user,
                                                              'documents': docs,
                                                              'form': form})
    elif request.method == 'POST':
        document_form = DocumentForm(request.POST, request.FILES)
        if not document_form.is_valid():
            return HttpResponseRedirect('/admin/')
        data = request.POST.dict()
        data['image'] = request.FILES['image']
        new_doc = Document(title=data['title'],
                           image=data['image'])
        new_doc.save()
        return HttpResponseRedirect('/admin/')


def admin_edit_documents(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    title = data['title']
    doc_id = int(data['id'])
    image = request.FILES.get('image')
    document = Document.objects.get(id=doc_id)
    document.title = title
    if image:
        document.image = image
    document.save()
    return HttpResponseRedirect('/admin/')


def admin_delete_documents(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/')
    data = request.POST.dict()
    doc_id = int(data['id'])
    document = Document.objects.get(id=doc_id)
    document.image.delete()
    document.delete()
    return HttpResponseRedirect('/admin/')


def admin_leaders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method == 'GET':
        snippets = Leader.objects.all()
        leaders = []
        for snippet in snippets:
            obj = {
                'name': snippet.name,
                'position': snippet.position,
                'image': snippet.image.url,
                'id': snippet.id
            }
            leaders.append(obj)
        return render(request, 'admin/pages/leadership.html', {'leaders': leaders,
                                                               'form': LeaderForm()})
    elif request.method == 'POST':
        leader_form = LeaderForm(request.POST, request.FILES)
        if not leader_form.is_valid():
            return HttpResponseRedirect('/admin/leaders/')
        data = request.POST.dict()
        data['image'] = request.FILES['image']
        new_leader = Leader(name=data['name'],
                            position=data['position'],
                            image=data['image'])
        new_leader.save()
        return HttpResponseRedirect('/admin/leaders/')


def admin_edit_leaders(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/leaders/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    name = data['name']
    position = data['position']
    image = request.FILES.get('image')
    lead_id = int(data['id'])
    leader = Leader.objects.get(id=lead_id)
    leader.name = name
    leader.position = position
    if image:
        leader.image = image
    leader.save()
    return HttpResponseRedirect('/admin/leaders/')


def admin_delete_leaders(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/leaders/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/leaders/')
    data = request.POST.dict()
    doc_id = int(data['id'])
    leader = Leader.objects.get(id=doc_id)
    leader.image.delete()
    leader.delete()
    return HttpResponseRedirect('/admin/leaders/')


def admin_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method == 'GET':
        snippets = Project.objects.all()
        current = []
        past = []
        for snippet in snippets:
            obj = {
                'id': snippet.id,
                'group': snippet.group,
                'image': snippet.image.url,
                'address': snippet.address,
                'description': snippet.description,
                'short_description': snippet.short_description,
                # 'start_date': snippet.start_date.strftime('%d.%m.%Y'),
                # 'end_date': snippet.end_date.strftime('%d.%m.%Y'),
                # 'start_value_date': snippet.start_date.strftime('%Y-%m-%d'),
                # 'end_value_date': snippet.end_date.strftime('%Y-%m-%d'),
                'storeys': snippet.storeys,
                'construction_year': snippet.construction_year,
                'photos': [{'url': photo.image.url, 'id': photo.id} for photo in Photo.objects.filter(project=snippet)]
            }
            if snippet.group == 0:
                current.append(obj)
            elif snippet.group == 1:
                past.append(obj)
        form = ProjectForm()
        return render(request, 'admin/pages/projects.html', {'current': current,
                                                             'past': past,
                                                             'form': form})
    elif request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            data = project_form.data.dict()
            # year, month, day = tuple(map(int, data['start_date'].split('-')))
            # data['start_date'] = datetime.date(year, month, day)
            # year, month, day = tuple(map(int, data['end_date'].split('-')))
            # data['end_date'] = datetime.date(year, month, day)
            snippet = Project(
                address=data['address'],
                group=int(data['group']),
                storeys=int(data['storeys']),
                construction_year=int(data['construction_year']),
                # start_date=data['start_date'],
                # end_date=data['end_date'],
                description=data['description'],
                short_description=data['short_description'],
                image=request.FILES.get('image')
            )
            snippet.save()
        return HttpResponseRedirect('/admin/projects/')


def admin_edit_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    subject_id = int(data['subject_id'])
    snippet = Project.objects.get(id=subject_id)
    snippet.address = data['address']
    snippet.group = 0 if data['group'] == 'Текущий проект' else 1
    snippet.storeys = int(data['storeys'])
    snippet.construction_year = int(data['construction_year'])
    # year, month, day = tuple(map(int, data['start_date'].split('-')))
    # snippet.start_date = datetime.date(year, month, day)
    # year, month, day = tuple(map(int, data['end_date'].split('-')))
    # snippet.end_date = datetime.date(year, month, day)
    snippet.description = data['description']
    snippet.short_description = data['short_description']
    image = request.FILES.get('image')
    if image:
        snippet.image = image
    snippet.save()
    return HttpResponseRedirect('/admin/projects/')


def admin_delete_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/projects/')
    data = request.POST.dict()
    project_id = int(data['project_id'])
    try:
        snippet = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return HttpResponseRedirect('/admin/projects/')
    snippet.image.delete()
    photos = Photo.objects.filter(project=snippet)
    for photo in photos:
        photo.image.delete()
        photo.delete()
    snippet.delete()
    return HttpResponseRedirect('/admin/projects/')


def admin_add_photo_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    new_image = request.FILES.get('image')
    project_id = int(request.POST.get('project_id'))
    photo = Photo(image=new_image, project_id=project_id)
    photo.save()
    response = {
        'url': photo.image.url,
        'id': photo.id
    }
    return JsonResponse(response)


def admin_del_photo_projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    photo_id = int(request.POST.get('img_id'))
    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return JsonResponse({'status': 400, 'description': 'This photo does not exist'})
    photo.image.delete()
    photo.delete()
    return JsonResponse({'status': 200, 'description': 'OK'})


def admin_vacancies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method == 'GET':
        vacancy_objs = []
        for snippet in Vacancy.objects.all():
            obj = {
                'id': snippet.id,
                'title': snippet.title,
                'description': snippet.description,
                'salary': snippet.salary,
                'seekers': []
            }
            for job_seeker in JobSeeker.objects.filter(vacancy=snippet):
                summary_size = get_file_size(job_seeker.summary.size)
                obj['seekers'].append({
                    'id': job_seeker.id,
                    'name': job_seeker.name,
                    'phone': job_seeker.phone,
                    'summary': {
                        'url': '/media/' + job_seeker.summary.name,
                        'name': job_seeker.summary.name.replace('files/', ''),
                        'size': summary_size
                    },
                    'answer': job_seeker.answer
                })
            vacancy_objs.append(obj)
        practice_files = []
        for snippet in PracticeSeeker.objects.all():
            size = get_file_size(snippet.file.size)
            practice_files.append({
                'url': '/media/' + snippet.file.name,
                'name': snippet.file.name.replace('files/', ''),
                'size': size,
                'id': snippet.id
            })
        with open('contacts.json', 'r') as file:
            data = json.load(file)
        path = b64decode(data['questionnaire']).decode()
        full_path = settings.MEDIA_ROOT + path.replace('/media', '')
        size = get_file_size(os.path.getsize(full_path))
        questionnaire = {
            'name': os.path.basename(full_path),
            'size': size,
            'url': path
        }
        return render(request, 'admin/pages/vacancies.html', {'questionnaire': questionnaire,
                                                              'vacancies': vacancy_objs[::-1],
                                                              'practice_files': practice_files[::-1],
                                                              'form': AddVacancyForm()})
    elif request.method == 'POST':
        vacancy_form = AddVacancyForm(request.POST, request.FILES)
        data = request.POST.dict()
        if vacancy_form.is_valid():
            title = data['title']
            description = data['description']
            salary = int(data['salary'])
            new_vacancy = Vacancy(title=title, description=description, salary=salary)
            new_vacancy.save()
        return HttpResponseRedirect('/admin/vacancies/')


def admin_edit_vacancies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    vacancy_id = int(data['vacancy_id'])
    snippet = Vacancy.objects.get(id=vacancy_id)
    snippet.title = data['title']
    snippet.description = data['description']
    snippet.salary = int(data['salary'])
    snippet.save()
    return HttpResponseRedirect('/admin/vacancies/')


def admin_delete_vacancies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method != 'POST':
        return HttpResponseRedirect('/admin/vacancies/')
    data = request.POST.dict()
    vacancy_id = int(data['vacancy_id'])
    try:
        snippet = Vacancy.objects.get(id=vacancy_id)
    except Project.DoesNotExist:
        return HttpResponseRedirect('/admin/vacancies/')
    snippet.delete()
    return HttpResponseRedirect('/admin/vacancies/')


def admin_del_practice_seeker(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    seeker_id = int(data['seeker_id'])
    try:
        snippet = JobSeeker.objects.get(id=seeker_id)
    except JobSeeker.DoesNotExist:
        return HttpResponseRedirect('/admin/vacancies/')
    path = snippet.summary.path
    if os.path.isfile(path):
        shutil.move(path, settings.MEDIA_ROOT + '/deleted/')
    snippet.delete()
    return JsonResponse({'status': 200, 'description': 'OK'})


def admin_del_practice_file(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    file_id = int(data['file_id'])
    try:
        snippet = PracticeSeeker.objects.get(id=file_id)
    except PracticeSeeker.DoesNotExist:
        return HttpResponseRedirect('/admin/vacancies/')
    path = snippet.file.path
    del_path = settings.MEDIA_ROOT + '/deleted/'
    if os.path.isfile(path):
        shutil.move(path, del_path)
    snippet.delete()
    return JsonResponse({'status': 200, 'description': 'OK'})


def admin_contacts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    if request.method == 'GET':
        with open('contacts.json', 'r') as file:
            data = json.load(file)
        info = {
            'phone': b64decode(data['phone']).decode(),
            'mail': b64decode(data['mail']).decode(),
            'address': b64decode(data['address']).decode(),
            'notifications': b64decode(data['notifications']).decode(),
            'office_image': b64decode(data['office_image']).decode()
        }
        new_questions = []
        answered_questions = []
        for snippet in Question.objects.all():
            obj = {
                'id': snippet.id,
                'name': snippet.name,
                'mail': snippet.mail,
                'theme': snippet.theme,
                'text': snippet.text,
                'answer': snippet.answer
            }
            if not obj['answer']:
                new_questions.append(obj)
            else:
                answered_questions.append(obj)
        about_ctx = get_about_from_json()
        return render(request, 'admin/pages/contacts.html', {'contacts': info,
                                                             'about': about_ctx,
                                                             'new_questions': new_questions[::-1],
                                                             'answered_questions': answered_questions[::-1]})
    elif request.method == 'POST':
        data = request.POST.dict()
        with open('contacts.json', 'r') as file:
            info = json.load(file)
        office_image = request.FILES.get('office_image')
        info['phone'] = b64encode(data['phone'].encode()).decode()
        info['mail'] = b64encode(data['mail'].encode()).decode()
        info['address'] = b64encode(data['address'].encode()).decode()
        info['notifications'] = b64encode(data['notifications'].encode()).decode()
        if office_image:
            path = default_storage.save('images/' + office_image.name, ContentFile(office_image.read()))
            last_image = settings.MEDIA_ROOT + b64decode(info['office_image']).decode().replace('/media', '')
            if os.path.isfile(last_image):
                os.remove(last_image)
            info['office_image'] = b64encode(('/media/' + path).encode()).decode()
        with open('contacts.json', 'w') as file:
            json.dump(info, file)
        return HttpResponseRedirect('/admin/contacts/')


def admin_set_answer(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    question_id = int(data['question_id'])
    answer = data['answer'].strip()
    snippet = Question.objects.get(id=question_id)
    snippet.answer = answer
    snippet.save()
    send_answer(snippet)
    return HttpResponseRedirect('/admin/contacts/')


def admin_del_question(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    data = request.POST.dict()
    question_id = int(data['question_id'])
    try:
        snippet = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return HttpResponseRedirect('/admin/contacts/')
    snippet.delete()
    return JsonResponse({'status': 200, 'description': 'OK'})


def admin_about_save(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    text = request.POST.get('text')
    image = request.FILES.get('image')
    with open('contacts.json', 'r') as file:
        data = json.load(file)
    if image:
        path = default_storage.save('images/'+image.name, ContentFile(image.read()))
        last_image = settings.MEDIA_ROOT + b64decode(data['about']['image']).decode().replace('/media', '')
        if os.path.isfile(last_image):
            os.remove(last_image)
        data['about']['image'] = b64encode(('/media/' + path).encode()).decode()
    data['about']['text'] = b64encode(text.encode()).decode()
    with open('contacts.json', 'w') as file:
        json.dump(data, file)
    return HttpResponseRedirect('/admin/contacts/')


def admin_questionnaire(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/')
    file = request.FILES.get('file')
    with open('contacts.json', 'r') as f:
        data = json.load(f)
    if file:
        path = default_storage.save('files/' + file.name, ContentFile(file.read()))
        last_file = b64decode(data['questionnaire']).decode()
        last_file_path = settings.MEDIA_ROOT + last_file.replace('/media', '')
        last_file_del_path = settings.MEDIA_ROOT + '/deleted/'
        if os.path.isfile(last_file_path):
            shutil.move(last_file_path, last_file_del_path)
        data['questionnaire'] = b64encode(('/media/' + path).encode()).decode()
        with open('contacts.json', 'w') as f:
            json.dump(data, f)
    return HttpResponseRedirect('/admin/vacancies/')


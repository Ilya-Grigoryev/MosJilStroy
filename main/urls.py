from django.urls import path
from main.views import *


urlpatterns = [
    path('', root, name='root'),
    path('documents/', about, name='about'),
    path('leaders/', leadership, name='leaders'),
    path('projects/', projects, name='projects'),
    path('project/<int:proj_id>/', project, name='project'),
    path('services/', services, name='services'),
    path('respond/', respond, name='respond'),
    path('practice/', practice, name='practice'),
    path('vacancies/', vacancies, name='vacancies'),
    path('contacts/', contacts, name='contacts'),
    path('question/', question, name='question'),
]


urlpatterns += [
    path('admin/login/', admin_login, name='login'),
    path('admin/logout/', admin_logout, name='logout'),

    path('admin/', admin_documents, name='admin-documents'),
    path('admin/edit-document/', admin_edit_documents, name='admin-edit-documents'),
    path('admin/delete-document/', admin_delete_documents, name='admin-delete-documents'),

    path('admin/leaders/', admin_leaders, name='admin-leaders'),
    path('admin/edit-leader/', admin_edit_leaders, name='admin-edit-leaders'),
    path('admin/delete-leader/', admin_delete_leaders, name='admin-delete-leaders'),

    path('admin/projects/', admin_projects, name='admin-projects'),
    path('admin/edit-project/', admin_edit_projects, name='admin-edit-projects'),
    path('admin/delete-project/', admin_delete_projects, name='admin-delete-projects'),
    path('admin/projects/add-photo/', admin_add_photo_projects, name='admin-add-photo-projects'),
    path('admin/projects/del-photo/', admin_del_photo_projects, name='admin-del-photo-projects'),

    path('admin/vacancies/', admin_vacancies, name='admin-vacancies'),
    path('admin/questionnaire/', admin_questionnaire, name='admin-questionnaire'),
    path('admin/edit-vacancy/', admin_edit_vacancies, name='admin-edit-vacancies'),
    path('admin/delete-vacancy/', admin_delete_vacancies, name='admin-delete-vacancies'),
    path('admin/practice/del-file/', admin_del_practice_file, name='admin-del-practice-file'),
    path('admin/practice/del-seeker/', admin_del_practice_seeker, name='admin-del-practice-seeker'),

    path('admin/contacts/', admin_contacts, name='admin-contacts'),
    path('admin/set-answer/', admin_set_answer, name='admin-set-answer'),
    path('admin/del-question/', admin_del_question, name='admin-del-question'),
    path('admin/save-about/',  admin_about_save,  name='admin-about-save'),
]
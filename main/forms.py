from django import forms


class VacancyForm(forms.Form):
    vacancy_id = forms.CharField(
        widget=forms.TextInput()
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'placeholder': 'ФИО'}
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'type': 'tel',
                   'placeholder': 'Телефон'}
        )
    )
    summary = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px;'}
        )
    )
    answer = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control text-input',
                   'style': 'height: 200px; margin-top: 5px',
                   'placeholder': 'Почему вы хотите работать у нас?'}
        )
    )


class QuestionForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'placeholder': 'Имя'}
        )
    )
    mail = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'type': 'mail',
                   'placeholder': 'Почта для ответа'}
        )
    )
    theme = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'type': 'mail',
                   'placeholder': 'Тема'}
        )
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control text-input',
                   'style': 'height: 200px; margin-top: 15px',
                   'placeholder': 'Текст сообщения'}
        )
    )


class PracticeForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control text-input'}
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'type': 'login',
                   'placeholder': 'Логин'}
        )
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 15px',
                   'type': 'password',
                   'placeholder': 'Пароль'}
        )
    )


class DocumentForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'Заголовок документа'}
        )
    )
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control text-input',
                   'id': 'add-img-load',
                   'style': 'margin-top: 10px',
                   'accept': 'image/*',
                   'placeholder': 'Документ'}
        )
    )


class LeaderForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'ФИО'}
        )
    )
    position = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 10px',
                   'placeholder': 'Должность'}
        )
    )
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control text-input',
                   'id': 'add-img-load',
                   'style': 'margin-top: 10px',
                   'accept': 'image/*',
                   'placeholder': 'Фотография'}
        )
    )


class ProjectForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'Адресс'}
        )
    )
    group = forms.ChoiceField(
        choices=((0, 'Текущий проект'), (1, 'Сданный объект')),
        widget=forms.Select(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'Статус'}
        )
    )
    storeys = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'Кол-во этажей'}
        )
    )
    construction_year = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control text-input',
                   'placeholder': 'Год постройки'}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control text-input',
                   'style': 'height: 200px; margin-top: 10px',
                   'placeholder': 'Описание'}
        )
    )
    short_description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control text-input',
                   'style': 'height: 100px; margin-top: 10px',
                   'placeholder': 'Краткое описание'}
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control text-input',
                   'id': 'add-img-load',
                   'style': 'margin-top: 10px',
                   'accept': 'image/*',
                   'placeholder': 'Фотография'}
        )
    )


class AddVacancyForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 10px',
                   'placeholder': 'Название'}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control text-input',
                   'style': 'height: 300px; margin-top: 10px',
                   'placeholder': 'Описание'}
        )
    )
    salary = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control text-input',
                   'style': 'margin-top: 10px',
                   'placeholder': 'Заработная плата'}
        )
    )

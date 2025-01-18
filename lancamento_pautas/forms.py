from django import forms
from django.core.exceptions import ValidationError

from .models import Disciplina, Estudante, ESCOLHER_MODELO, Pauta, Nota


class SubmeterPautaForm(forms.ModelForm):

    class Meta:
        model = Pauta
        fields = ['modelo', 'descricao', 'disciplina', 'estudantes']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            }),
            'modelo': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Escolhe o turno',
            }),
            'disciplina': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            }),
            'estudantes': forms.SelectMultiple(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            }),
        }


class SubmeterNotaForm(forms.ModelForm):

    class Meta:
        model = Nota
        exclude = ['AC1', 'AC2', 'PF1', 'PF2']
        widgets = {
            'pauta': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            }),
            'estudante': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            }),
        }


class SubmeterDisciplinaForm(forms.ModelForm):

    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo', 'turno', 'professor', 'estudantes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Nome da disciplina'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Código da disciplina',
                'maxlength': '3',
                'required': 'true'
            }),
            'turno': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Escolhe o turno',
            }),
            'professor': forms.Select(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Selecione o professor',
            }),
            'estudantes': forms.SelectMultiple(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                'placeholder': 'Selecione o/os estudantes',
            }),
        }

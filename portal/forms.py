from django import forms


class adminInputForm(forms.Form):
    lectureno = forms.CharField(max_length=254)
    videolink = forms.CharField(max_length=254)
    Assignment = forms.CharField(max_length=254)

from django import forms


class ParseForm(forms.Form):
    id_user = forms.CharField(required=True)
    api_key = forms.CharField(required=True)

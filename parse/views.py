from django.shortcuts import render

from parse.forms import ParseForm
from parse.tasks import task_parse


def ozon_parse(request):
    if request.method == 'POST':
        form = ParseForm(request.POST)
        if form.is_valid():
            id_user = form.cleaned_data.get('id_user')
            api_key = form.cleaned_data.get('api_key')
            task_parse.delay(id_user=id_user, api_key=api_key)
    else:
        form = ParseForm()
    return render(request, 'parse.html', {'form': form})

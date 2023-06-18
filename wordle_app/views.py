from django.shortcuts import render, redirect
from .models import Word
from django.db.models import Q

def delete_word(request, word_id):
    word_to_delete = Word.objects.get(id=word_id)
    word_to_delete.delete()
    return redirect('/')

def add_word(request):
    error_message_add = None

    if request.method == "POST":
        word_to_add = request.POST.get('word')
        if len(word_to_add) != 5:
            error_message_add = "Word must be 5 characters long."
        elif not word_to_add.isalpha():
            error_message_add = "Word must only contain letters."
        elif Word.objects.filter(text__iexact=word_to_add).exists():
            error_message_add = "Word already exists."
        else:
            Word.objects.create(text=word_to_add)
            return redirect('/')

        words = Word.objects.all().order_by('text')
        context = {'error_message_add': error_message_add, 'words': words}
        return render(request, 'home.html', context)

    return redirect('/')

def search_words(request):
    error_message = None  
    param_starts = request.POST.get('search_param_starts')
    param_ends = request.POST.get('search_param_ends')
    param_contains = request.POST.get('search_param_contains')
    param_excludes = request.POST.get('search_param_excludes')

    query = Q()

    if param_starts:
        query &= Q(text__startswith=param_starts)
    if param_ends:
        query &= Q(text__endswith=param_ends)
    if param_contains:
        for letter in param_contains:
            query &= Q(text__contains=letter)
    if param_excludes:
        for letter in param_excludes:
            query &= ~Q(text__contains=letter)

    words = Word.objects.filter(query).order_by('text')

    context = {'words': words, 'error_message': error_message}
    return render(request, 'home.html', context)

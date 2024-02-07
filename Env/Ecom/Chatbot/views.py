from django.shortcuts import render
from . models import *
from nlp import extract_intent_and_entities

# Create your views here.

def chatview(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        intent, entities = extract_intent_and_entities(user_input)
        Message.objects.create(text=user_input, intent=intent, entities=entities)
        return render(request, 'chatbot/reply.html', {'intent': intent, 'entities': entities})
        
    return render(request, 'chatbot/chat.html')
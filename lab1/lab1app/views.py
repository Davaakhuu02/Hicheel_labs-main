from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
    item_list = Item.objects.all()
    category_list = Category.objects.all()
    item_dic = {'items': item_list,
                'categories': category_list }
    return render(request, 'index.html', context = item_dic)
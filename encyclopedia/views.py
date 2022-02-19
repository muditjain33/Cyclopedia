from django.shortcuts import render
from . import util
import markdown2
import random
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse

class NewSearch(forms.Form):
    search= forms.CharField(max_length=100,widget= forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":NewSearch()
    })

def page(request,name):
    for entry in util.list_entries():
        if entry==name:
            value=util.get_entry(name)
            value=markdown2.markdown(value)
            return render(request,"encyclopedia/page.html",{
                "title":name,
                "value":value,
                "form":NewSearch()
            })
    return render(request,"encyclopedia/error.html",{"form":NewSearch()})

def search(request):
    if(request.method == "POST"):
        form=NewSearch(request.POST)
        if form.is_valid():
            item=form.cleaned_data["search"]
            # return HttpResponse(f"I Love you {item}")
            l=[]
            for entry in util.list_entries():
                if entry==item:
                    return HttpResponseRedirect(reverse('page', args=(),kwargs={'name': item}))
                if item in entry:
                    l.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": l,
                "form":NewSearch()
            })  
    else:
        form = NewSearch()
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })

def randome(request):
    item= random.choice(util.list_entries())
    if item:
        return HttpResponseRedirect(reverse('page', args=(),kwargs={'name': item}))
    else:
        return render(request,"encyclopedia/error.html",{"form":NewSearch()})

class CreateItem(forms.Form):
    Title  = forms.CharField(max_length=100,widget= forms.TextInput(attrs={'placeholder':'Title of the page'}))
    Content= forms.CharField(widget=forms.Textarea)

def create(request):
    if(request.method == 'POST'):
         form1=CreateItem(request.POST)
         if form1.is_valid():
            title=form1.cleaned_data['Title']
            content=form1.cleaned_data['Content']
            for entry in util.list_entries():
                if entry==title:
                    return render(request,"encyclopedia/error1.html",{"form":NewSearch()})
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('page', args=(),kwargs={'name': title}))
    else:
        return render(request, "encyclopedia/create.html", {"form":NewSearch(),"form1":CreateItem()})


def edit(request,name):
    class EditItem(forms.Form):
        # Content= forms.CharField(widget=forms.Textarea(attrs={'value': util.get_entry(name)}))
        Content= forms.CharField(initial=util.get_entry(name),widget=forms.Textarea)
    # # return HttpResponse(f"I Love you {name}")    
    if(request.method == 'POST'):
        form2=EditItem(request.POST)
        if form2.is_valid():
            content=form2.cleaned_data['Content']
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse('page', args=(),kwargs={'name': name}))
    else:
        return render(request,"encyclopedia/edit.html",{"form":NewSearch(),"form2":EditItem(),"title":name})
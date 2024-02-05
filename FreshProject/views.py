from django.shortcuts import render

def basic(request):
    con = "THIS IS A HTML PAGE"
    return render(request, "basic.html", {"KEY": con})

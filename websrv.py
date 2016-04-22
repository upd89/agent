#!/usr/bin/env python

from bottle import get, post, request, run, abort, redirect

@get('/')
def index():
    redirect('MainPage')

@get('/MainPage')
def main():
    return "MainPage"

@get('/:name')
def display(name):
    return "render page " + name

@get('/:name/edit')
def edit_form(name):
    form  = "<form method='post'>"
    form += "<input type=text name=content>"
    form += "<input type=submit name=submit>"
    form += "</form>"
    return "edit form " + name + form

@post('/:name/edit')
def edit(name):
    #content = request.forms.get('content')
    if request.POST.get('submit'):
        return(request.POST['content'])
    #redirect("/%s" % name)

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)

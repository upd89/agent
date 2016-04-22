#!/usr/bin/env python

from bottle import get, post, request, run, abort, redirect

@get('/')
def index():
    redirect('MainPage')

@get('/MainPage')
def main():
    return "MainPage"

@get(':name')
def display(name):
    return "render page " + name

@get(':name/edit')
def edit_form(name):
    return "edit form " + name

@post(':name/edit')
def edit(name):
    if request.POST.get('subit'):
        print(request.POST['content'])
    redirect("/%s" % name)

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)

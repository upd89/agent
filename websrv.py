#!/usr/bin/env python

from bottle import get, post, request, run, abort, redirect
import json
import lib.persist

@get('/')
def index():
    redirect('help')

@get('/help')
def main():
    return "nothing to see here"

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

@post('/task')
def new_task():
    tasks = lib.persist.Persist("tasks.data")
    # TODO: Test if json is valid
    data = json.load(request.body)
    #tasks.set_key("0", request.body.read())
    tasks.set_key(data.get('task_id').encode("utf8"), request.body.read())
    tasks.close()
    return("ok")

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)

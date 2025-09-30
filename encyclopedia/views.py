from django.shortcuts import redirect, render

from . import util
import markdown2
import random 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    
    if query in entries:
        #instead of repeating and typing long sentences, 
        # we can call entry() function from above
        return entry(request, title=query)
    
    # e is a variable just like we use n and i in loops and conditions
    results = [e for e in entries 
                 if query.lower() in e.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def new_page(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")

        #if it already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message" : "this entry already exists. "
            })
        # if its new
        util.save_entry(title, content)
        return redirect("entry", title=title)
    # eza kan get request show the form
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    content = util.get_entry(title)

    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist."
        })

    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)
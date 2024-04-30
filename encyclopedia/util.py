import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from markdown2 import Markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    _, entriesDir = default_storage.listdir("entries");
    
    for entry in entriesDir:
        if title.lower() == entry.lower().replace(".md", ""):
            raise FileExistsError
        else:
            continue
    
    filename = f"entries/{title}.md"
    
    default_storage.save(filename, ContentFile(content))
    
    return "Ok"

def edit_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    _, entriesDir = default_storage.listdir("entries");
    
    for entry in entriesDir:
        if title.lower() == entry.lower().replace(".md", ""):
            filename = f"entries/{entry}"
            default_storage.delete(filename)
            default_storage.save(filename, ContentFile(content))
            return
        else:
            continue
    
    raise FileNotFoundError
    

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        _, entriesDir = default_storage.listdir("entries");
        
        for entry in entriesDir:
            if title.lower() == entry.lower().replace(".md", ""):
                f = default_storage.open(f"entries/{entry}")
                return f.read().decode("utf-8")
            else:
                continue
    except FileNotFoundError:
        return None

def entry_to_html(content):
    """
    Converts markdown to html
    """
    md = Markdown()
    return md.convert(content)

def get_entry_html(title):
    """
    Retrieves an encyclopedia entry by its title and converts the markdown content to html.
    If no such entry exists, the function returns None.
    """
    content = get_entry(title)
    if content:
        return entry_to_html(content)
    else:
        return None
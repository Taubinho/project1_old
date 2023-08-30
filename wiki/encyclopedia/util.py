import re
import pdb

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """

    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def search_entries(term):
    """
    Returns a query as list if search term matches an entry, else it returns a 
    list of entries that have the query as a substring.
    """
    
    entries = list_entries()
    search_result=[]

    for entry in entries:
        if re.search(term.upper(),entry.upper()):
            search_result.append(entry)
    
    return search_result


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


"""def ghetto_markdown(text):

    re.sub(r"[#](.*)(?:\n|$)", "<h1>\\1</h1>",text)
    re.sub(r"[*_]{2}(.*)[*_]{2}", "<b>\\1</b>", text)
    re.sub(r"[\n]{2}", "<p>\\1</p>", text)

    re.sub(r"[\[](?P<text>.*)[\]][\(](?P<link>.*)[\)]",lambda match:if text)
    if link_matches:
        for match in link_matches:
            replace(match, f"<a href='{match[0]}'>{match[1]}</a>")

    ul_matches = re.sub(r"[-*+](.*?)(?:\n|$)", text)

    return text 

You can create a new paragraph by leaving a blank line between lines of text."""
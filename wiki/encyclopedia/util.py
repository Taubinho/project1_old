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


def markdown_lite(text):
    """
    Modifies text so that it can 'support' markdown, only works for headings (just lvl1), bolding, making paragraphs,
    links and unordered lists. It does that by using regular expresions and substituting markdown syntax with HTML.
    https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
    """

    # uses regular expresions to substitute any line that starts with '#' to be encased with '<h1></h1>'
    # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#headings 
    
    # replacement function used to find the "level" of the heading
    def create_headers(match):
        header_lvl = len(match.group(1))
        if header_lvl > 6:
            header_lvl = 6

        return f"<h{header_lvl}>{match.group(2)}</h{header_lvl}>"


    modified_text = re.sub(r"^(#+)(.*)$", create_headers, text, flags=re.MULTILINE)

    # uses regular expresions to bolden ('<b></b>') text between two underscores (_) or stars (*)
    # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#styling-text
    modified_text = re.sub(r"[*_]{2}(.*?)[*_]{2}", "<b>\\1</b>", modified_text)

    # uses regulare expresions to insert a paragraph ('<p></p>') if there is an empty line in the text
    # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#paragraphs
    
    modified_text = re.sub(r"(\n\s*\n(.*)(?=\n\s*\n|$))", "<p>\\2</p>", modified_text, flags=re.DOTALL)

    # creates HTML links ('<a href="..."></a>') from markdown link syntax ([text to display](http_link))
    # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links
    def create_links(match):
        text = match.group(1)
        link = match.group(2)

        return "<a href ='" + link + "'>" + text + "</a>"

    modified_text = re.sub(r"[\[](?P<text>.*?)[\]][\(](?P<link>.*?)[\)]", create_links, modified_text)

    # creates unordered lists from markdown syntax ("You can make an unordered list by preceding one or more lines of text with -, *, or +")
    # https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#lists
    def create_list_items(match):
        for group in match.groups():
            list_item ='<li>' + group + '</li>'
        return list_item
    
    def create_list(match):
        for group in match.groups():
            return '<ul>' + group + '</ul>'
    
    modified_text = re.sub(r"^[-*+](.*?)(?:\n|$)", create_list_items, modified_text, flags=re.MULTILINE)
    modified_text = re.sub(r"(<li>.*</li>)", create_list, modified_text)

    return modified_text


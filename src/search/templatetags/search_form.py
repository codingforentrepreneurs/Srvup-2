from django import template
register = template.Library()


@register.inclusion_tag('search/snippets/search_form.html')
def search_form(request, navbar=False):
    return {"request": request, 'navbar':navbar}
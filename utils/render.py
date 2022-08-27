from django.template import Context, Template

def html(obj_dict, html_like):
    t = Template(html_like)
    c = Context(obj_dict)
    return t.render(c)
PREDEFINED_HTML = {}

PREDEFINED_HTML['f#btns'] = '''
    <span>
        <a title="{{html_params.title_edit}}" href="{{html_params.editHref}}" class="fsharp_btns_edit" row_id="{{row.id}}">{{html_params.editBtn}}</a>
        <a title="{{html_params.title_del}}"  href="{{html_params.delHref}}"  class="fsharp_btns_del" row_id="{{row.id}}">{{html_params.delBtn}}</a>
        <a title="{{html_params.title_view}}" href="{{html_params.viewHref}}" class="fsharp_btns_view" row_id="{{row.id}}">{{html_params.viewBtn}}</a>
    </span>
'''

PREDEFINED_HTML['f#link'] = '''
    <a title="{{html_params.title_href}}" href="{{html_params.href}}">{{html_params.jumpBtn}}</a>
'''
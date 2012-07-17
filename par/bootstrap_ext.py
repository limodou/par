def bootstrap_tabs(visitor, items):
    def format_id(s):
        return s.replace('.', '-')
    
    txt = []
    txt.append('<div class="tabbable">')
    
    txt.append('<ul class="nav nav-tabs">')
    for i, x in enumerate(items):
        if 'title' not in x:
            x['kwargs']['title'] = x['kwargs']['id']
        if i == 0:
            cls = ' class="active"'
        else:
            cls = ''
        txt.append('<li%s><a href="#%s" data-toggle="tab">%s</a></li>' % (cls, format_id(x['kwargs']['id']), x['kwargs']['title']))
    txt.append('</ul>')
    
    txt.append('<div class="tab-content">')
    for i, x in enumerate(items):
        if i == 0:
            cls = ' active'
        else:
            cls = ''
        txt.append('<div class="tab-pane%s" id="%s">' % (cls, format_id(x['kwargs']['id'])))
        text = visitor.parse_text(x['body'], 'article')
        txt.append(text)
        txt.append('</div>')
    txt.append('</div>')
    
    txt.append('</div>')
    
    return '\n'.join(txt)

def bootstrap_alert(visitor, items):
    """
    Format:
        
        [[alert(class=error)]]:
            message
    """
    txt = []
    for x in items:
        cls = x['kwargs'].get('class', '')
        if cls:
            cls = 'alert-%s' % cls
        txt.append('<div class="alert %s">' % cls)
        if 'close' in x['kwargs']:
            txt.append('<button class="close" data-dismiss="alert">&times;</button>')
        text = visitor.parse_text(x['body'], 'article')
        txt.append(text)
        txt.append('</div>')
    return '\n'.join(txt)

blocks = {'tabs':bootstrap_tabs, 'alert':bootstrap_alert}
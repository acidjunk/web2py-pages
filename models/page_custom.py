db.define_table('page_item_custom',
    Field('page', db.page, writable=False, readable=False, label=T('Page')),
    Field('page_item', db.page_item, writable=False, readable=False, label=T('Page item')),
    Field('column', type='string', requires=IS_IN_SET(('full','left','right')), label=T('Alignment')),
    Field('title', type='string', label=T('Title')),
    Field('image', type='upload', label=T('Image')),
    Field('background', type='upload', label=T('Background')),
    Field('background_repeat', type='string', requires=IS_EMPTY_OR(IS_IN_SET(('no-repeat', 'repeat', 'repeat-x', 'repeat-y'))), label=T('Background repeat')),
    Field('background_position', type='string', requires=IS_EMPTY_OR(IS_IN_SET(('right bottom','right center','right top','left bottom','left center','left top','center bottom','center center','center top'))), label=T('Background position')),
    Field('min_height', type='integer', label=T('Height of box in pixels (optional)')))

def openCustomDiv(custom):
    html = ''
    if not custom.background_position or custom.background_position == None:
        custom.background_position = 'right bottom'
    if not custom.background_repeat or custom.background_repeat == None:
        custom.background_repeat = 'no-repeat'
        
    if custom.min_height and custom.background:
        html += '<div class="page column_%s" style="min-height:%spx; background-image:url(\'%s\'); background-repeat:%s; background-position:%s;">' % (custom.column, custom.min_height, URL('default', 'download', args=custom.background), custom.background_repeat, custom.background_position)
    elif custom.background:
        html += '<div class="page column_%s" style="background-image:url(\'%s\'); background-repeat:%s; background-position:%s;">' % (custom.column, URL('default', 'download', args=custom.background), custom.background_repeat, custom.background_position)
    elif custom.min_height:
        html += '<div class="page column_%s" style="min-height:%spx;">' % (custom.column, custom.min_height)
    else:
        html += '<div class="page column_%s">' % (custom.column)
    if custom.image:
        html += str(IMG(_src=URL('default', 'download', args=custom.image), _class='custom_img'))
        html += '<div class="content">'
    if custom.title:
        html += str(H2(custom.title))
    return XML(html)
    
    
def closeCustomDiv(custom):
    html=''
    if custom.image:
        html += '</div><div style="clear:both;"></div></div>'
    else:
        html += '</div>'
    #html += '<div style="clear:both;"></div>'
    return XML(html)

from datetime import datetime

sidebars_left=[]
sidebars_right=[]
breadcrumbs=[]
if request.controller=='pagetree' and (request.function=='show' or request.function=='showEditable') and request.args(0):
    #request 1 should be ID or URL_name
    try:
        pagetree=db.pagetree[int(request.args(0))] or redirect(error)
    except:
        pagetree=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        
    org_id=pagetree.id
    parent=pagetree.id
    done=False
    menu=[]
    while not done:
        try:
            pagetree=db.pagetree[parent] or redirect(error)
            if pagetree.randomOrdered: page_children=db(db.pagetree.parent==pagetree.id).select(orderby='<random>')   
            else: page_children=db(db.pagetree.parent==pagetree.id).select(orderby=db.pagetree.order_nr)  
            if pagetree.id != org_id:
                breadcrumbs.append({'title':pagetree.title, 'url':pagetree.url})
            parent=pagetree.parent
            if page_children:
                menu=[]
                for child in page_children:
                    menu.append((XML('%s' % child.short_title), URL(request.controller,request.function, args=child.url)==URL(args=request.args), URL('pagetree','show/%s' % (child.url))))
                #Hook for bouwstroomloket
                if pagetree.url=='contact':
                    menu.append(('Locatie', False, URL('contact','index')))
                if pagetree.url=='nieuws':
                    menu.append(('Social Media Nieuws', False, URL('aggregator','index')))
                if pagetree.childrenTitle:
                    title=pagetree.childrenTitle
                else:
                    title=pagetree.short_title
                if pagetree.parent != 0:
                    sidebars_right.append({'title':title, 'menu':menu})
                else:
                    sidebars_left.append({'title':title, 'menu':menu})
            elif pagetree.url=='contact':
                if pagetree.childrenTitle:
                    title=pagetree.childrenTitle
                else:
                    title=pagetree.short_title
                menu=[]
                menu.append(('Locatie', False, URL('contact','index')))
                if pagetree.parent != 0:
                    sidebars_right.append({'title':title, 'menu':menu})
                else:
                    sidebars_left.append({'title':title, 'menu':menu})
        except:
            done=True

    #UBERKOOL way to reverse items in list
    sidebars_left=sidebars_left[::-1]
    sidebars_right=sidebars_right[::-1]
    breadcrumbs=breadcrumbs[::-1]
  
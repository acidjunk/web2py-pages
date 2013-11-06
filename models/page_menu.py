##########################################
## this is the main application menu
## add/remove items as required
##########################################
error=URL(r=request,f='error')

#MAIN MENU
pages=db((db.page.parent==0) & (db.page.language==T.accepted_language) & (db.page.isMenuitem==True)).select(orderby=db.page.order_nr)
for page in pages:
    sub_pages=db((db.page.parent==page.id) & (db.page.isMenuitem==True)).select(orderby=db.page.order_nr)
    submenu=[]
    for sub_page in sub_pages:
        submenu.append([sub_page.short_title, False, URL('page','show/%s' % (sub_page.url))])
    response.menu.append((page.short_title, False, URL('page','show/%s' % (page.url)), submenu))
    
#FIRST LEVEL SUBMENUUS AND NAVIGITION HELP
""""
response.right_menu=[]
response.navigation_helper=[]
if request.controller=="page" and (request.function=="show" or request.function=="showEditable"):
    try:
        page_id=int(request.args(0))
        page=db.page[page_id] or redirect(error)
    except:
        page=db(db.page.url==request.args(0)).select().first() or redirect(error)
        page_id=page.id
    
    if page.childrenTitle: response.right_menu_title=page.childrenTitle
    else: response.right_menu_title=page.short_title
    sub_pages=db(db.page.parent==page_id).select(orderby=db.page.order_nr)
    if page_id==77:
        response.right_menu.append(('Medewerkers', False, URL('default','showEmployees'),[]))
    for sub_page in sub_pages:
        response.right_menu.append((sub_page.short_title, False, URL('page','show/%s' % (sub_page.url),[])))
    # deal with navigation helper
    parent=page.parent
    done=False
    while not done:
        try:
            temp_page=db.page[parent] or redirect(error)
            response.navigation_helper.insert(0,(temp_page.short_title, False, URL('page','show/%s' % (temp_page.url),[])))
            parent=temp_page.parent
        except:
            done=True
elif request.controller=="default" and (request.function=="showNews" or request.function=="showNewsItem"):
    news=db(db.news.id>0).select(orderby=~db.news.posted_on) or redirect(error)
    response.right_menu_title="Nieuws"
    for newsitem in news:
        response.right_menu.append((newsitem.short_title, False, URL('default','showNewsItem/%s' % (newsitem.id),[])))
    response.navigation_helper.insert(0,('Nieuws', False, URL('default','index',[])))
    
response.right_menu_static = []
response.right_menu_form = []
if request.controller=="page" and (request.function=="show" or request.function=="showEditable"):
    try:
        page_id=int(request.args(0))
    except:
        page=db(db.page.url==request.args(0)).select().first() or redirect(error)
        page_id=page.id
    page_items = db(db.page_item.page==page_id).select()
    for page_item in page_items:
        if page_item.tablename=='page_form':
            page_forms=db(db.page_form.id==page_item.record_id).select().first()
            if page_forms.form_type == 'Support':
                requestForm = 'support.load'
                title = 'Vraag support aan'
                response.right_menu_form.append((title, False, URL('page',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Demo':
                requestForm = 'demo.load'
                title = 'Vraag een demo aan' 
                response.right_menu_form.append((title, False, URL('page',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Offers':
                requestForm = 'offers.load'
                title = 'Vraag een offerte aan'     
                response.right_menu_form.append((title, False, URL('page',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Question':
                requestForm = 'question.load'
                title = 'Stel ons een vraag'
                response.right_menu_form.append((title, False, URL('page',requestForm,args=[page_id])))
                """
#    response.right_menu_static.append((T('Contact'), False, URL('contact', 'index', args=[page_id])))
#else:
#    response.right_menu_static.append((T('Contact'), False, URL('contact', 'index')))

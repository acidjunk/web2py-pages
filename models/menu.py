##########################################
## this is the main application menu
## add/remove items as required
##########################################
error=URL(r=request,f='error')

#MAIN MENU
response.menu = []
response.menu += [(T('Welcome'), False, URL('default','index'))]
#response.menu = [(T('Home'), False, URL('default','index'), [])]
pagetree=db((db.pagetree.parent==0) & (db.pagetree.page_language==T.accepted_language) & (db.pagetree.isMenuitem==True)).select(orderby=db.pagetree.order_nr)
for page in pagetree:
    sub_pages=db((db.pagetree.parent==page.id) & (db.pagetree.isMenuitem==True)).select(orderby=db.pagetree.order_nr)
    submenu=[]
    for sub_page in sub_pages:
        submenu.append([sub_page.short_title, False, URL('pagetree','show/%s' % (sub_page.url))])
    response.menu.append((page.short_title, False, URL('pagetree','show/%s' % (page.url)), submenu))   

#TODO: add simple contact module
#response.menu += [(T('Contact'), False, URL('contact','index'))]

if auth.has_membership('admins'):
    response.menu += [(T('Admin'), False, URL('pagetree','adminMenu'))]

#FIRST LEVEL SUBMENUUS AND NAVIGATION HELP
response.right_menu=[]
response.navigation_helper=[]
if request.controller=="pagetree" and (request.function=="show" or request.function=="showEditable"):
    try:
        page_id=int(request.args(0))
        pagetree=db.pagetree[page_id] or redirect(error)
    except:
        pagetree=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        page_id=pagetree.id
    
    if pagetree.childrenTitle: response.right_menu_title=pagetree.childrenTitle
    else: response.right_menu_title=pagetree.short_title
    sub_pages=db(db.pagetree.parent==page_id).select(orderby=db.pagetree.order_nr)
    for sub_page in sub_pages:
        response.right_menu.append((sub_page.short_title, False, URL('pagetree','show/%s' % (sub_page.url),[])))
    # deal with navigation helper
    parent=pagetree.parent
    done=False
    while not done:
        try:
            temp_page=db.pagetree[parent] or redirect(error)
            response.navigation_helper.insert(0,(temp_page.short_title, False, URL('pagetree','show/%s' % (temp_page.url),[])))
            parent=temp_page.parent
        except:
            done=True
    
response.right_menu_static = []
response.right_menu_form = []
if request.controller=="pagetree" and (request.function=="show" or request.function=="showEditable"):
    try:
        page_id=int(request.args(0))
    except:
        pagetree=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        page_id=pagetree.id
    page_items = db(db.page_item.pagetree==page_id).select()
    for page_item in page_items:
        if page_item.tablename=='page_form':
            page_forms=db(db.page_form.id==page_item.record_id).select().first()
            if page_forms.form_type == 'Support':
                requestForm = 'support.load'
                title = T('Request support')
                response.right_menu_form.append((title, False, URL('contact',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Demo':
                requestForm = 'demo.load'
                title = T('Request a demo') 
                response.right_menu_form.append((title, False, URL('contact',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Offers':
                requestForm = 'offers.load'
                title = T('Request an offer')     
                response.right_menu_form.append((title, False, URL('contact',requestForm,args=[page_id])))
            elif page_forms.form_type == 'Question':
                requestForm = 'question.load'
                title = T('Ask a question')
                response.right_menu_form.append((title, False, URL('contact',requestForm,args=[page_id])))

#NO CONTACT MODULE YET                
#    response.right_menu_static.append((T('Contact'), False, URL('contact', 'index', args=[page_id])))
#else:
#    response.right_menu_static.append((T('Contact'), False, URL('contact', 'index')))

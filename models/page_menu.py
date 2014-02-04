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

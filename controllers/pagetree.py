# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

#error handler
error=URL(r=request,f='error')
error_no_text=URL(r=request,f='error_no_text')
error_no_linked_content=URL(r=request,f='error_no_linked_content')

#needed for Picasa
import gdata.photos.service
import gdata.media

def debug():
    return dict(message=BEAUTIFY(request))

@auth.requires_membership('admins')
def index():
    """
    Startplace of pagetree module: lets you make new pages
    """
    auth.settings.registration_requires_approval = True
    maxPage=db((db.pagetree.parent==0) & (db.pagetree.page_language==T.accepted_language)).count()
    form=SQLFORM(db.pagetree)
    form.vars.parent=0
    form.vars.page_language=T.accepted_language
    form.vars.order_nr=maxPage+1
    if form.process().accepted:
        redirect(URL())
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
   
    pages=db(db.pagetree.page_language==T.accepted_language).select()
    return dict(pages=pages, form=form)

@auth.requires_membership('admins')
def manage():
    grid = SQLFORM.smartgrid(db.pagetree, 
                             fields=(db.pagetree.id, db.pagetree.title, db.pagetree.short_title,db.pagetree.url, db.pagetree.isActive), 
                             headers={'pagetree.id':'ID','pagetree.title':'Title','pagetree.short_title':'Short name', 'pagetree.url':'url', 'pagetree.isActive':'Active?'}, 
                             orderby=db.pagetree.order_nr,   
                             searchable=True,  
                             sortable=True,  
                             paginate=30,   
                             deletable=True, 
                             editable=True, 
                             details=True, 
                             selectable=None, 
                             create=True, 
                             csv=True, 
                             #linked_tables=['Category'], 
                             user_signature = True, 
                             #maxtextlengths={'vvb_items.title':30,'vvb_items.summary':75}, 
                             maxtextlength=20, 
                             onvalidation=None, 
                             oncreate=None, 
                             onupdate=None, 
                             ondelete=None, 
                             sorter_icons=('[^]','[v]'),  
                             ui = 'jquery-ui',  
                             showbuttontext=None,  
                             _class="web2py_grid",  
                             formname='web2py_grid')
    return dict(grid=grid)
    
    
@auth.requires_membership('admins')
def deletePageItem():
    try:
        page_id, page_item_id = request.args[:2]
    except:
        redirect(error)
    pagetree=db(db.pagetree.id==page_id).select().first() or redirect(error)
    page_item=db(db.page_item.id==page_item_id).select().first() or redirect(error)
    if page_item.tablename=='page_text':
        del db.page_text[page_item.record_id]
    elif page_item.tablename=='page_image':
        del db.page_image[page_item.record_id]
    elif page_item.tablename=='page_link':
        del db.page_link[page_item.record_id]
    elif page_item.tablename=='page_faq':
        del db.page_faq[page_item.record_id]
    elif page_item.tablename=='page_address':
        del db.page_address[page_item.record_id]
    elif page_item.tablename=='page_file':
        del db.page_file[page_item.record_id]
    elif page_item.tablename=='page_picasa':
        del db.page_picasa[page_item.record_id]
    elif page_item.tablename=='page_youtube':
        del db.page_youtube[page_item.record_id]
    elif page_item.tablename=='page_twitter':
        del db.page_twitter[page_item.record_id]
    elif page_item.tablename=='page_facebook':
        del db.page_facebook[page_item.record_id]
    elif page_item.tablename=='page_slider':
        del db.page_slider[page_item.record_id]
    elif page_item.tablename=='page_form':
        del db.page_form[page_item.record_id]  
    elif page_item.tablename=='page_fbcomments':
        del db.page_fbcomments[page_item.record_id]      
    else: 
        #Unknow delete type!
        redirect(error)
    
    #order numbers again after a delete
    all_page_items = db(db.page_item.pagetree==page_id).select(); 
    deleted_page_item=db(db.page_item.id==page_item_id).select().first() or redirect(error)   
    for page_item in all_page_items:
       if (int(page_item.order_nr) > int(deleted_page_item.order_nr)):
           orderNr = int(page_item.order_nr)-1          
           db((db.page_item.id == page_item.id) & (db.page_item.pagetree==page_id)).update(order_nr = orderNr)
         
    #delete the page_item  
    del db.page_item[page_item_id]
    redirect(URL('showEditable/%s' % page_id))

def makeThumbnail(dbtable,ImageID,size=(134,134)):
    try:    
        thisImage=db(dbtable.id==ImageID).select()[0]
        import os, uuid
        from PIL import Image
    except: return
    im=Image.open(request.folder + 'uploads/' + thisImage.image)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='pagetree.imageThumb.%s.png' % (uuid.uuid4())
    im.save(request.folder + 'static/images/thumbs/' + thumbName,'png', optimize=True)
    thisImage.update_record(imageThumb=thumbName)
    return 

@auth.requires_membership('admins')
def sortOrderNr():
    try:
        #ophalen args
        page_id, page_item_id, new_sort_var = request.args[:3]
        #cast naar int zzzzz
        page_id=int(page_id)
        page_item_id=int(page_item_id)
        order_nr_new=int(new_sort_var)        
    except:
        redirect(error)   

    page_item1=db(db.page_item.id==page_item_id).select().first() or redirect(error)
    order_nr_old=page_item1.order_nr
    
    
    if(order_nr_new > order_nr_old):
        #move down        
        #deal with changing numbers
        updateOrderNrs = db((db.page_item.order_nr > order_nr_old) & (db.page_item.order_nr <= order_nr_new) & (db.page_item.pagetree==page_id)).select(orderby=db.page_item.order_nr)        
        #set order to 0 for moving content
        db((db.page_item.order_nr == order_nr_old) & (db.page_item.pagetree==page_id)).update(order_nr = 0)
        #tempNr for changing order_nr
        tempNr = int(order_nr_old)
        for page_item in updateOrderNrs:
            db(db.page_item.id == page_item.id).update(order_nr = tempNr)
            tempNr += 1
        #assign correct value to changed record
        db((db.page_item.order_nr == 0) & (db.page_item.pagetree==page_id)).update(order_nr = order_nr_new)
        message = 'moved down'
    else:
        #move up        
        #deal with changing numbers
        updateOrderNrs = db((db.page_item.order_nr < order_nr_old) & (db.page_item.order_nr >= order_nr_new) & (db.page_item.pagetree==page_id)).select(orderby=db.page_item.order_nr)        
        #set order to 0 for moving content
        db((db.page_item.order_nr == order_nr_old) & (db.page_item.pagetree==page_id)).update(order_nr = 0)
        #tempNr for changing order_nr
        tempNr = int(order_nr_new) + 1
        for page_item in updateOrderNrs:
            db(db.page_item.id == page_item.id).update(order_nr = tempNr)
            tempNr += 1
        #assign correct value to changed record
        db((db.page_item.order_nr == 0) & (db.page_item.pagetree==page_id)).update(order_nr = order_nr_new)
        message = 'moved up'
    
    redirect(URL('showEditable/%s' % page_id))
    
@auth.requires_membership('admins')
def resetOrderNr():
    try:
        page_id=int(request.args(0))     
    except:
        redirect(error)
    for i in range (1,6):
        db((db.page_item.id == i) & (db.page_item.pagetree==page_id)).update(order_nr = i)
    message = 'reset'
    redirect(URL('showEditable/%s' % page_id))
    return dict(message=message)

@auth.requires_membership('admins')
def editMarkmin():
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item,formstyle='table2cols')
    else: form=SQLFORM(db.page_text,formstyle='table2cols')
    form.vars.text_type='markmin'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('text'))

@auth.requires_membership('admins')
def editHtml():
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item,formstyle='table2cols')
    else: form=SQLFORM(db.page_text,formstyle='table2cols')
    form.vars.text_type='html'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('text'))

@auth.requires_membership('admins')
def edit():
    """Implements editing of pagetree title and url"""
    dbtable = db.pagetree          #uploads table name
    page_id=int(request.args(0))
    pagetree=db.pagetree[page_id] or redirect(error)
    form=SQLFORM(db.pagetree,pagetree)
    if form.process().accepted:
        if form.vars.image: makeThumbnail(dbtable,form.vars.id,(134,134)) #Thumbnail not used in this project
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('Editing the pagetree itself'))

@auth.requires_membership('admins')
def editText():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item)
    else: form=SQLFORM(db.page_text)
    form.vars.text_type='textarea'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('Plain text'))

@auth.requires_membership('admins')
def editLink():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_link[item_id] or redirect(error)
        form=SQLFORM(db.page_link,item)
    else: form=SQLFORM(db.page_link)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_link).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_link',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('link'))

@auth.requires_membership('admins')
def editFAQ():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_faq[item_id] or redirect(error)
        form=SQLFORM(db.page_faq,item)
    else: form=SQLFORM(db.page_faq)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_faq).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_faq',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('faq'))

@auth.requires_membership('admins')
def editAddress():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_address[item_id] or redirect(error)
        form=SQLFORM(db.page_address,item)
    else: form=SQLFORM(db.page_address)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_address).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_address',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('address'))

@auth.requires_membership('admins')
def editImage():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_image[item_id] or redirect(error)
        form=SQLFORM(db.page_image,item)
    else: form=SQLFORM(db.page_image)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_image).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_image',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('image'))

def editForm():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_form[item_id] or redirect(error)
        form=SQLFORM(db.page_form,item)
    else: form=SQLFORM(db.page_form)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_form).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_form',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('form'))

@auth.requires_membership('admins')
def editFile():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_file[item_id] or redirect(error)
        form=SQLFORM(db.page_file,item)
    else: form=SQLFORM(db.page_file)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_file).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_file',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('file'))

@auth.requires_membership('admins')
def editPicasa():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_picasa[item_id] or redirect(error)
        form=SQLFORM(db.page_picasa,item)
    else: form=SQLFORM(db.page_picasa)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_picasa).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_picasa',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('picasa'))

@auth.requires_membership('admins')
def editYoutube():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_youtube[item_id] or redirect(error)
        form=SQLFORM(db.page_youtube,item)
    else: form=SQLFORM(db.page_youtube)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_youtube).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_youtube',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('youtube'))

@auth.requires_membership('admins')
def editFacebook():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_facebook[item_id] or redirect(error)
        form=SQLFORM(db.page_facebook,item)
    else: form=SQLFORM(db.page_facebook)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_facebook).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_facebook',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('facebook'))

@auth.requires_membership('admins')
def editTwitter():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_twitter[item_id] or redirect(error)
        form=SQLFORM(db.page_twitter,item)
    else: form=SQLFORM(db.page_twitter)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_twitter).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_twitter',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('twitter'))

@auth.requires_membership('admins')
def editSlider():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_slider[item_id] or redirect(error)
        form=SQLFORM(db.page_slider,item)
    else: form=SQLFORM(db.page_slider)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_slider).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_slider',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('slider'))

@auth.requires_membership('admins')
def editFBComments():
    response.view='pagetree/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    pagetree=db.pagetree[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_fbcomments[item_id] or redirect(error)
        form=SQLFORM(db.page_fbcomments,item)
    else: form=SQLFORM(db.page_fbcomments)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_fbcomments).select().last()
            maxPageItem=db(db.page_item.pagetree==page_id).count()
            db.page_item.insert(pagetree=page_id,record_id=last.id,tablename='page_fbcomments',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, pagetree=pagetree, subtitle=T('fbcomments'))

@auth.requires_membership('admins')
def movePage():
    #request 1 should be ID or URL_name
    
    if request.args(1):
        #request 2 should be new parent
        page_id=request.args(0)
        page_parent=request.args(1)
        my_page=db(db.pagetree.id==page_id).select().first() or redirect(error)
        my_url=my_page.url
        new_parent=db(db.pagetree.id==page_parent).select().first()
        if new_parent: new_parent=new_parent.id
        else: new_parent=0

        tempNr = int(my_page.order_nr)
        updateOrderNrs = db((db.pagetree.parent==my_page.parent) & (db.pagetree.order_nr > my_page.order_nr)).select(orderby=db.pagetree.order_nr)
        db(db.pagetree.id==my_page.id).update(order_nr = 0)
        for pagetree in updateOrderNrs:
            db(db.pagetree.id == pagetree.id).update(order_nr = tempNr)
            tempNr += 1
        
        highestOrderNr=db(db.pagetree.parent==new_parent).select(orderby=db.pagetree.order_nr).last()
        if highestOrderNr: highestOrderNr=int(highestOrderNr.order_nr + 1)
        else: highestOrderNr=1
        
        row = db(db.pagetree.id == page_id).select().first()
        row.update_record(parent=page_parent, order_nr=highestOrderNr)
                
        redirect(URL('show',args=(my_url)))
   
    try:
        page_id=int(request.args(0))
        my_page=db.pagetree[page_id] or redirect(error)
    except:
        my_page=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        page_id=pagetree.id
        
    pages=db(db.pagetree).select(orderby=db.pagetree.parent) or redirect(error)
    return dict(my_page=my_page, pages=pages)

@auth.requires_membership('admins')
def searchForChilds(pId,pSet):
    result = []
    for p in pSet:
        if p.parent == pId:
            result.append(p)
    return result

@auth.requires_membership('admins')            
def sortPages():
    if request.args(0) == '0':
        pageId = 0
        pagetree = db(db.pagetree.parent == 0).select().first()
    else:
        pageId = int(request.args(0)) or 'error can\'t cast id to int'
        pagetree = db(db.pagetree.id == pageId).select().first()
    pages = db(db.pagetree).select()
    pMap = []
    searchIds = []
    
    result = searchForChilds(pageId,pages)
    if not result == []:
        pMap.append([pagetree,result])
        for r in result: searchIds.append(r.id)
    
    if not result == [] and (pageId != 0):
        again = True
        while again:
            again = False
            loopList = searchIds
            searchIds = []
            for i in range(0,len(loopList)-1):
                r = loopList[i]
                result = searchForChilds(r,pages)
                if not result == []:
                    rPage = db(db.pagetree.id == r).select().first()
                    pMap.append([rPage,result])
                    for r in result: searchIds.append(r.id)
                    again = True

    for pM in pMap:
        pM[1] = sorted(pM[1], key=lambda pagetree: pagetree.order_nr)   
       
    return dict(pMap=pMap,root=pageId) 


@auth.requires_membership('admins')            
def sortTopPages():
    response.view='pagetree/sortPages.html'
    toppages = db(db.pagetree.parent == 0).select()
    pages = db(db.pagetree).select()
    pMap = []
    searchIds = []
    pageId=0
    result = searchForChilds(pageId,pages)
    if not result == []:
        pMap.append([pagetree,result])
        for r in result: searchIds.append(r.id)

    for pM in pMap:
        pM[1] = sorted(pM[1], key=lambda pagetree: pagetree.order_nr)   
       
    return dict(pMap=pMap,root=pageId) 


@auth.requires_membership('admins')
def changePageOrder():
    try:
        page_id = int(request.args[0])
        order_nr_new = int(request.args[1])   
        currentPage = int(request.args[2])     
    except:
        redirect(error)   

    curr = db(db.pagetree.id==page_id).select().first() or redirect(error)
    order_nr_old=curr.order_nr

    if(order_nr_new > order_nr_old):
        updateOrderNrs = db((db.pagetree.order_nr > order_nr_old) & (db.pagetree.order_nr <= order_nr_new) & (db.pagetree.parent==curr.parent)).select(orderby=db.pagetree.order_nr)        
        db((db.pagetree.order_nr == order_nr_old) & (db.pagetree.parent==curr.parent)).update(order_nr = 0)
        tempNr = int(order_nr_old)
        for p in updateOrderNrs:
            db(db.pagetree.id == p.id).update(order_nr = tempNr)
            tempNr += 1
        db((db.pagetree.order_nr == 0) & (db.pagetree.parent==curr.parent)).update(order_nr = order_nr_new)
    else:
        updateOrderNrs = db((db.pagetree.order_nr < order_nr_old) & (db.pagetree.order_nr >= order_nr_new) & (db.pagetree.parent==curr.parent)).select(orderby=db.pagetree.order_nr)        
        db((db.pagetree.order_nr == order_nr_old) & (db.pagetree.parent==curr.parent)).update(order_nr = 0)
        tempNr = int(order_nr_new) + 1
        for p in updateOrderNrs:
            db(db.pagetree.id == p.id).update(order_nr = tempNr)
            tempNr += 1
        db((db.pagetree.order_nr == 0) & (db.pagetree.parent==curr.parent)).update(order_nr = order_nr_new)
    
    redirect(URL('sortPages/%s' % currentPage))

@auth.requires_membership('admins')
def resetPageOrder():
    parents = db().select(db.pagetree.parent,distinct=True)
    for p in parents:
        childs = db(db.pagetree.parent == p.parent).select()
        counter = 1
        for c in childs:
            db(db.pagetree.id == c.id).update(order_nr = counter)
            counter += 1

def showPicasa():
    gd_photo_client = gdata.photos.service.PhotosService()
    #id = request.args(0) or 'error'
    userID=request.args(0) or 'error'
    albumID=request.args(1) or 'error'
    if userID and albumID:
        try:
            photos = gd_photo_client.GetFeed('/data/feed/base/user/%s/albumid/%s?kind=photo' % (userID, albumID))
        except:
            redirect(error_no_linked_content)
    return dict(photos=photos.entry)
 
#@cache(request.env.path_info, time_expire=1, cache_model=cache.ram)     
def show():
    #TODO: Remove next 2 lines?
    #import time
    #t = time.ctime()
    
    #request 1 should be ID or URL_name
    try:
        page_id=int(request.args(0))
        pagetree=db.pagetree[page_id] or redirect(error)
    except:
        pagetree=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        page_id=pagetree.id
    if pagetree.randomOrdered: page_children=db(db.pagetree.parent==page_id).select(orderby='<random>')   
    else: page_children=db(db.pagetree.parent==page_id).select(orderby=db.pagetree.order_nr)  
    page_items = db(db.page_item.pagetree==pagetree.id).select(orderby=db.page_item.order_nr)

    is_admin=auth.has_membership('admins')

    content=[]
    for page_item in page_items:
        if page_item.tablename=='page_text':
            temp=db.page_text[page_item.record_id] or redirect(error_no_text)
            content.append(temp)
        elif page_item.tablename=='page_image':
            temp=db.page_image[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_link':
            temp=db.page_link[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_faq':
            temp=db.page_faq[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)   
        elif page_item.tablename=='page_address':
            temp=db.page_address[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)  
        elif page_item.tablename=='page_file':
            temp=db.page_file[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_form':
            temp=db.page_form[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_picasa':
            temp=db.page_picasa[page_item.record_id] or redirect(error_no_linked_content)
            gd_photo_client = gdata.photos.service.PhotosService()
            #id = request.args(0) or 'error'
            userID=temp.userid
            albumID=temp.albumid
            if userID and albumID:
                try:
                    photos = gd_photo_client.GetFeed('/data/feed/base/user/%s/albumid/%s?kind=photo' % (userID, albumID))
                    content.append(photos.entry)
                except:
                    redirect(error_no_linked_content)
        elif page_item.tablename=='page_youtube':
            temp=db.page_youtube[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_facebook':
            temp=db.page_facebook[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_twitter':
            temp=db.page_twitter[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_slider':
            temp=db.page_slider[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_fbcomments':
            temp=db.page_fbcomments[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
    return dict(page=pagetree, page_items=page_items, content=content, page_children=page_children, is_admin=is_admin)

@auth.requires_membership('admins')
def showEditable():
    #request 1 should be ID or URL_name
    try:
        page_id=int(request.args(0))
        pagetree=db.pagetree[page_id] or redirect(error)
    except:
        pagetree=db(db.pagetree.url==request.args(0)).select().first() or redirect(error)
        page_id=pagetree.id
    page_children=db(db.pagetree.parent==page_id).select(orderby=db.pagetree.order_nr)   
    form=SQLFORM.factory(db.pagetree)
    if form.accepts(request.vars):
        dbtable = db.pagetree
        #makeThumbnail(dbtable,form.vars.id,(134,134))
        form.vars.parent=page_id
        maxPage=db(db.pagetree.parent==pagetree.parent).count()
        form.vars.order_nr=maxPage+1
        form.vars.language=T.accepted_language
        db.pagetree.insert(**db.pagetree._filter_fields(form.vars))
        redirect(URL('showEditable/%s' % page_id))
    page_items = db(db.page_item.pagetree==pagetree.id).select(orderby=db.page_item.order_nr)
    content=[]
    for page_item in page_items:
        if page_item.tablename=='page_text':
            temp=db.page_text[page_item.record_id] or redirect(error_no_text)
            content.append(temp)
        elif page_item.tablename=='page_image':
            temp=db.page_image[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_link':
            temp=db.page_link[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_faq':
            temp=db.page_faq[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp) 
        elif page_item.tablename=='page_address':
            temp=db.page_address[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp) 
        elif page_item.tablename=='page_file':
            temp=db.page_file[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_picasa':
            temp=db.page_picasa[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_youtube':
            temp=db.page_youtube[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_facebook':
            temp=db.page_facebook[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_twitter':
            temp=db.page_twitter[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_slider':
            temp=db.page_slider[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_form':
            temp=db.page_form[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_fbcomments':
            temp=db.page_fbcomments[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)      
                                 
    return dict(page=pagetree, page_items=page_items, page_children=page_children, content=content, form=form, is_admin=is_admin)

def getAlbums():
    userID= request.args(0)
    lstAlbums = []
    if userID:
        try:
            albums = gd_photo_client.GetUserFeed(user=userID)
            for album in albums.entry:
                entry=A(IMG(_src=album.media.thumbnail[0].url, _alt=album.title.text), _href=URL('getPhotos/%s/%s' % (userID, album.gphoto_id.text))) 
                lstAlbums.append(entry)
        except:
            redirect(URL('index'))
    else:
        redirect(URL('index'))
    return dict(lstAlbums=DIV(*[lstAlbums]))

def getPhotos():
    userID=request.args(0)
    albumID=request.args(1)
    lstPhotos =[]
    if userID and albumID:
        try:
            photos = gd_photo_client.GetFeed('/data/feed/base/user/%s/albumid/%s?kind=photo' % (userID, albumID))
            for photo in photos.entry:
                entry=A(IMG(_src=photo.media.content[0].url, _alt=photo.title.text, _width='320', _height='258')) 
                lstPhotos.append(entry)
        except:
            redirect(URL('index'))
    else:
        redirect(URL('index'))
    return dict(lstPhotos=DIV(*[lstPhotos]))

def copyPage():
    pageToCopy = request.args(0)
    pagetree = db(db.pagetree.id == pageToCopy).select().first()
    pageItems = db(db.page_item.pagetree == pageToCopy).select()
    
    dictInsert = {}
    #---Parse pagetree---
    for key, value in pagetree.iteritems():
        if not (key == 'update_record') | (key == 'page_item') | (key == 'page_archive') | (key == 'delete_record'):
            dictInsert[key] = value
    dictInsert['title'] = 'COPY_%s' % dictInsert['title']
    dictInsert['url'] = 'copy-%s' % dictInsert['url']
    dictInsert['order_nr'] = db(db.pagetree.parent==dictInsert['parent']).select(db.pagetree.order_nr.max()).first()[db.pagetree.order_nr.max()] + 1
    dictInsert['id'] = db(db.pagetree).select(db.pagetree.id.max()).first()[db.pagetree.id.max()] + 1
    insertedPageId = db.pagetree.bulk_insert([dictInsert])[0]
    
    #---Parse Page_items---
    for dict in pageItems:
        dictInsert = {}
        for key, value in dict.iteritems():
            if not (key == 'update_record') | (key == 'delete_record'):
                dictInsert[key] = value
        if not len(dictInsert) == 0:
            dictInsert['id'] = db(db.page_item).select(db.page_item.id.max()).first()[db.page_item.id.max()] + 1
            dictInsert['pagetree'] = insertedPageId
            dictInsert['record_id'] = copyContent(dictInsert['tablename'],dictInsert['record_id'])
            db.page_item.bulk_insert([dictInsert])
            
    redirect(URL('index'))
    return dict()

def copyContent(tbName,id):
    content = db(db[tbName].id == id).select().first()

    dictInsert = {}
    for key,value in content.iteritems():    
        if not (key == 'page_text_archive') | (key == 'update_record') | (key == 'delete_record'):         
            dictInsert[key] = value
    dictInsert['id'] = db(db[tbName]).select(db[tbName].id.max()).first()[db[tbName].id.max()] + 1
    insertedContentId = db[tbName].bulk_insert([dictInsert])[0]

    return insertedContentId

def showSearch():
    #TODO: clean up _style= construct
    result=None
    message=SPAN(T('Perform a quick search in the info part of the site'))
    form=FORM(INPUT(_name='name', _style="width:135px;", requires=IS_LENGTH(maxsize=20, minsize=3)),
              INPUT(_type='submit', _value=T('Search')))
    if form.accepts(request,session):
        #Trigger the redirect to search pagetree
        result=True
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form, message=message, result=result)

# If you don't have an admin; Create a admin user in code... some where in one of your default controller
# TODO: write code that makes first user a member of admins group??
@auth.requires_membership('admins')
def adminPanel():
    form1=SQLFORM(db.auth_membership)
    if form1.process().accepted:
        redirect(URL())
    elif form1.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    form2=SQLFORM(db.auth_group)
    if form2.process().accepted:
        redirect(URL())
    elif form2.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    allGroups=db(db.auth_group).select()
    allMemberships=db(db.auth_membership).select()
    return dict(form1=form1,form2=form2,allGroups=allGroups,allMemberships=allMemberships)

@auth.requires_membership('admins')
def adminMenu():
    return dict(title='Administrator Quickmenu')

#def tags():
#    response.view='tags/tags.load'
#    import re
#    db_tag = db.tag
#    tagged = db(db.tag_link.id>0).select()
#    #nodetagged = db(~db.tag.name.belongs(db(db.package_tag)._select(db.package_tag.name))).select(orderby=db.tag.name)
#    db_link = db.tag_link
#    table_name=request.args(0)
#    record_id=request.args(1)
#    if not auth.user_id:
#        return ''
#    form = SQLFORM.factory(Field('tag_name',requires=IS_SLUG()))
#    if request.vars.tag_db:
#        request.vars.tag_name = request.vars.tag_db
#    if request.vars.tag_name:
#        for item in request.vars.tag_name.split(','):
#            tag_name = re.compile('\s+').sub(' ',item).strip()
#            tag_exists = tag = db(db_tag.name==tag_name).select().first()
#            if not tag_exists:
#                tag = db_tag.insert(name=tag_name, links=1)
#            link = db(db_link.tag==tag.id)\
#                (db_link.table_name==table_name)\
#                (db_link.record_id==record_id).select().first()
#            if not link:
#                db_link.insert(tag=tag.id,
#                               table_name=table_name,record_id=record_id)
#                if tag_exists:
#                    tag.update_record(links=tag.links+1)
#    for key in request.vars:
#        if key[:6]=='delete':
#            link_id=key[6:]
#            link=db_link[link_id]
#            del db_link[link_id]
#            db_tag[link.tag] = dict(links=db_tag[link.tag].links-1)
#    links = db(db_link.table_name==table_name)\
#              (db_link.record_id==record_id).select()\
#              .sort(lambda row: row.tag.name.upper())
#    #return dict(tagged=tagged, nodetagged=nodetagged, links=links, form=form)
#    return dict(tagged=tagged,links=links,form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

@auth.requires_membership('admins')
def export():
    db.export_to_csv_file(open('somefile.csv', 'wb'))

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
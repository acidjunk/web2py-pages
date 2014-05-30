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

def error():
    redirect(URL('default', 'index'))


def index():
    """
    Start page of page module: lets you make new pages
    """
    auth.settings.registration_requires_approval = True
    maxPage=db((db.page.parent==0) & (db.page.language==T.accepted_language)).count()
    form=SQLFORM(db.page)
    form.vars.parent=0
    form.vars.language=T.accepted_language
    form.vars.order_nr=maxPage+1
    if form.process().accepted:
        redirect(URL())
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
   
    pages=db(db.page.id>0).select()
    return dict(pages=pages, form=form)

@auth.requires_membership('admins')
def test_page():
    import uuid
    title='Add new page with page items. Please upload an image.'
    form = SQLFORM.factory(Field('image', 'upload', requires=IS_NOT_EMPTY(), uploadfolder=os.path.join(request.folder,'uploads')), table_name='test_page')
    if form.process().accepted:
        request.vars.image.file.seek(0)
        maxPage=db((db.page.parent==0) & (db.page.language==T.accepted_language)).count()
        
        #ADD PAGE
        page = db.page.insert(language=T.accepted_language,
                              parent=0,
                              title='Test page for testing Page Module',
                              short_title='Test page',
                              url='test-page-%s' % (uuid.uuid4()),
                              summary_title='Test summery title',
                              summary='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus a vehicula turpis, sodales semper nisi. Sed egestas eros id urna condimentum pharetra. Donec et dolor sed urna posuere porttitor. Fusce at felis nec tellus tempor lobortis. Sed eleifend magna quis sodales dignissim. Mauris quis vulputate lacus.',
                              order_nr=maxPage+1)
        
        #ADD PAGE TEXT
        page_text = db.page_text.insert(title='Page Text Test HTML',
                                        type='html',
                                        body="""
                                        <div id="lipsum">
                                            <h1>This is a H1 title</h1>
                                            <h2>This is a H2 title</h2>
                                            <h3>This is a H3 title</h3>
                                            <h4>This is a H4 title</h4>
                                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus a vehicula turpis, sodales semper nisi. Sed egestas eros id urna condimentum pharetra. Donec et dolor sed urna posuere porttitor. Fusce at felis nec tellus tempor lobortis. Sed eleifend magna quis sodales dignissim. Mauris quis vulputate lacus. Donec non ante tincidunt, suscipit nibh nec, feugiat lorem. Suspendisse blandit posuere metus non condimentum. Donec velit nibh, cursus sit amet lectus vitae, hendrerit lacinia magna. Sed tristique dolor et dolor venenatis, et venenatis orci lacinia. Ut a laoreet lacus, nec laoreet ligula. Sed malesuada ligula risus, id bibendum nibh adipiscing eget. Integer eleifend fermentum erat quis ornare.</p>
                                            <p>Quisque sodales, ipsum non interdum vehicula, nunc eros suscipit est, ac dapibus augue tellus et sem. Ut laoreet porta dolor. Donec facilisis, odio id porttitor imperdiet, lectus lacus viverra magna, a varius est sem vitae dui. Phasellus aliquet elit vel purus commodo, eget ullamcorper tellus accumsan. Proin non condimentum sapien. Nulla sed hendrerit nibh. Duis vel erat sollicitudin, ornare nibh quis, dignissim arcu. Praesent fringilla, dolor vel tincidunt interdum, nisi purus tristique velit, sed semper lorem tortor eu justo. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec ligula nibh, volutpat et ipsum vitae, luctus adipiscing nisi. Donec fringilla, enim ac egestas fermentum, augue purus suscipit arcu, vitae congue diam ante at justo.</p>
                                            <p>Vestibulum mattis sed felis vitae consequat. Aenean egestas, erat et malesuada fermentum, dolor eros sollicitudin elit, eget consequat felis turpis iaculis libero. Duis eros est, tincidunt nec aliquam at, tempus ac diam. Aliquam porttitor mi et turpis porttitor eleifend. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur adipiscing risus id rutrum volutpat. Praesent mollis odio eget metus auctor molestie. In quam eros, posuere non sem in, imperdiet porta mi. Etiam bibendum, libero ac consequat condimentum, sem dolor cursus ante, nec varius nunc sem eu orci. Suspendisse libero ante, egestas vel neque vel, ultrices dapibus dui. Donec sollicitudin ipsum libero, nec euismod nisl faucibus quis. Praesent accumsan venenatis gravida. Pellentesque interdum vel massa sit amet lobortis. Maecenas pulvinar, purus quis malesuada laoreet, nunc libero volutpat justo, at luctus sem velit non neque.</p>
                                            <p>Mauris aliquam erat a commodo placerat. Praesent eget odio mauris. Nunc luctus nibh facilisis ante dignissim, quis auctor felis commodo. Nunc vel lacinia velit. Nulla facilisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Suspendisse metus odio, adipiscing vel sapien id, iaculis facilisis leo. Vivamus sit amet erat eros.</p>
                                            <ul>
                                            <li>Een</li>
                                            <li>Twee</li>
                                            <li>Drie</li>
                                            <li>Vier
                                                <ul>
                                                    <li>Een</li>
                                                    <li>Twee</li>
                                                    <li>Drie</li>
                                                </ul>
                                            </li>
                                            <li>Vijf</li>
                                            <li>Zes</li>
                                            <li>Zeven</li>
                                            <li>Acht</li>
                                            </ul>
                                            <p>Etiam mollis, risus vitae ultrices feugiat, quam urna convallis mauris, quis sodales lectus tortor id mi. Sed quis nibh ac ipsum scelerisque interdum. Curabitur blandit at velit sed suscipit. Praesent vehicula nulla libero, interdum faucibus libero tempus non. Fusce viverra scelerisque mi, sed vehicula nisi porttitor quis. Nullam in aliquam ipsum. In hac habitasse platea dictumst. Aenean mattis posuere tempor. Aliquam interdum adipiscing elit, ac varius neque feugiat ac. Morbi fermentum, ligula ut laoreet commodo, sem erat feugiat mi, non posuere mauris neque at est. Phasellus quis accumsan felis. Morbi vitae lobortis mi, quis congue augue.</p>
                                        </div>""")
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_text.id,tablename='page_text',order_nr=maxPageItem+1)
        
        #ADD PAGE IMAGE
        page_image = db.page_image.insert(title='Page Image Test', image=db.page_image.image.store(request.vars.image.file,request.vars.image.filename))
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_image.id,tablename='page_image',order_nr=maxPageItem+1)
        request.vars.image.file.seek(0)
        
        #ADD PAGE FILE
        page_file = db.page_file.insert(title='Page File Test', file=db.page_file.file.store(request.vars.image.file,request.vars.image.filename))
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_file.id,tablename='page_file',order_nr=maxPageItem+1)
        request.vars.image.file.seek(0)
        
        #ADD PAGE PICASA
        page_picasa = db.page_picasa.insert(userid='113197574843599669846', albumid='5686684644215662097')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_picasa.id,tablename='page_picasa',order_nr=maxPageItem+1)
        
        #ADD PAGE YOUTUBE
        page_youtube = db.page_youtube.insert(title='Page Youtube Test', youtube='EDoylhFo8xY')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_youtube.id,tablename='page_youtube',order_nr=maxPageItem+1)
        
        #ADD PAGE FACEBOOK
        page_facebook = db.page_facebook.insert(facebook='https://www.facebook.com/formatics.nl?fref=ts')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_facebook.id,tablename='page_facebook',order_nr=maxPageItem+1)
        
        
        #ADD PAGE LINK
        page_link = db.page_link.insert(title='Page link Test', link='http://www.formatics.nl')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_link.id,tablename='page_link',order_nr=maxPageItem+1)
        
        #ADD PAGE FAQ
        page_faq = db.page_faq.insert(question='Lorem ipsum dolor?', answer='Vivamus a vehicula turpis, sodales semper nisi. Sed egestas eros id urna condimentum pharetra. Donec et dolor sed urna posuere porttitor. Fusce at felis nec tellus tempor lobortis.')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_faq.id,tablename='page_faq',order_nr=maxPageItem+1)
        
        #ADD PAGE DEALER
        page_dealer = db.page_dealer.insert(name='Dealer Name',
                                            address='Julinalastraat 63',
                                            postcode='6039 AH',
                                            location='Stramproy',
                                            website='http://www.formatics.nl',
                                            email='info@formatics.nl',
                                            phone='0495 820 222')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_dealer.id,tablename='page_dealer',order_nr=maxPageItem+1)
        
        #ADD PAGE SLIDER
        sliderID = db.page_slider.insert(width='600',
                                            height='400',
                                            image1=db.page_slider.image1.store(request.vars.image.file,request.vars.image.filename),
                                            link1='http://www.google.nl',
                                            caption1='Een testlink naar Google')

        page_slider = db(db.page_slider.id == sliderID).select().first()

        request.vars.image.file.seek(0)
        page_slider.update_record(image2=db.page_slider.image2.store(request.vars.image.file,request.vars.image.filename),
                          link2='http://www.google.nl',
                          caption2='Een testlink naar Google 2')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image3=db.page_slider.image3.store(request.vars.image.file,request.vars.image.filename),
                          link3='http://www.google.nl',
                          caption3='Een testlink naar Google 3')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image4=db.page_slider.image4.store(request.vars.image.file,request.vars.image.filename),
                          link4='http://www.google.nl',
                          caption4='Een testlink naar Google 4')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image5=db.page_slider.image5.store(request.vars.image.file,request.vars.image.filename),
                          link5='http://www.google.nl',
                          caption5='Een testlink naar Google 5')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image6=db.page_slider.image6.store(request.vars.image.file,request.vars.image.filename),
                          link6='http://www.google.nl',
                          caption6='Een testlink naar Google 6')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image7=db.page_slider.image7.store(request.vars.image.file,request.vars.image.filename),
                          link7='http://www.google.nl',
                          caption7='Een testlink naar Google 7')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image8=db.page_slider.image8.store(request.vars.image.file,request.vars.image.filename),
                          link8='http://www.google.nl',
                          caption8='Een testlink naar Google 8')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image9=db.page_slider.image9.store(request.vars.image.file,request.vars.image.filename),
                          link9='http://www.google.nl',
                          caption9='Een testlink naar Google 9')
        
        request.vars.image.file.seek(0)
        page_slider.update_record(image10=db.page_slider.image10.store(request.vars.image.file,request.vars.image.filename),
                          link10='http://www.google.nl',
                          caption10='Een testlink naar Google 10')                           
                                 
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_slider.id,tablename='page_slider',order_nr=maxPageItem+1)
        request.vars.image.file.seek(0)
        
        #ADD PAGE FORM
        page_form = db.page_form.insert(form_type='Contactpage')
        maxPageItem=db(db.page_item.page==page.id).count()
        db.page_item.insert(page=page.id,record_id=page_form.id,tablename='page_form',order_nr=maxPageItem+1)
        redirect(URL('page', 'show', args=page.url))
    return dict(title=title, form=form)

@auth.requires_membership('admins')
def manage():
    grid = SQLFORM.smartgrid(db.page, 
                             fields=(db.page.id, db.page.title, db.page.short_title,db.page.url, db.page.isActive), 
                             headers={'page.id':'ID','page.title':'Titel','page.short_title':'Korte naam', 'page.url':'url', 'page.isActive':'Is actief'}, 
                             orderby=db.page.order_nr,   
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
def delPage():
    page_id = request.args(0)

    page_item=db(db.page_item.page==page_id).select() or redirect(error)

    # Delete page items first!
    for page_item in page_item:
        if page_item.tablename=='page_text':
            del db.page_text[page_item.record_id]
        elif page_item.tablename=='page_image':
            del db.page_image[page_item.record_id]
        elif page_item.tablename=='page_link':
            del db.page_link[page_item.record_id]
        elif page_item.tablename=='page_faq':
            del db.page_faq[page_item.record_id]
        elif page_item.tablename=='page_dealer':
            del db.page_dealer[page_item.record_id]
        elif page_item.tablename=='page_file':
            del db.page_file[page_item.record_id]
        elif page_item.tablename=='page_picasa':
            del db.page_picasa[page_item.record_id]
        elif page_item.tablename=='page_youtube':
            del db.page_youtube[page_item.record_id]
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

    #Delete page
    del db.page[page_id]

    redirect(URL('page', 'manage'))

@auth.requires_membership('admins')
def deletePageItem():
    try:
        page_id, page_item_id = request.args[:2]
    except:
        redirect(error)
    page=db(db.page.id==page_id).select().first() or redirect(error)
    page_item=db(db.page_item.id==page_item_id).select().first() or redirect(error)
    if page_item.tablename=='page_text':
        del db.page_text[page_item.record_id]
    elif page_item.tablename=='page_image':
        del db.page_image[page_item.record_id]
    elif page_item.tablename=='page_link':
        del db.page_link[page_item.record_id]
    elif page_item.tablename=='page_faq':
        del db.page_faq[page_item.record_id]
    elif page_item.tablename=='page_dealer':
        del db.page_dealer[page_item.record_id]
    elif page_item.tablename=='page_file':
        del db.page_file[page_item.record_id]
    elif page_item.tablename=='page_picasa':
        del db.page_picasa[page_item.record_id]
    elif page_item.tablename=='page_youtube':
        del db.page_youtube[page_item.record_id]
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
    
    #order nummers fatsoenlijk zetten na een delete
    all_page_items = db(db.page_item.page==page_id).select(); 
    deleted_page_item=db(db.page_item.id==page_item_id).select().first() or redirect(error)   
    for page_item in all_page_items:
       if (int(page_item.order_nr) > int(deleted_page_item.order_nr)):
           orderNr = int(page_item.order_nr)-1          
           db((db.page_item.id == page_item.id) & (db.page_item.page==page_id)).update(order_nr = orderNr)
         
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
    thumbName='page.imageThumb.%s.png' % (uuid.uuid4())
    im.save(request.folder + 'static/page/images/thumbs/' + thumbName,'png', optimize=True)
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
        #regel alle nummers die moeten veranderen
        updateOrderNrs = db((db.page_item.order_nr > order_nr_old) & (db.page_item.order_nr <= order_nr_new) & (db.page_item.page==page_id)).select(orderby=db.page_item.order_nr)        
        #zet het order_nr dat verplaatst wordt op 0
        db((db.page_item.order_nr == order_nr_old) & (db.page_item.page==page_id)).update(order_nr = 0)
        #tempNr voor het toewijzen aan order_nr
        tempNr = int(order_nr_old)
        for page_item in updateOrderNrs:
            db(db.page_item.id == page_item.id).update(order_nr = tempNr)
            tempNr += 1
        #geef het verschoven record de juiste waarde
        db((db.page_item.order_nr == 0) & (db.page_item.page==page_id)).update(order_nr = order_nr_new)
        message = 'moved down'
    else:
        #move up        
        #regel alle nummers die moeten veranderen
        updateOrderNrs = db((db.page_item.order_nr < order_nr_old) & (db.page_item.order_nr >= order_nr_new) & (db.page_item.page==page_id)).select(orderby=db.page_item.order_nr)        
        #zet het order_nr dat verplaatst wordt op 0
        db((db.page_item.order_nr == order_nr_old) & (db.page_item.page==page_id)).update(order_nr = 0)
        #tempNr voor het toewijzen aan order_nr
        tempNr = int(order_nr_new) + 1
        for page_item in updateOrderNrs:
            db(db.page_item.id == page_item.id).update(order_nr = tempNr)
            tempNr += 1
        #geef het verschoven record de juiste waarde
        db((db.page_item.order_nr == 0) & (db.page_item.page==page_id)).update(order_nr = order_nr_new)
        message = 'moved up'
    
    redirect(URL('showEditable/%s' % page_id))
    
@auth.requires_membership('admins')
def resetOrderNr():
    try:
        page_id=int(request.args(0))     
    except:
        redirect(error)
    for i in range (1,6): #TODO: vragen aan Tomas wat dit precies is
        db((db.page_item.id == i) & (db.page_item.page==page_id)).update(order_nr = i)
    message = 'reset'
    redirect(URL('showEditable/%s' % page_id))
    return dict(message=message)

@auth.requires_membership('admins')
def editMarkmin():
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item,formstyle='table2cols')
    else: form=SQLFORM(db.page_text,formstyle='table2cols')
    form.vars.type='markmin'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('text'))

@auth.requires_membership('admins')
def editHtml():
    db.page_text.body.widget=ckeditor.widget
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item,formstyle='table2cols')
    else: form=SQLFORM(db.page_text,formstyle='table2cols')
    form.vars.type='html'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('text'))

@auth.requires_membership('admins')
def edit():
    """Implements editing of page title and url"""
    dbtable = db.page          #uploads table name
    page_id=int(request.args(0))
    page=db.page[page_id] or redirect(error)
    form=SQLFORM(db.page,page)
    if form.process().accepted:
        if form.vars.image: makeThumbnail(dbtable,form.vars.id,(134,134)) #Thumbnail not used in this project
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('Editing the page itself'))

@auth.requires_membership('admins')
def editText():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_text[item_id] or redirect(error)
        form=SQLFORM(db.page_text,item)
    else: form=SQLFORM(db.page_text)
    form.vars.type='textarea'
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_text).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_text',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('Plain text'))

@auth.requires_membership('admins')
def editLink():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_link[item_id] or redirect(error)
        form=SQLFORM(db.page_link,item)
    else: form=SQLFORM(db.page_link)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_link).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_link',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('link'))

@auth.requires_membership('admins')
def editFAQ():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_faq[item_id] or redirect(error)
        form=SQLFORM(db.page_faq,item)
    else: form=SQLFORM(db.page_faq)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_faq).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_faq',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('faq'))

@auth.requires_membership('admins')
def editDealer():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_dealer[item_id] or redirect(error)
        form=SQLFORM(db.page_dealer,item)
    else: form=SQLFORM(db.page_dealer)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_dealer).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_dealer',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('dealer'))

@auth.requires_membership('admins')
def editImage():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_image[item_id] or redirect(error)
        form=SQLFORM(db.page_image,item)
    else: form=SQLFORM(db.page_image)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_image).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_image',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('image'))

def editForm():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_form[item_id] or redirect(error)
        form=SQLFORM(db.page_form,item)
    else: form=SQLFORM(db.page_form)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_form).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_form',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('form'))

@auth.requires_membership('admins')
def editFile():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_file[item_id] or redirect(error)
        form=SQLFORM(db.page_file,item)
    else: form=SQLFORM(db.page_file)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_file).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_file',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('file'))

@auth.requires_membership('admins')
def editPicasa():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_picasa[item_id] or redirect(error)
        form=SQLFORM(db.page_picasa,item)
    else: form=SQLFORM(db.page_picasa)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_picasa).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_picasa',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('picasa'))

@auth.requires_membership('admins')
def editYoutube():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_youtube[item_id] or redirect(error)
        form=SQLFORM(db.page_youtube,item)
    else: form=SQLFORM(db.page_youtube)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_youtube).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_youtube',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('youtube'))

@auth.requires_membership('admins')
def editFacebook():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_facebook[item_id] or redirect(error)
        form=SQLFORM(db.page_facebook,item)
    else: form=SQLFORM(db.page_facebook)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_facebook).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_facebook',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('facebook'))


@auth.requires_membership('admins')
def editSlider():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_slider[item_id] or redirect(error)
        form=SQLFORM(db.page_slider,item)
    else: form=SQLFORM(db.page_slider)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_slider).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_slider',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('slider'))

@auth.requires_membership('admins')
def editFBComments():
    response.view='page/edit.html'
    try:
        page_id, item_id = request.args[:2]
    except:
        redirect(error)    
    page=db.page[page_id] or redirect(error)
    if item_id!="0": 
        item=db.page_fbcomments[item_id] or redirect(error)
        form=SQLFORM(db.page_fbcomments,item)
    else: form=SQLFORM(db.page_fbcomments)
    if form.process().accepted:
        if item_id=="0":
            last=db(db.page_fbcomments).select().last()
            maxPageItem=db(db.page_item.page==page_id).count()
            db.page_item.insert(page=page_id,record_id=last.id,tablename='page_fbcomments',order_nr=maxPageItem+1)
        redirect(URL('showEditable/%s' % page_id))
    return dict(form=form, page=page, subtitle=T('fbcomments'))

@auth.requires_membership('admins')
def movePage():
    #request 1 should be ID or URL_name
    
    if request.args(1):
        #request 2 should be new parent
        page_id=request.args(0)
        page_parent=request.args(1)
        my_page=db(db.page.id==page_id).select().first() or redirect(error)
        my_url=my_page.url
        new_parent=db(db.page.id==page_parent).select().first()
        if new_parent: new_parent=new_parent.id
        else: new_parent=0

        tempNr = int(my_page.order_nr)
        updateOrderNrs = db((db.page.parent==my_page.parent) & (db.page.order_nr > my_page.order_nr)).select(orderby=db.page.order_nr)
        db(db.page.id==my_page.id).update(order_nr = 0)
        for page in updateOrderNrs:
            db(db.page.id == page.id).update(order_nr = tempNr)
            tempNr += 1
        
        highestOrderNr=db(db.page.parent==new_parent).select(orderby=db.page.order_nr).last()
        if highestOrderNr: highestOrderNr=int(highestOrderNr.order_nr + 1)
        else: highestOrderNr=1
        
        row = db(db.page.id == page_id).select().first()
        row.update_record(parent=page_parent, order_nr=highestOrderNr)
                
        redirect(URL('show',args=(my_url)))
   
    try:
        page_id=int(request.args(0))
        my_page=db.page[page_id] or redirect(error)
    except:
        my_page=db(db.page.url==request.args(0)).select().first() or redirect(error)
        page_id=page.id
        
    pages=db(db.page).select(orderby=db.page.parent) or redirect(error)
    return dict(my_page=my_page, pages=pages)

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
        page=db.page[page_id] or redirect(error)
    except:
        page=db(db.page.url==request.args(0)).select().first() or redirect(error)
        page_id=page.id
    if page.randomOrdered: page_children=db(db.page.parent==page_id).select(orderby='<random>')   
    else: page_children=db(db.page.parent==page_id).select(orderby=db.page.order_nr)  
    page_items = db(db.page_item.page==page.id).select(orderby=db.page_item.order_nr)

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
        elif page_item.tablename=='page_dealer':
            temp=db.page_dealer[page_item.record_id] or redirect(error_no_linked_content)
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
        elif page_item.tablename=='page_slider':
            temp=db.page_slider[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_fbcomments':
            temp=db.page_fbcomments[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
    return dict(page=page, page_items=page_items, content=content, page_children=page_children, is_admin=is_admin)

@auth.requires_membership('admins')
def showEditable():
    #request 1 should be ID or URL_name
    try:
        page_id=int(request.args(0))
        page=db.page[page_id] or redirect(error)
    except:
        page=db(db.page.url==request.args(0)).select().first() or redirect(error)
        page_id=page.id
    page_children=db(db.page.parent==page_id).select(orderby=db.page.order_nr)   
    form=SQLFORM.factory(db.page)
    if form.accepts(request.vars):
        dbtable = db.page
        #makeThumbnail(dbtable,form.vars.id,(134,134))
        form.vars.parent=page_id
        maxPage=db(db.page.parent==page.parent).count()
        form.vars.order_nr=maxPage+1
        form.vars.language=T.accepted_language
        db.page.insert(**db.page._filter_fields(form.vars))
        redirect(URL('showEditable/%s' % page_id))
    page_items = db(db.page_item.page==page.id).select(orderby=db.page_item.order_nr)
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
        elif page_item.tablename=='page_dealer':
            temp=db.page_dealer[page_item.record_id] or redirect(error_no_linked_content)
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
        elif page_item.tablename=='page_slider':
            temp=db.page_slider[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_form':
            temp=db.page_form[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)
        elif page_item.tablename=='page_fbcomments':
            temp=db.page_fbcomments[page_item.record_id] or redirect(error_no_linked_content)
            content.append(temp)      
                                 
    return dict(page=page, page_items=page_items, page_children=page_children, content=content, form=form)

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
    page = db(db.page.id == pageToCopy).select().first()
    pageItems = db(db.page_item.page == pageToCopy).select()
    
    dictInsert = {}
    #---Parse Page---
    for key, value in page.iteritems():
        if not (key == 'update_record') | (key == 'page_item') | (key == 'page_archive') | (key == 'page_item_custom') | (key == 'delete_record'):
            dictInsert[key] = value
    dictInsert['title'] = 'COPY_%s' % dictInsert['title']
    dictInsert['id'] = db(db.page).select(db.page.id.max()).first()[db.page.id.max()] + 1
    insertedPageId = db.page.bulk_insert([dictInsert])[0]
    
    #---Parse Page_items---
    for dict in pageItems:
        dictInsert = {}
        for key, value in dict.iteritems():
            if not (key == 'update_record') | (key == 'page_item_custom') | (key == 'delete_record'):
                dictInsert[key] = value
        if not len(dictInsert) == 0:
            dictInsert['id'] = db(db.page_item).select(db.page_item.id.max()).first()[db.page_item.id.max()] + 1
            dictInsert['page'] = insertedPageId
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
        #Trigger th eredirect to search page
        result=True
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form, message=message, result=result)

def offers():
    """
    offers form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Offers'
    form.vars.page=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        mail.send(to=['formaticsmailer@gmail.com'],subject='Nieuw verzoek',message=message)     
        redirect(URL('thankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def support():
    """
    support form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Support'
    form.vars.type=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        mail.send(to=['formaticsmailer@gmail.com'],subject='Nieuw verzoek',message=message) 
        redirect(URL('thankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def demo():
    """
    demo form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Demo'
    form.vars.type=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        mail.send(to=['formaticsmailer@gmail.com'],subject='Nieuw verzoek',message=message) 
        redirect(URL('thankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def question():
    """
    question form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Question'
    form.vars.type=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        mail.send(to=['formaticsmailer@gmail.com'],subject='Nieuw verzoek',message=message) 
        redirect(URL('thankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def contact():
    """
    contact form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Contact'
    form.vars.type=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        mail.send(to=['formaticsmailer@gmail.com'],subject='Nieuw verzoek',message=message) 
        redirect(URL('thankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def icontact():
    """
    contact form component
    """
    try:
        page_id = int(request.args(0))
        page=db.page[page_id] or redirect(error)
        page_id = page.title
    except:
        page_id = 'Contact page'
    form=SQLFORM(db.contact)
    form.vars.type='Contact'
    form.vars.type=page_id
    form.vars.language=T.accepted_language
    if form.process().accepted:
        contact = db(db.contact.id == form.vars.id).select().first()
        context = dict(contact=contact)
        message = response.render('emails/contactKlant.html', context)
        #mail.send(to=[form.vars.email],subject='Aanvraag ontvangen',message=message)
        if auth.is_logged_in():
            userID = str(auth.user.id) + ' (' + auth.user.first_name + ' ' + auth.user.last_name + ')'
        else:
            userID = 'Gast'
        context = dict(contact=contact,userID=userID)
        message = response.render('emails/contactAdmin.html', context)
        #SEND DIRECTLY
        mail.send(to=settings.contact_to_email,bcc=settings.email_bcc,subject='Nieuw verzoek',message=message) 
        
        #ADD TO QUEUE
        #db.queue.insert(status='pending', email=settings.email_to, subject='Nieuw verzoek', message=message)
        #db.commit()
        redirect(URL('ithankYou.load'))
    elif form.errors:
        response.flash = T('form has errors')
    else:
        response.flash = T('please fill the form')
    return dict(form=form)

def thankYou():
    thanks = 'thanks'
    return dict(thanks=thanks)

def ithankYou():
    thanks = 'thanks'
    return dict(thanks=thanks)

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
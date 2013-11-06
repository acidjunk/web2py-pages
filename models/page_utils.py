import os
import re
import datetime

class DictObj(object):
    def __getattr__(self, attr):
        return self.__dict__.get(attr)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')

def buttonDownload(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(c='static',f=action,args=args)),']')

def url(f,args=request.args,vars={}):
    return URL(r=request,f=f,args=args,vars=vars)

def goto(f,args=request.args,vars={},message='error'):
    session.flash=message
    redirect(url(f,args=args,vars=vars))

def error():
    goto('error')

def get(table, i=0, message='error'):
    try:
        id = int(request.args(i))
    except ValueError:
        goto('error',message=message)
    return table[id] or goto('error',message=message)

def link_client(client):
    return A(client.last_name,_href=url('showClient',client.id))

def link_contact(contact):
    return A(contact.last_name,_href=url('showContact',contact.id))

def link(text,action,args=[]):
    return SPAN(A(text,_href=URL(r=request,f=action,args=args)))

def pageIcon(link):
    linkName, linkExtension = os.path.splitext(link)
    if linkExtension:
        linkExtension=re.sub('\.', '', linkExtension)
        if os.path.exists(os.path.join(request.folder, 'static', 'page', 'images','extensions','%s.png' % linkExtension)): #Yay! Found nice icon
            return IMG(_src=URL(r=request,c='static', f=os.path.join('page', 'images','extensions','%s.png' % linkExtension)), _width="48")
        elif os.path.exists(os.path.join(request.folder, 'static','page','images','icons','file_extension_%s.png' % linkExtension)): #Mhm! Only found less nice icon but an icon nonetheless
            return IMG(_src=URL(r=request,c='static', f=os.path.join('page','images','icons','file_extension_%s.png' % linkExtension)), _width="48")
        else:
            return IMG(_src=URL(r=request,c='static', f=os.path.join('page','images','extensions','download.png')), _width="48")
    else: #no extension found; my best guess is that it's a link
        return IMG(_src=URL(r=request,c='static', f=os.path.join('page','images','extensions','isp.png')), _width="48")
    
#def editTags(table_name, record_id):
#    import re
#    db_tag = db.tag
#    db_link = db.tag_link
#    tagged = db((db.tag_link.table_name == table_name) & (db.tag_link.record_id == record_id)).select()
#    allTags = db(db.tag).select()
#    
#    if not auth.user_id:
#        return ''
#    formTags = SQLFORM.factory(Field('tag_name',requires=IS_SLUG()))
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
#                                   table_name=table_name,record_id=record_id)
#                if tag_exists:
#                        tag.update_record(links=tag.links+1)
#    for key in request.vars:
#        if key[:6]=='delete':
#            link_id=key[6:]
#            link=db_link[link_id]
#            del db_link[link_id]
#            db_tag[link.tag] = dict(links=db_tag[link.tag].links-1)
#    links = db(db_link.table_name==table_name)\
#                   (db_link.record_id==record_id).select()\
#                  .sort(lambda row: row.tag.name.upper()) 
#    return dict(tagged=tagged,links=links,formTags=formTags,allTags=allTags)
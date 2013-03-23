# -*- coding: utf-8 -*-
# This controller will implement a basic but powerfull search.
# For each tabel/model you define one method that handles the search in that model.
# Then you return a result.

def index():
    message="please provide a search term or use the advanced search"
    return locals()

def home():
    vars=request.vars
    return locals()

def quick():
    validTermFound=False
    term=request.vars['searchPhrase'] #Set when user pressed enter from search box in layout
    if term: validTermFound=True

    if not validTermFound:
        try:
            term=request.args(0)
        except:
            redirect(URL('search','index'))
    try:
        mode=request.args(1)
    except:
        mode="ALL"

    #Fix for non valid terms and ugly home page quick search stuff
    if term==None:
        redirect(URL('search','showSearch'))
        
    types=[]
    if term:
        types.append('pages')
    return dict(term=term, types=types)

def showSearch():
    #TODO: clean up _style= construct
    result=None
    message=SPAN(T('Enter searchphrase'))
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


def tags():
    import re
    r = re.compile('<[^>]*>')
    
    response.view='search/tags.load'
    
    #TODO: Decide if we use summary for tags
    term=request.args(0) or redirect(URL('default', 'index'))
    
    tags=db(db.plugin_tagging_tag.name.contains(term)).select()
    results=[]
    for tag in tags:
        content_items=db(db.plugin_tagging_link.tag==tag.id).select(orderby=db.plugin_tagging_link.table_name)
        #if settings.debug: print "Search found items: %s for tag name: %s with id: %d" % (content_items,tag.name,tag.id)
        for content_item in content_items:
            found=False
            for result in results:
                if (result['table_name']==content_item.table_name) & (result['id']==content_item.record_id):
                    found=True
            if not found:
                if content_item.table_name=="page":
                    detail=db(db.page.id==content_item.record_id).select().first()
                    if detail != None:
                        summary=None
                        page_items=db((db.page_item.page==content_item.record_id) & (db.page_item.tablename=='page_text')).select()
                        if page_items:
                            summary=''
                            for item in page_items:
                                page_text=db(db.page_text.id==item.record_id).select().first()
                                if page_text.type=='html':
                                    summary+=page_text.body
                                elif page_text.type=='markmin':
                                    summary+=str(MARKMIN(page_text.body, extra={'space':lambda code: '<br>'}))
                                else:
                                    summary+=page_text.body
                            summary = r.sub('', summary)
                        results.append({'tag':tag.name, 'id':content_item.record_id, 'table_name':content_item.table_name,'title':detail.title,'link':URL('page', 'show', args=detail.url),'summary':summary})
                else:
                    if settings.debug: print "Error: unsupported tableName (%s) for search" % content_item.table_name
    return dict(results=results, term=term, tags=tags)

def pages():
    import re
    r = re.compile('<[^>]*>')
    
    response.view='search/pages.load'
    try:
        term=request.args(0)
    except:
        redirect(error)
    pages=db((db.page.title.contains(term)) & (db.page.language=='nl')).select()
    results=[]
    for page in pages:
        summary=None
        page_items=db((db.page_item.page==page.id) & (db.page_item.tablename=='page_text')).select()
        if page_items:
            summary=''
            for item in page_items:
                page_text=db(db.page_text.id==item.record_id).select().first()
                if page_text.type=='html':
                    summary+=page_text.body
                elif page_text.type=='markmin':
                    summary+=str(MARKMIN(page_text.body, extra={'space':lambda code: '<br>'}))
                else:
                    summary+=page_text.body
            summary = r.sub('', summary)
        results.append({'id':page.id, 'table_name':'page','title':page.title,'summary':summary, 'link':URL('page', 'show', args=page.url)})
    return dict(results=results, term=term)
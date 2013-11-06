# Contact stuff
db.define_table('contact',
   Field('language', requires=IS_IN_SET(('nl','en')),writable=False,readable=False),                
   Field('type', type='string', label=T('Type'), requires=IS_IN_SET(('Support','Question','Demo','Offers','Contactpage')), writable=False,readable=False),
   Field('page', type='string', label=T('Page'),writable=False,readable=False),
   Field('name', type='string', label=T('Name'), requires=(IS_NOT_EMPTY())),
   Field('email',type='string' ,label='Email', requires=IS_EMAIL()),
   Field('company', type='string', label=T('Company')),
   Field('body','text',label=T('Your comment')),
   auth.signature,
   Field('posted_on','datetime',default=request.now,writable=False,readable=False))

db.contact.is_active.writable=False
db.contact.is_active.readable=False

db.define_table('queue',
    Field('status'),
    Field('email'),
    Field('subject'),
    Field('message'))
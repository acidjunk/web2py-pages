import os

#The parent reference could also be done with:
#    Field('parent', 'reference page'),
db.define_table('page',
    Field('language', requires=IS_IN_SET(('nl-nl','en-us'))), #TODO: see if you can use language list from web2py itself
    Field('parent', type='integer', writable=False,readable=False,  
          label=T('Parent page')),                
    Field('title',default='',label=T("Title"),
          requires=(IS_NOT_EMPTY())),
    Field('short_title',default='',label=T("Short title, will appear in menu's"),
          requires=(IS_NOT_EMPTY())),
    Field('url',default='',label=T('Unique name of the URL'),
          requires=(IS_SLUG(),IS_NOT_IN_DB(db,'page.url'))),
    Field('summary_title', type='string', label=T('summary title'), comment=T('will be used for naming boxes if provided.')),                                
    Field('summary', type='text', label=T('summary'), comment=T('will be shown in the sidebar.')),                                
    Field('isActive','boolean',default=True),
    Field('isMenuitem','boolean',default=True,label=T("When enabled the page will appear in menu or submenu")),
    Field('showChildren','boolean',default=True,label=T("When enabled the subdocuments of this page will be visible")),
    Field('childrenTitle','string',label=T("Name the sub pages")),
    Field('image', type='upload', label=T("Page icon")),
    Field('imageThumb', type='upload', writable=False, readable=False, uploadfolder=os.path.join(request.folder,'static','page','images','thumbs'),),
    Field('showSiblings','boolean',default=False,label=T("When enabled the siblingsMenu will be visible")),
    Field('randomOrdered','boolean',default=False,label=T("When enabled the children will be shown in random order")),
    Field('order_nr', type='integer', default=0, writable=False,readable=False),    
    Field('role',db.auth_group,requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_group.id','%(role)s'))),
    Field('changelog',default=''),
    auth.signature,
    format = '%(title)s', migrate=True)

db.define_table('page_archive',                                    
    Field('current_record',db.page),                               
    db.page,
    format = '%(slug) %(modified_on)s', migrate=True)

db.define_table('page_item',
   Field('page', db.page, writable=False,readable=False,
          label=T('Page')),  
   Field('tablename', type='string', requires=IS_IN_SET(('page_text','page_image','page_file','page_link','page_youtube','page_facebook','page_form','page_image_slider','page_form','page_faq','page_dealer')), writable=False,readable=False,
          label=T('Content type')),
   Field('record_id', type='integer', writable=False,readable=False),
   Field('order_nr', type='integer', default=0, writable=True,readable=True))

db.page_item.page.requires = IS_IN_DB(db, db.page.id, 'Language: %(language)s %(title)s')

db.define_table('page_text',
   Field('title', type='string',
          label=T('Define if you use subtitles')),
   Field('type', type='string', writable=False,readable=False,  
          requires=IS_IN_SET(('html','markmin','textarea')), label=T('Parent page')),                 
   Field('body', type='text',requires=(IS_NOT_EMPTY())))  

db.define_table('page_text_archive',
    Field('current_record',db.page_text),                               
    db.page_text,
    format = '%(title) %(modified_on)s', migrate=True)

db.define_table('page_image',
   Field('title', type='string',
          label=T('Define the image title')),
   Field('image', type='upload',requires=(IS_NOT_EMPTY())),
   Field('hasLightbox', type='boolean', label=T('Has lightbox?'), default=True))

db.define_table('page_file',
   Field('title', type='string',
          label=T('Define the file title'),requires=(IS_NOT_EMPTY())),
   Field('file', type='upload',requires=(IS_NOT_EMPTY())))

db.define_table('page_picasa',
   Field('userid', type='string',
          label=T('Google Picasa User ID'), requires=(IS_NOT_EMPTY())),
   Field('albumid', type='string',
         label=T("Google Picasa Album ID"), requires=(IS_NOT_EMPTY())))

db.define_table('page_youtube',
   Field('title', type='string',
          label=T('Define a custom title')),
   Field('youtube', type='string',
         label=T("Youtube code"), requires=(IS_NOT_EMPTY())))

db.define_table('page_facebook',
   Field('facebook', type='string',
         label=T("Facebook URL"), requires=(IS_NOT_EMPTY())))

#TODO: Needs extra field for internal link or external link
db.define_table('page_link',
   Field('title', type='string',
          label=T('Name of the link'),requires=(IS_NOT_EMPTY())),
   Field('link', type='string',requires=(IS_URL())))

db.define_table('page_faq',
   Field('question', type='string',
          label=T('Question'), requires=(IS_NOT_EMPTY())),
   Field('answer', type='text', label=T("Answer"), requires=(IS_NOT_EMPTY())))  

db.define_table('page_dealer',
    Field('name', type='string', label=T('dealer name'), requires=(IS_NOT_EMPTY())),
    Field('address', type='string', label=T('dealer address')),
    Field('postcode', type='string', label=T('postcode')),
    Field('location', type='string', label=T('location')),
    Field('website', type='string', label=T('website')),
    Field('email', type='string', label=T('email')),
    Field('phone', type='string', label=T('phone')))               

db.define_table('page_slider',
   Field('width', type='string', label=T('width in pixels'), requires=(IS_NOT_EMPTY())),
   Field('height', type='string', label=T('height in pixels'), requires=(IS_NOT_EMPTY())),
   Field('image1', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider'), requires=(IS_NOT_EMPTY()), comment=T("Only first picture is mandatory")),
   Field('link1', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption1', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image2', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link2', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption2', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),  
   Field('image3', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link3', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption3', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image4', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link4', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption4', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image5', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link5', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption5', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image6', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link6', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption6', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image7', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link7', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption7', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image8', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link8', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption8', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image9', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link9', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption9', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")),
   Field('image10', type='upload', uploadfolder=os.path.join(request.folder,'static/page/images/slider')),
   Field('link10', type='string', label=T('Link'), comment=T("Fill out a link and the picture will be a button"), requires=(IS_EMPTY_OR(IS_URL()))),
   Field('caption10', type='string', label=T('Caption'), comment=T("Fill out a caption and a, SEO friendly, extra text will be shown")))

db.define_table('page_form',
   Field('form_type', type='string', label=T('Choose a form to include'), requires=IS_IN_SET(('Support','Question','Demo','Offers','Contactpage'))))

#Add first toplevel page if none exist
if (db((db.page.parent==0) & (db.page.language=='en-us') & (db.page.isMenuitem==True)).count() == 0):
    db.page.insert(language='en-us',
                   parent=0,
                   title='Informatie',
                   short_title='Informatie',
                   url='info')
from plugin_ckeditor import CKEditor
ckeditor = CKEditor(db)
ckeditor.define_tables()

#Plugin CKEditor:
#controllers/plugin_ckeditor.py
#model/1_ckeditor.py
#modules/plugin_ckeditor.py
#static/plugin_ckeditor
#views/plugin_ckeditor

# db.newsletter.agenda_content.widget = ckeditor.widget
# db.newsletter_items.content.widget = ckeditor.widget
# db.newsletter_boxes.content.widget = ckeditor.widget

db.page_text.type.widget = ckeditor.widget

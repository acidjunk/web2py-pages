def customizePageItem():
    pageID = request.args(0) or redirect(URL('default', 'index'))
    page_itemID = request.args(1) or redirect(URL('default', 'index'))
    db.page_item_custom.page.default = pageID
    db.page_item_custom.page_item.default = page_itemID
    page_item_custom = db(db.page_item_custom.page_item == page_itemID).select().last()
    if page_item_custom:
        form = SQLFORM(db.page_item_custom, page_item_custom.id, deletable=True, upload=URL('default', 'download'))
    else:
        form = SQLFORM(db.page_item_custom)
    if form.process().accepted:
       redirect(URL('page', 'showEditable', args=pageID))
    return dict(form=form)
        
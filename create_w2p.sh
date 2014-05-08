#TODO: write a python script for this
tar -cvzf ../web2py.plugin.pages_with_languages.w2p views/page views/page_custom views/plugin_ckeditor views/plugin_tagging controllers/page* modules/plugin_ckeditor.py models/page*.py models/0_db.py models/plugin_ckeditor.py models/plugin_tagging.py static/page static/plugin_ckeditor static/plugin_markitup static/plugin_wiki languages/
tar -cvzf ../web2py.plugin.pages.w2p views/page views/page_custom views/plugin_ckeditor views/plugin_tagging controllers/page* modules/plugin_ckeditor.py models/page*.py models/0_db.py models/plugin_ckeditor.py models/plugin_tagging.py static/page static/plugin_ckeditor static/plugin_markitup static/plugin_wiki
echo "Shall I copy the w2p file to release location? y/n "
read ans
if [ ${ans} == 'y' ]; then
    cp ../web2py.plugin.pages*.w2p ~/Dropbox/Public
fi

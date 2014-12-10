web2py-pages
============

Pages module for web2py which gives you a good starting point for any type of CMS.
It features a tree of pages with sluggified (URL friendly) names. Pages can consist out of items. Current page items:
markmin text, html text, plain text, image, imageslider, photoalbum, FAQ, address, 
file upload, links and a couple of pre defined forms.

Installation:
To try it; just clone it in a web2py/applications/ folder.
E.g.: git clone git@github.com:acidjunk/web2py-pages.git pages

Or use the copy_to_app.sh script to copy just the needed files to an existing app.

Todo:
- Add the extra styling info in one.css file
- Test
- Clean up older web2py constructs
- Fix language problem

Needed dependencies:
- gdata for google picasa
- PIL for scaling and thumbs (ImageMagick support will be added)

You can also use the w2p files (you'll still need the deps.)

w2p:
https://dl.dropboxusercontent.com/u/20756661/web2py.plugin.pages.w2p
https://dl.dropboxusercontent.com/u/20756661/web2py.plugin.pages_with_languages.w2p

Changelog:
-----
Version 1.1 (develop)
- Recreated the w2p release script
- Used welcome app to get an easier workflow (git repo can be cloned and should give you a complete and working web2py app)
- Fixed language support

-----
Version 1.0 RC2
- Fixed the issue with the DAL and a reserved keyword 'page' error. The app should will now install without touching any core web2py welcome/ application file

-----
Version 1.0 RC1
- Added CKeditor and markmin
- Added tagging
- Added adminMenu
- Added an easy way to create a test page with all items
- Added page copy functionality
- Added NL translation
- Fixed language settings; en-us is default
- Moved loading of the javascript deps to the view, so no change in the web2py layout is needed.
- Nivoslider, Fancybox, Google Picasa Photoalbum have working views
- It's ready to use as a web2py plugin

Known problems:
- not SQL strict
- some jquery problems with the other javascript deps and the latest web2py stable (2.7.1). 
A workround is available on most places by downgrading jquery to 1.8.0
----
Version  0.9

Current State: This is a work in progress. 

Already works:
- DB model for multilingual page tree with subpages and complex pages that can consist of many different page items.
- Basic editing in the tree
- MarkMin, Html Or Plain text + the following extra types: File, Image, Slider, Facebookbox, Twitterbox, Address, Subpages, Youtube, FAQ
- Menu 
- Tested Against web2py 2.4.1




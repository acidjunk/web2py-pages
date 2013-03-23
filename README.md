web2py-pages
============

Pages module for web2py which gives you a good starting point for any type of CMS

Version  0.9

Current State: This is a work in progress. 

Already works:
- DB model for multilingual page tree with subpages and complex pages that can consist of many different page items.
- Basic editing in the tree
- MarkMin, Html Or Plain text + the following extra types: File, Image, Slider, Facebookbox, Twitterbox, Address, Subpages, Youtube, FAQ
- Menu 
- Tested Against web2py 2.4.1

Installation:
To try it; just create a new app from the web2py admin and copy the content of this github folder over it.

Todo:
- Add the extra styling info in one.css file
- Add the missing java libs (Fancybox, NivoSlider,FCKeditor) 
- Fix headers for the extra java libs in a smart way
- Test
- Clean up older web2py constructs

Needed dependencies:
- gdata for google picasa
- PIL for scaling and thumbs (ImageMagick support will be added)


#set the language
#if auth.has_membership('admins'):
#    if 'siteLanguage' in request.cookies and not (request.cookies['siteLanguage'] is None):
#        T.force(request.cookies['siteLanguage'].value)
#else: 
#    #FORCE LANG TO NL for non admin stuff
#    #WHEN EN trans is done; remove the admin stuff

#TODO:: put nice flash/language select back 
#T.force('nl-nl')
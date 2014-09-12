#TODO: remove this when we did some more test with postgres
real_DAL = DAL

#A hook to get around the DAL check_reserved problem with a table named 'page'
def DAL(*args, **kwargs):
   kwargs['check_reserved'] = False
   kwargs['entity_quoting'] = True
   return real_DAL(*args, **kwargs)

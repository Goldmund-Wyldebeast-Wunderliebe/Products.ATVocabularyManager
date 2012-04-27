from Products.Five import BrowserView                                                     

class SimpleVocabularyView(BrowserView): 


    def __call__(self):
        if 'save' in self.request.form.keys():
            return self.saveVocab()

        elif 'delete' in self.request.form.keys():
            return self.deleteTerm()
        else:
            return super(SimpleVocabularyView, self).__call__() 

    def saveVocab(self):
        request = self.request
        form = request.form
        if 'keys' in form and 'values' in form:
            
            values = form.get("values")
            keys = form.get("keys")
            oldvalues = form.get("oldvalues")
            oldkeys = form.get("oldkeys")


            ##Loop over keys .. and see if it is different then oldkey at that index.
            ##If so.. the id change, and we have to rename it.
            ##If not, we check if the title (value) changed and change that if needed.
            for index, key in enumerate(keys):
                value = values[index]
                oldkey =  index < len(oldkeys) and oldkeys[index] or ''
                ##Are we changing or creating?
                if hasattr(self.context, key) or hasattr(self.context, oldkey) :                                          
                    ##Only need old key/value if there's something to change
                    oldvalue = oldvalues[index]

                    if key != oldkey:
                        ##They changed the ID. Rename the term.
                        self.context.manage_renameObjects((oldkey, ), (key, ))
                        self.context.plone_utils.addPortalMessage("Renamed term: '%s' to '%s' " % (oldkey, key))                   
                        self.context.plone_log("Renamed term: '%s' to '%s' " % (oldkey, key))                   

                    ##Check if there's any term with this key.
                    ##Check if the title has indeed changed.
                    if oldvalue != value:
                        ##Fetch term and set title and reindex.
                        term = getattr(self.context, key)                                   
                        term.setTitle(value)                                           
                        term.reindexObject(idxs=['Title'])
                        self.context.plone_utils.addPortalMessage("Updated term: '%s' , Title: '%s' " % (key, value))                   
                        self.context.plone_log("Updated term: '%s' , Title: '%s' " % (key, value))                   
                else:                                                              
                    ##New term                                                     
                    self.context.invokeFactory('SimpleVocabularyTerm', key, title=value)
                    self.context.plone_utils.addPortalMessage("Created term: %s , Title: %s " % (key, value))                   
                    self.context.plone_log("Created term: %s , Title: %s " % (key, value))                   

        return self.request.response.redirect(self.context.absolute_url())

    def deleteTerm(self):
        request = self.request
        form = request.form

        if 'key' in form:
            key = form.get('key')
            if hasattr(self.context, key):
                self.context.manage_delObjects(key)
                self.context.plone_utils.addPortalMessage("Deleted term: %s " % key)
        return

#    def saveTerm(self):
#        request = self.request
#        self.context = self.self.context
#        form = request.form
#
#        if 'key' in form and 'value' in form:
#            key = form.get('key')
#            value = form.get('value')
#            if hasattr(self.context, key):                                          
#                term = getattr(self.context, key)                                   
#                term.setTitle(value)                                           
#                self.context.plone_utils.addPortalMessage("Updated term: %s , Title: %s " % (key, value))                   
#            else:                                                              
#                ##New term                                                     
#                self.context.invokeFactory('SimpleVocabularyTerm', key, title=value)
#                self.context.plone_utils.addPortalMessage("Created term: %s , Title: %s " % (key, value))                  
#        return


#    def _saveTerm(self, key, value):
#        if hasattr(self.self.context, key):                                          
#            term = getattr(self.self.context, key)                                   
#            term.setTitle(value)                                           
#            self.self.context.plone_utils.addPortalMessage("Updated term: %s , Title: %s " % (key, value))                   
#        else:                                                              
#            ##New term                                                     
#            self.self.context.invokeFactory('SimpleVocabularyTerm', key, title=value)
#            self.self.context.plone_utils.addPortalMessage("Created term: %s , Title: %s " % (key, value))                  

#encoding=utf-8

def no_new_attributes(wrapped_setattr):
    """ raise an error on attempts to add a new attribute, while
        allowing existing attributes to be set to new values.
    """
    def __setattr__(self, name, value):
        if hasattr(self, name):    # not a new attribute, allow setting
            wrapped_setattr(self, name, value)
        else:                      # a new attribute, forbid adding it
            raise AttributeError("can't add attribute %r to %s" % (name, self))
    return __setattr__
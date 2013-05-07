#coding=UTF-8
from django.conf import settings

allowed_apps = [
    {
        'app':'auth', 
        'models':[
            {
                'model':'user',
                'fields':['username', 'first_name', 'last_name']
            },
#            {
#                'model':'group',
#                'fields':['name']
#            },            
        ]
    },
    {   
        'app':'contenttype'
    },
#    {   
#        'app':'aspect',
#    }        
]

ALLOWEDS_APPS = getattr(settings, "REL_ALLOWEDS_APPS", allowed_apps)
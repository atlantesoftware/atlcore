'''
Created on Feb 1, 2012

@author: raisel
'''
from atlcore.mailresponder.mailfacade import MailFacade

import logging
from string import lower
logger = logging.getLogger('atlcms')

class MailResponder(object):
    
    RESPONDER_ACCOUNT = 'suenacubano@suenacubano.com'
    
    command_translation = {
       'ayuda':'command_help',
       'cartelera':'command_calendar',
       'cancelar':'command_unsubscribe',
       'suscribir':'command_subscribe',
       'postal':'command_send_postal',
       #'info':'command_info'
       'enviar':'command_send',
       'promo':'command_send_custom_promo',
       'generalbulletin':'command_send_general_bulletin',
    }
    
    def process_analityc(self, email_object):
        pass

    def execute_command(self, raw_email=None):   
        raw_email = raw_email        
        email_request = self.get_email_request_object(raw_email)        
        command = email_request['command']        
        email_from = email_request['from']          
        if email_from != 'info@suenacubano.com':
            logger.info('=========EMAIL FROM->%s=======COMMAND->%s' % (email_from,command));
            
            if command and command != '' and self.command_translation.has_key(lower(command)):
                command = lower(command)
                self.__getattribute__(self.command_translation.get(command))(email_request)
                self.process_analityc(email_request, True)
            else:
                self.command_help(email_request, False)
                self.process_analityc(email_request, False)
        
                                               
    def respond(self, subject, body, to_email_list, dict_images={}):
        logger.info('=========ENTERED=======');
        MailFacade.send_bulk_emails(subject, body, self.RESPONDER_ACCOUNT, to_email_list, dict_images)
        
    def get_email_request_object(self, raw_email):
        email_request = {}
        email_request['subject'] = '' # Inicializando el subject para el caso que no se envie datos
        
        for line in raw_email.splitlines():
            if line.lower().startswith('subject:'):
                email_request['subject'] = line.partition('Subject:')[2].strip()
                       
            elif line.lower().startswith('from:'):
                email_request['from'] = line.partition('From:')[2].strip()
                if email_request['from'].find('<') >= 0:
                    email_request['from'] = email_request['from'].partition('<')[2].partition('>')[0]
            
            elif line.lower().startswith('to:'):
                email_request['to'] = line.partition('To:')[2].strip()
                if email_request['to'].find('<') >= 0:
                    email_request['to'] = email_request['to'].partition('<')[2].partition('>')[0]
                    
        command,params = self.split_command_and_params(email_request['subject'])    
        email_request['command'] = command
        email_request['params'] = params
        
        return email_request
        
    def split_command_and_params(self, subject):
        list = subject.split()
        if len(list) > 0:
            return (list[0],list[1:])
        return ('','')

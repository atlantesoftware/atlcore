#coding=UTF-8
import commands
from telnetlib import Telnet
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(subject, text_content, html_content, to):
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class EmailValidator(object):
    
    def get_email_server(self, email):
        domain = email.split('@')[1]
        response = commands.getoutput('nslookup -q=mx %s' % domain) 
        response = response.splitlines()
        email_server = ''
        for line in response:
            if line.find('exchanger = ') > 0:
                email_server = line.split(' ')[len(line.split(' ')) - 1][:-1]
        return email_server
                
    def check_email(self, email):
        email_server = self.get_email_server(email)
        domain = email.split('@')[1]
        if email_server != '':
            tn = Telnet(email_server, 25)
            
            print 'Making smtp to: %s' % email_server
            tn.write(b'helo hi\n')
            print 'Response: %s' % tn.read_until('\n')
            
            print 'mail from:<jessica@%s>\n' % domain
            tn.write(b'mail from:<jessica@%s>\n' % domain)
            print 'Response: %s' % tn.read_until('\n')
            
            print 'rcpt to:<%s>\n' % email
            tn.write(b'rcpt to:<%s>\n' % email)
            print 'Response: %s' % tn.read_until('\n')
            response = tn.read_until('\n')
            print 'Response: %s' % response
            
            tn.write(b'quit\n')
            return response.startswith('250')
        else:
            return False
        
#if __name__ == "__main__":
#    email_validator = EmailValidator()
#    print email_validator.check_email('sirdreis@hotmail.com')
    
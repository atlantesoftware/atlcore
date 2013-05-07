#encoding=UTF-8
from django.core import mail
from django.core.mail.message import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings


class MailFacade(object):
    
    @classmethod
    def send_decorated_email(cls, subject, body, from_email, to_email_list):
        msg = mail.EmailMessage(subject, body, from_email, to_email_list)        
        msg.content_subtype = "html"
        msg.send()
    
    
    @classmethod
    def send_bulk_emails(cls, subject, body, from_email, to_email_list, dict_images=None):
        msg_list = []
        for email in to_email_list:
            msg = EmailMultiAlternatives(subject, body, from_email, [email])
            if dict_images:
                for key in dict_images.keys():
                    image_path = dict_images.get(key)
                    fp = open(image_path, 'rb')
                    mimeImage = MIMEImage(fp.read())
                    fp.close()
                    mimeImage.add_header('Content-ID', '<'+ key +'>')
                    msg.attach(mimeImage)
            msg.attach_alternative(body, "text/html")
            msg.encoding = "utf-8"
            msg.mixed_subtype = 'related'
            #msg.content_subtype = "html" # Doute
            msg_list.append(msg)
        
        connection = mail.get_connection()
        connection.open()
        ten_msg_list = []
        while msg_list <> []:
            if len(ten_msg_list) < 1000:
                ten_msg_list.append(msg_list[0])
                msg_list.pop(0)
            else:
                connection.send_messages(ten_msg_list)
                ten_msg_list = []
        if ten_msg_list <> []:
            connection.send_messages(ten_msg_list)
        connection.close()

import smtplib
from src import configurations, message_email_html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

title = "STATISTIQUE DOMOTIQUE MAMAN SERVICE"
destination = "victoirekasende133@gmail.com"
provenance = "MAMAN SERVICE"


def envoyer_email(email_destinataire, sujet, message, provenance):
    multipart_message = MIMEMultipart()
    multipart_message["Subject"] = sujet
    multipart_message["From"] = provenance
    multipart_message["To"] = email_destinataire

    html_part = MIMEText(message, "html")
    multipart_message.attach(html_part)
    
    serveur_mail = smtplib.SMTP(configurations.config_server, configurations.config_server_port)
    serveur_mail.starttls()
    serveur_mail.login(configurations.config_email, configurations.config_password)
    serveur_mail.sendmail(configurations.config_email, email_destinataire, multipart_message.as_string())
    
    serveur_mail.quit()
    

def send_mail(etat_maison):
    message_html = message_email_html.return_fString_html(etat_maison)
    envoyer_email(destination, title, message_html, provenance=provenance)



     


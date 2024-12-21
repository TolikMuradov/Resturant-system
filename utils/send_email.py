from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_html_email(subject, to_email, template, context):
    """
    HTML formatında e-posta göndermek için bir yardımcı fonksiyon.
    """
    html_content = render_to_string(template, context)
    email = EmailMessage(subject, html_content, to=[to_email])
    email.content_subtype = "html"  # HTML formatını belirtir
    email.send()

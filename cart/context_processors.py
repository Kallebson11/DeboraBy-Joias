from django.conf import settings
 
def whatsapp(request):
    return {'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER}
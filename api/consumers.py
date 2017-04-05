from channels.handler import AsgiHandler
from django.http import HttpResponse


def http_consumer(message):
    response = HttpResponse("Hello World! You ased for %s" % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)
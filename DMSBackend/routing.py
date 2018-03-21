from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler

from serve.consumer import ServeConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
            path("connectToServer", ServeConsumer),
        ]),
})

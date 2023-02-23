from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from devices.models import Aqua


class AquaSerializer(ModelSerializer):
    color_rgb = serializers.SerializerMethodField('_color_rgb')

    def _color_rgb(self, object):
        color = object.color
        r = color[1:color.index('g')]
        g = color[color.index('g')+1:color.index('b')]
        b = color[color.index('b')+1:]
        return (f'rgb({r},{g},{b})')

    class Meta:
        model = Aqua
        exclude = ('id', 'color',)


class AquasSerializer(ModelSerializer):
    ip = serializers.SerializerMethodField('_ip')
    port = serializers.SerializerMethodField('_port')

    def _ip(self, object):
        ip = object.sensor.ip
        return ip

    def _port(self, object):
        port = object.sensor.port
        return port

    class Meta:
        model = Aqua
        exclude = ('id', 'color', 'sensor',)

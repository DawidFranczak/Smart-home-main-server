from devices.models import Aqua

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class AquaSerializer(ModelSerializer):
    color_rgb = serializers.SerializerMethodField("_color_rgb")

    def _color_rgb(self, object):
        color = object.color
        _r = color[1 : color.index("g")]
        _g = color[color.index("g") + 1 : color.index("b")]
        _b = color[color.index("b") + 1 :]
        return f"rgb({_r},{_g},{_b})"

    class Meta:
        model = Aqua
        exclude = (
            "id",
            "color",
        )


class AquasSerializer(ModelSerializer):
    ip = serializers.SerializerMethodField("_ip")
    port = serializers.SerializerMethodField("_port")

    def _ip(self, object):
        _ip = object.sensor.ip
        return _ip

    def _port(self, object):
        _port = object.sensor.port
        return _port

    class Meta:
        model = Aqua
        exclude = (
            "id",
            "color",
            "sensor",
        )

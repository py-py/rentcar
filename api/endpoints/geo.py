from geo.models import City
from geo.models import Country
from rest_framework import serializers
from rest_framework import viewsets


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="code.name")

    class Meta:
        model = Country
        fields = ("id", "uuid", "code", "name", "currency")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "uuid", "name")


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ("country__code",)

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
    country_id = serializers.ReadOnlyField(source="country.id")
    country_code = serializers.ReadOnlyField(source="country.code.code")

    class Meta:
        model = City
        fields = ("id", "uuid", "name", "country_id", "country_code")


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ("country__code",)

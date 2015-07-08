import datetime
import arrow
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers, viewsets, generics, filters
from modeltranslation.translator import translator, NotRegistered
from munigeo import api as munigeo_api
import django_filters

from .models import Unit, Resource, Reservation, Purpose


all_views = []
def register_view(klass, name, base_name=None):
    entry = {'class': klass, 'name': name}
    if base_name is not None:
        entry['base_name'] = base_name
    all_views.append(entry)

LANGUAGES = [x[0] for x in settings.LANGUAGES]


class TranslatedModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TranslatedModelSerializer, self).__init__(*args, **kwargs)
        model = self.Meta.model
        try:
            trans_opts = translator.get_options_for_model(model)
        except NotRegistered:
            self.translated_fields = []
            return

        self.translated_fields = trans_opts.fields.keys()
        # Remove the pre-existing data in the bundle.
        for field_name in self.translated_fields:
            for lang in LANGUAGES:
                key = "%s_%s" % (field_name, lang)
                if key in self.fields:
                    del self.fields[key]

    def to_representation(self, obj):
        ret = super(TranslatedModelSerializer, self).to_representation(obj)
        if obj is None:
            return ret

        for field_name in self.translated_fields:
            if field_name not in self.fields:
                continue
            d = {}
            for lang in LANGUAGES:
                key = "%s_%s" % (field_name, lang)
                val = getattr(obj, key, None)
                if val is None:
                    continue
                d[lang] = val

            # If no text provided, leave the field as null
            for key, val in d.items():
                if val is not None:
                    break
            else:
                d = None
            ret[field_name] = d

        return ret


class NullableTimeField(serializers.TimeField):
    def to_representation(self, value):
        if not value:
            return None
        return super().to_representation(value)


class UnitSerializer(TranslatedModelSerializer, munigeo_api.GeoModelSerializer):
    opening_hours_today = serializers.DictField(child=NullableTimeField(),
                                                source='get_opening_hours')

    class Meta:
        model = Unit


class UnitViewSet(munigeo_api.GeoModelAPIView, viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

register_view(UnitViewSet, 'unit')


class PurposeSerializer(TranslatedModelSerializer):
    class Meta:
        model = Purpose
        fields = ['name', 'main_type', 'id']


class ResourceSerializer(TranslatedModelSerializer, munigeo_api.GeoModelSerializer):
    available_hours = serializers.SerializerMethodField()
    opening_hours_today = serializers.DictField(child=NullableTimeField(),
                                                source='get_opening_hours')
    purposes = PurposeSerializer(many=True)

    class Meta:
        model = Resource

    def get_available_hours(self, obj):
        parameters = self.context['request'].query_params
        if 'duration' in parameters or 'start' in parameters or 'end' in parameters:
            try:
                duration = datetime.timedelta(minutes=int(parameters['duration']))
            except MultiValueDictKeyError:
                duration = None
            try:
                start = arrow.get(parameters['start']).datetime
            except MultiValueDictKeyError:
                start = None
            try:
                end = arrow.get(parameters['end']).datetime
            except MultiValueDictKeyError:
                end = None
            return obj.get_available_hours(start=start, end=end, duration=duration)
        return obj.get_available_hours()


class ResourceFilter(django_filters.FilterSet):
    purpose = django_filters.CharFilter(name="purposes__id", lookup_type='iexact')

    class Meta:
        model = Resource
        fields = ['purpose']


class ResourceViewSet(munigeo_api.GeoModelAPIView, viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = ResourceFilter

register_view(ResourceViewSet, 'resource')


class ReservationSerializer(TranslatedModelSerializer, munigeo_api.GeoModelSerializer):

    class Meta:
        model = Reservation
        fields = ['resource', 'begin', 'end', 'user']


class ReservationViewSet(munigeo_api.GeoModelAPIView, viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

register_view(ReservationViewSet, 'reservation')

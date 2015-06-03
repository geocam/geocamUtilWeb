from django.core.serializers.json import DjangoJSONEncoder


class DatetimeJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return super(DatetimeJsonEncoder, self).default(obj)
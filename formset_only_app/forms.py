from django.forms.models import modelformset_factory
from .models import Item

ItemModelFormSet = modelformset_factory(
    Item,
    extra=2, 
    max_num=3,
    fields='__all__',
)
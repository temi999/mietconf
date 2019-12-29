from django.forms import ModelForm
from . import models

class SendMaterialForm(ModelForm):
    class Meta:
        model = models.Material
        fields = ['title', 'description', 'document', 'presentation']
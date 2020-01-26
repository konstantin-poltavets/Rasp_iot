from django import forms
from .models import Modules, Boards, Mqtt, Mqttypes

class ModulesForm(forms.ModelForm):


    class Meta:

        model = Modules
        model.description = forms.CharField(widget=forms.CharField)
        fields = ['name' , 'photos', 'description', 'id', 'type1', 'type2',  'type3', 'type4']


        #model.description.widget.attrs.update(rows='2')

'''
    def __init__(self, id, *args, **kwargs):
        super(ModulesForm, self).__init__(*args, **kwargs)
        self.fields['id'].queryset = Modules.objects.filter(id=82)
'''

class BoardsForm(forms.ModelForm):

    class Meta:

        model = Boards
        fields = ['name', 'description', 'id',
                  'ip_address', 'processor', 'sensor1', 'sensor2',  'sensor3', 'sensor4','location', 'photos', 'scetch']

class MqttForm(forms.ModelForm):

    class Meta:

        model = Mqtt
        fields = ['created_date', 'topic', 'payload']



class MqttypesForm(forms.ModelForm):

    class Meta:

        model = Mqttypes
        fields = ['id', 'type', 'topic']
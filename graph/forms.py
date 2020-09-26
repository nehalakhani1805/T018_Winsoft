from django import forms
from .models import Input, Vertex, Edge


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['key', 'enc_string']

class AddNodeForm(forms.ModelForm):
    class Meta:
        model = Vertex
        fields = ['name','x_val','y_val']

class DeleteNodeForm(forms.ModelForm):
    class Meta:
        model = Vertex
        fields = ['name']

class AddEdgeForm(forms.Form):
    VertexOne = forms.CharField(max_length=20)
    VertexTwo = forms.CharField(max_length=20)

class DeleteEdgeForm(forms.Form):
    VertexOne = forms.CharField(max_length=20)
    VertexTwo = forms.CharField(max_length=20)


        
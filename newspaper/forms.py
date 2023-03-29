from django.contrib.auth.forms import UserCreationForm
from newspaper.models import Redactor


class RedactorCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + ("years_of_experience", "first_name", "last_name")


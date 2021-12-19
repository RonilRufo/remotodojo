import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    """
    Factory test for :model:`accounts.CustomUser`
    """

    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ("email",)

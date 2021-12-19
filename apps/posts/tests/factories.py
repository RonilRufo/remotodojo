import factory


class PostFactory(factory.django.DjangoModelFactory):
    """
    Factory test for :model:`posts.Post`
    """

    class Meta:
        model = "posts.Post"

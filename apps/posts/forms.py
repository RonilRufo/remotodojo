from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Form to be used to create/edit a post.
    """

    class Meta:
        model = Post
        fields = ("content", "is_published", "is_public")
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Post something here...",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_published"].label = "Publish"
        self.fields["is_public"].label = "Make Post Public"
        self.fields["is_published"].widget.attrs["class"] = "form-check-input"
        self.fields["is_public"].widget.attrs["class"] = "form-check-input"

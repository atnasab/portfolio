from django import forms
import bleach


ALLOWED_TAGS = []  # no HTML in contact messages


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "your@email.com", "autocomplete": "email"}),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Subject"}),
    )
    message = forms.CharField(
        max_length=3000,
        widget=forms.Textarea(attrs={"placeholder": "Your message…", "rows": 6}),
    )
    # Honeypot field — must stay empty
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        """Honeypot: reject if filled."""
        val = self.cleaned_data.get("website", "")
        if val:
            raise forms.ValidationError("Bot detected.")
        return val

    def clean_name(self):
        return bleach.clean(self.cleaned_data["name"], tags=ALLOWED_TAGS, strip=True)

    def clean_subject(self):
        return bleach.clean(self.cleaned_data["subject"], tags=ALLOWED_TAGS, strip=True)

    def clean_message(self):
        return bleach.clean(self.cleaned_data["message"], tags=ALLOWED_TAGS, strip=True)

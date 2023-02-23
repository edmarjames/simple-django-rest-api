from django.db                          import models

# import the User model
from django.contrib.auth.models         import User
# import the post_save signal
from django.db.models.signals           import post_save
# import the django receiver package
from django.dispatch                    import receiver
# import token model
from rest_framework.authtoken.models    import Token


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

# PostSave receiver - will generate a new token when a new user has been created
@receiver(post_save, sender=User)
# sender - will be the user that is saved to the database
def generate_auth_token(sender, instance=None, created=False, **kwargs):

    # if user is created
    if created:
        # create a token for that user
        Token.objects.create(user=instance)
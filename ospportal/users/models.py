import random, os
from django.db import models
#from django.contrib.auth.models import User
from core.models import User
from PIL import Image


#Get file extention
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,9999999999)
    name, ext = get_filename_ext(filename)
    final_filename ='{new_filename}{ext}'.format(new_filename=new_filename, ext=ext) #f'{new_filename}{ext}'

    return "profil_pics/{new_filename}".format(
            new_filename=new_filename, final_filename=final_filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. Similar to `bio`, this field is not required. It may be blank.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    address = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False, verbose_name="City")
    country = models.CharField(max_length=100, blank=False, null=False, verbose_name="Country")
    loc_lat = models.CharField(max_length=20, blank=False, null=False, verbose_name="Latitude")
    loc_lng = models.CharField(max_length=20, blank=False, null=False, verbose_name="Longitude")


    def __str__(self):
        return f'{self.user.username} Profile'

    #overide the inbuilt save method
    #def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


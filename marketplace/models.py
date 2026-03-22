from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)


class Hobby(models.Model):
    class OutputType(models.TextChoices):
        PRODUCT = "P", _("Product")
        SERVICE = "S", _("Service")
        ITEM = "I", _("Item")

    output_type = models.CharField(
        max_length=1,
        choices=OutputType,
        default=OutputType.PRODUCT,
    )
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hobby"
        verbose_name_plural = "Hobbies"


class UserHasHobby(models.Model):
    hobby   = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Claimed hobby"
        verbose_name_plural = "Claimed hobbies"


class Vote(models.Model):
    hobby = models.ForeignKey(
        Hobby,
        related_name="votes",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

class Offering(models.Model):
    class OfferingType(models.TextChoices):
        PRODUCT = "P", _("Product")
        SERVICE = "S", _("Service")

    class StockStatus(models.TextChoices):
        IN_STOCK = "I", _("In stock")
        OUT_OF_STOCK = "O", _("Out of stock")
        MADE_ON_DEMAND = "D", _("Made on demand")


    name = models.CharField(max_length=100)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    offering_type = models.CharField(
        max_length=1,
        choices=OfferingType,
        default=OfferingType.PRODUCT,
    )
    stock_status = models.CharField(
        max_length=1,
        choices=StockStatus,
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to='offerings/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None and self.photo:
            image = Image.open(self.photo) 
                
            if image.mode in ("RGBA", "P", "LA"):
                image = image.convert("RGB")
            elif image.mode != "RGB":
                image = image.convert("RGB")
                
            image.thumbnail((600, 600), Image.Resampling.LANCZOS)
                
            output = BytesIO()
            image.save(output, format='AVIF', quality=50, speed=8)
            output.seek(0)
                
            original_name = os.path.splitext(os.path.basename(self.photo.name))[0]
            self.photo = ContentFile(output.getvalue(), f"{original_name}.avif")
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Offering"
        verbose_name_plural = "Offerings"

    def __str__(self):
        return self.name

class Trade(models.Model):
    class TradeStatus(models.TextChoices):
        PENDING = "P", _("Pending")
        ACCEPTED = "A", _("Accepted")
        REJECTED = "R", _("Rejected")
        TOO_LOW = "T", _("Too low price")

    target_offering = models.ForeignKey(Offering, related_name='incoming_trades', on_delete=models.CASCADE)
    offered_offering = models.ForeignKey(Offering, related_name='outgoing_trades', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    message = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=TradeStatus,
        default=TradeStatus.PENDING,
    )
    proposer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
    
class Gang(models.Model):
        name = models.CharField(max_length=50)
        description = models.CharField(max_length=100)
        creator = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='led_gangs'
        )

        members = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='gangs',
            blank=True
        )

        def __str__(self):
            return self.name
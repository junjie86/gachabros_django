from django.db.models.signals import post_save
from django.dispatch import receiver
from wallet.models import Wallet
from core.models import Profile

@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    """Create a Wallet when a Profile is created"""
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def save_wallet(sender, instance, **kwargs):
    """Save the Wallet when the Profile is saved"""
    instance.wallet.save()
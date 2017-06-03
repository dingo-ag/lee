from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    phone = models.CharField(_('Phone'), max_length=25)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def get_short_name(self):
        return str(self.first_name).capitalize()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).capitalize()


class ShippingAddress(models.Model):
    class DeliveryType:
        HOME_TO_HOME = 1
        OFFICE_TO_HOME = 2
        HOME_TO_OFFICE = 3
        OFFICE_TO_OFFICE = 4

        all_types = (
            (HOME_TO_HOME, _('From home to home')),
            (OFFICE_TO_HOME, _('From office to home')),
            (HOME_TO_OFFICE, _('From home to office')),
            (OFFICE_TO_OFFICE, _('From office to office')),
        )

        user_types = (
            (OFFICE_TO_HOME, _('To the door')),
            (OFFICE_TO_OFFICE, _('To the office of transport company')),
        )

    user = models.ForeignKey('User', verbose_name=_('Address owner'), on_delete=models.CASCADE)
    first_name = models.CharField(_('Contact first name'), max_length=50)
    last_name = models.CharField(_('Contact last name'), max_length=50)
    phone = models.CharField(_('Contact phone'), max_length=50)
    country = models.CharField(_('Country'), max_length=100, default=_('Ukraine'))
    city_village = models.CharField(_('City or village'), max_length=100, default=_('Kiev'))
    street = models.CharField(_('Street'), max_length=100, blank=True)
    building = models.CharField(_('Building'), max_length=100, blank=True)
    apartments = models.CharField(_('Apartments'), max_length=100, blank=True)
    postcode = models.CharField(_('Post code'), max_length=10, blank=True)
    delivery_type = models.IntegerField(_('Delivery type'), choices=DeliveryType.user_types,
                                        default=DeliveryType.OFFICE_TO_OFFICE)
    delivery_service = models.ForeignKey('shop.DeliveryService')

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.postcode, self.city_village, self.street, self.building,
                                          '/' if self.apartments else '', self.apartments)


class Wishlist(models.Model):
    user = models.ForeignKey('User', verbose_name=_('Wishlist owner'), on_delete=models.CASCADE)

    def __str__(self):
        return 'Wishlist of {}'.format(self.user.email)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', verbose_name=_('Product'), on_delete=models.SET_NULL, null=True)
    private = models.BooleanField(verbose_name=_('Is private'), default=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.product.name)

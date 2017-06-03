from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    class Statuses:
        IN_STOCK = 1
        OUT_OF_STOCK = 2
        DISCONTINUED = 3

        NOVELTY = 1
        ENDS = 2
        TOP_OF_SALES = 3

        choices = (
            (IN_STOCK, _('Product in stock')),
            (OUT_OF_STOCK, _('Sorry, but product ended')),
            (DISCONTINUED, _('Product is discontinued')),
        )

        additional_choices = (
            (NOVELTY, _('Novelty')),
            (ENDS, _('Ends')),
            (TOP_OF_SALES, _('Top of sales')),

        )

    name = models.CharField(_('Name'), max_length=255)
    image = models.FileField(_('Image'), default='shop/products/images/no_image.png')
    category = models.ForeignKey('Category', verbose_name=_('Category'), on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2, default=0)
    added = models.DateTimeField(_('Added to stock'), auto_now_add=True)
    description = models.TextField(_('Description'), blank=True)
    characteristics = JSONField(_('Characteristics'), blank=True)
    status = models.IntegerField(_('Status'), choices=Statuses.choices, default=Statuses.IN_STOCK)
    additional_status = models.IntegerField(_('Additional status'), choices=Statuses.additional_choices,
                                            default=Statuses.NOVELTY)
    size = models.CharField(_('Size'), max_length=100, default=_('Unknown'))
    weight = models.IntegerField(_('Weight'), default=0)
    total_count = models.IntegerField(_('Count'), default=0)
    discount = models.IntegerField(_('Discount'), default=0)  # Discount in percents from common price
    manufacturer = models.ForeignKey('Manufacturer', verbose_name=_('Manufacturer'), blank=True, null=True)
    product_code = models.CharField(_('Product code'), max_length=255, blank=True)

    def __str__(self):
        return self.name.capitalize()


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    parent_category = models.ForeignKey('self', verbose_name=_('Parent category'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True)
    picture = models.FileField(_('Picture'), default='shop/categories/images/no_image.png')
    active = models.BooleanField(_('Is active'), default=True)

    def __str__(self):
        return self.name.capitalize()


class Manufacturer(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    site = models.CharField(_('Official Site'), max_length=150, blank=True)
    short_description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name.capitalize()


class Comment(models.Model):
    class Rating:
        POOR = 1
        FAIR = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5

        choices = (
            (POOR, _('Poor')),
            (FAIR, _('Fair')),
            (AVERAGE, _('Average')),
            (GOOD, _('Good')),
            (EXCELLENT, _('Excellent'))
        )

    parent_comment = models.ForeignKey('self', verbose_name=_('Reply for'), blank=True, null=True)
    user = models.ForeignKey('users.User', verbose_name=_('Comment owner'))
    product = models.ForeignKey('Product', verbose_name=_('About product'))
    rating = models.IntegerField(_('Rating'), choices=Rating.choices, default=Rating.GOOD)
    review = models.TextField(default=_('Good'))


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(_('Count'), default=1)
    item_price = models.DecimalField(_('Item cost'), max_digits=12, decimal_places=2, default=0)

    def item_price_update(self):
        self.item_price = self.product.price * self.count


class Order(models.Model):
    class Statuses:
        NOT_ORDERED = 1
        NOT_PROCESSED = 2
        PROCESSED = 3
        ASSEMBLED = 4
        SENT = 5
        DELIVERED = 6

        choices = (
            (NOT_ORDERED, _('Shopping is continued')),
            (NOT_PROCESSED, _('Order created, but not processed')),
            (PROCESSED, _('Order processed and waiting for assembly')),
            (ASSEMBLED, _('Order assembled and wait for sent')),
            (SENT, _('Order was sent')),
            (DELIVERED, _('Order delivered')),
        )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.IntegerField(_('Status'), choices=Statuses.choices, default=Statuses.NOT_ORDERED)
    order_price = models.DecimalField(_('Order price'), max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    ordered = models.DateTimeField(_('Ordered'), null=True)
    delivery_service = models.ForeignKey('DeliveryService', blank=True, null=True)
    shipping_address = models.ForeignKey('users.ShippingAddress', on_delete=models.DO_NOTHING, blank=True, null=True)
    tracking_number = models.CharField(_('Tracking number'), max_length=255, blank=True)
    total_weight = models.IntegerField(_('Weight'), default=0)
    total_size = models.CharField(_('Size'), max_length=100, blank=True)
    shipping_cost = models.DecimalField(_('Shipping cost'), max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(_('Total cost'), max_digits=12, decimal_places=2, default=0)
    description = models.TextField(_('Description'), blank=True)
    system_comment = models.TextField(_('Working information'), blank=True)

    def __str__(self):
        return '{} #{}'.format(str(_('Order')), self.id)


class DeliveryService(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    site = models.CharField(_('Site'), max_length=100)
    calculator_link = models.CharField(_('Calculator'), max_length=150, blank=True)

    def __str__(self):
        return self.name.capitalize()

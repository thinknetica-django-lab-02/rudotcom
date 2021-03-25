from main.models import *

c = Category(name='Аксессуары', slug='accessories')
c.save()
c1 = Category(name='Брелоки', parent=c, slug='keychains')
c1.save()

category = Category.objects.get(slug='accessories')
vendor = Vendor.objects.get(pk=1)

i1 = Item(vendor=vendor, category=category, title='Брелок "Цепь"', description='Цепочка', price=299, quantity=10)
i1.save()

i2 = Item.objects.create(vendor=vendor, category=category, title='Брелок "Ремешок"', description='Ремешок', price=299, quantity=10)

items = Item.objects.all()[:5]
items

keychains = Item.objects.filter(title__startswith='Брелок')
keychains = keychains.exclude(description__icontains='Цеп')

Item.objects.filter(tag__string='таро')
Item.objects.filter(tag__string__icontains='р').distinct()

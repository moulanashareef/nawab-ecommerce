from pathlib import Path
import shutil
from decimal import Decimal
import os

# Initialize Django BEFORE importing models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

import django
django.setup()

from django.db import transaction, connection
from django.core.management.color import no_style
from store.models import Product, Category

# Exact Nawab catalog: id|category|name|price|image-slug
DATA = '''
1|Fashion|Classic Cotton T-Shirt|799|classic-cotton-tshirt
2|Fashion|Slim Fit Jeans|1499|slim-fit-jeans
3|Fashion|Casual Hoodie|1299|casual-hoodie
4|Fashion|Denim Jacket|1999|denim-jacket
5|Fashion|Casual Shirt|999|casual-shirt
6|Fashion|Formal Shirt|1199|formal-shirt
7|Fashion|Cargo Pants|1399|cargo-pants
8|Fashion|Track Pants|899|track-pants
9|Fashion|Oversized T-Shirt|849|oversized-tshirt
10|Fashion|Polo T-Shirt|899|polo-tshirt
11|Fashion|Bomber Jacket|2199|bomber-jacket
12|Fashion|Leather Jacket|2999|leather-jacket
13|Fashion|Chinos|1299|chinos
14|Fashion|Linen Shirt|1099|linen-shirt
15|Fashion|Printed Shirt|999|printed-shirt
16|Fashion|Sweatshirt|1199|sweatshirt
17|Fashion|Winter Sweater|1599|winter-sweater
18|Fashion|Sports Shorts|699|sports-shorts
19|Fashion|Running Shorts|749|running-shorts
20|Fashion|Kurta|1299|kurta
21|Fashion|Casual Sneakers|1799|casual-sneakers
22|Fashion|Running Shoes|2299|running-shoes
23|Fashion|Canvas Shoes|1499|canvas-shoes
24|Fashion|Baseball Cap|499|baseball-cap
25|Fashion|Leather Belt|699|leather-belt
26|Fashion|Classic Wallet|799|classic-wallet
27|Fashion|Sunglasses|999|sunglasses
28|Fashion|Backpack|1299|backpack
29|Fashion|Analog Watch|1999|analog-watch
30|Fashion|Fashion Scarf|599|fashion-scarf
31|Home|Modern Table Lamp|899|modern-table-lamp
32|Home|LED Ceiling Light|1299|led-ceiling-light
33|Home|Decorative Wall Clock|799|decorative-wall-clock
34|Home|Ceramic Vase|599|ceramic-vase
35|Home|Cushion Set|699|cushion-set
36|Home|Cotton Bedsheet|999|cotton-bedsheet
37|Home|Soft Blanket|1299|soft-blanket
38|Home|Bath Towel Set|799|bath-towel-set
39|Home|Kitchen Storage Set|899|kitchen-storage-set
40|Home|Non-Stick Frying Pan|999|non-stick-frying-pan
41|Home|Stainless Steel Bottle|599|stainless-steel-bottle
42|Home|Electric Kettle|1199|electric-kettle
43|Home|Coffee Maker|2499|coffee-maker
44|Home|Dinner Set|1599|dinner-set
45|Home|Glass Tumbler Set|499|glass-tumbler-set
46|Home|Kitchen Knife Set|899|kitchen-knife-set
47|Home|Wooden Cutting Board|499|wooden-cutting-board
48|Home|Storage Organizer|699|storage-organizer
49|Home|Laundry Basket|799|laundry-basket
50|Home|Floor Mat|499|floor-mat
51|Home|Artificial Plant|699|artificial-plant
52|Home|Scented Candle|399|scented-candle
53|Home|Photo Frame|349|photo-frame
54|Home|Wall Art|899|wall-art
55|Home|Table Runner|499|table-runner
56|Home|Curtain Set|1199|curtain-set
57|Home|Pillow Set|699|pillow-set
58|Home|Bathroom Organizer|599|bathroom-organizer
59|Home|Laundry Bag|399|laundry-bag
60|Home|Decorative Mirror|1499|decorative-mirror
61|Gaming|Gaming Mouse|1299|gaming-mouse
62|Gaming|Mechanical Gaming Keyboard|2499|mechanical-keyboard
63|Gaming|Gaming Headset|1999|gaming-headset
64|Gaming|RGB Gaming Mouse Pad|999|rgb-mouse-pad
65|Gaming|Gaming Controller|2299|gaming-controller
66|Gaming|Gaming Chair|8999|gaming-chair
67|Gaming|Gaming Desk|6999|gaming-desk
68|Gaming|USB Gaming Microphone|2499|usb-gaming-microphone
69|Gaming|Webcam|1999|webcam
70|Gaming|Gaming Speakers|1799|gaming-speakers
71|Gaming|RGB LED Strip|799|rgb-led-strip
72|Gaming|Console Stand|899|console-stand
73|Gaming|Controller Charging Dock|1299|controller-charging-dock
74|Gaming|Gaming Laptop Stand|1199|gaming-laptop-stand
75|Gaming|VR Headset|8999|vr-headset
76|Gaming|Portable Gaming Console|5999|portable-gaming-console
77|Gaming|Gaming Earbuds|1599|gaming-earbuds
78|Gaming|Gaming Keypad|1499|gaming-keypad
79|Gaming|Streaming Light|1299|streaming-light
80|Gaming|Gaming Capture Card|3999|capture-card
81|Gaming|Game Controller Grip|499|controller-grip
82|Gaming|Gaming Finger Sleeves|299|gaming-finger-sleeves
83|Gaming|Gaming Cooling Pad|1499|cooling-pad
84|Gaming|Gaming Monitor Stand|1799|monitor-stand
85|Gaming|RGB Desk Mat|999|rgb-desk-mat
86|Gaming|Game Storage Case|699|game-storage-case
87|Gaming|Gaming Backpack|1799|gaming-backpack
88|Gaming|Headset Stand|799|headset-stand
89|Gaming|Gaming Cable Organizer|399|cable-organizer
90|Gaming|RGB Gaming Controller|2699|rgb-gaming-controller
91|Electronics|Smartphone|14999|smartphone
92|Electronics|Tablet|12999|tablet
93|Electronics|Laptop|49999|laptop
94|Electronics|Smart TV|29999|smart-tv
95|Electronics|Bluetooth Speaker|1999|bluetooth-speaker
96|Electronics|Wireless Earbuds|1499|wireless-earbuds
97|Electronics|Smartwatch|2999|smartwatch
98|Electronics|Power Bank|999|power-bank
99|Electronics|Wireless Charger|899|wireless-charger
100|Electronics|USB-C Charger|799|usb-c-charger
101|Electronics|Bluetooth Headphones|1999|bluetooth-headphones
102|Electronics|Digital Camera|29999|digital-camera
103|Electronics|Action Camera|6999|action-camera
104|Electronics|Portable Projector|7999|portable-projector
105|Electronics|Smart Home Hub|2499|smart-home-hub
106|Electronics|Wi-Fi Router|1799|wifi-router
107|Electronics|Bluetooth Adapter|499|bluetooth-adapter
108|Electronics|USB Hub|799|usb-hub
109|Electronics|External SSD|4999|external-ssd
110|Electronics|External Hard Drive|4499|external-hard-drive
111|Electronics|Computer Monitor|9999|computer-monitor
112|Electronics|Wireless Keyboard|1299|wireless-keyboard
113|Electronics|Wireless Mouse|899|wireless-mouse
114|Electronics|Laser Printer|7999|laser-printer
115|Electronics|Smart Doorbell|3499|smart-doorbell
116|Electronics|Security Camera|2499|security-camera
117|Electronics|Digital Alarm Clock|699|digital-alarm-clock
118|Electronics|Smart Plug|699|smart-plug
119|Electronics|Electric Shaver|1499|electric-shaver
120|Electronics|Electric Trimmer|999|electric-trimmer
121|Accessories|Leather Wallet|699|leather-wallet
122|Accessories|Travel Backpack|1499|travel-backpack
123|Accessories|Laptop Backpack|1799|laptop-backpack
124|Accessories|Phone Case|399|phone-case
125|Accessories|Screen Protector|299|screen-protector
126|Accessories|USB-C Cable|399|usb-c-cable
127|Accessories|Lightning Cable|499|lightning-cable
128|Accessories|Car Phone Holder|599|car-phone-holder
129|Accessories|Phone Stand|399|phone-stand
130|Accessories|Laptop Stand|999|laptop-stand
131|Accessories|Cable Organizer|299|cable-organizer
132|Accessories|Travel Adapter|799|travel-adapter
133|Accessories|Keychain|199|keychain
134|Accessories|Card Holder|499|card-holder
135|Accessories|Sunglasses Case|299|sunglasses-case
136|Accessories|Wristband|249|wristband
137|Accessories|Fitness Band Strap|399|fitness-band-strap
138|Accessories|Watch Strap|499|watch-strap
139|Accessories|Key Organizer|599|key-organizer
140|Accessories|Travel Pouch|699|travel-pouch
141|Accessories|Passport Holder|599|passport-holder
142|Accessories|Luggage Tag|299|luggage-tag
143|Accessories|Travel Neck Pillow|799|travel-neck-pillow
144|Accessories|Foldable Umbrella|599|foldable-umbrella
145|Accessories|Waterproof Pouch|399|waterproof-pouch
146|Accessories|Reusable Shopping Bag|249|reusable-shopping-bag
147|Accessories|Minimalist Key Ring|199|minimalist-key-ring
148|Accessories|Cable Clips|199|cable-clips
149|Accessories|Desk Organizer|699|desk-organizer
150|Accessories|Multi-Purpose Pouch|499|multi-purpose-pouch
'''

CATALOG = [
    (int(a), b, c, int(d), e)
    for line in DATA.strip().splitlines()
    for a,b,c,d,e in [line.split('|')]
]

BASE = Path(__file__).resolve().parent
SOURCE_IMAGES = BASE / 'images'
STATIC_IMAGES = BASE / 'static' / 'images'

@transaction.atomic
def sync():
    if len(CATALOG) != 150 or [x[0] for x in CATALOG] != list(range(1, 151)):
        raise RuntimeError('Catalog validation failed: expected exact IDs 1-150.')

    categories = {c.name: c for c in Category.objects.all()}
    needed = {'Fashion','Home','Gaming','Electronics','Accessories'}
    missing_categories = needed - categories.keys()
    if missing_categories:
        raise RuntimeError(f'Missing categories: {sorted(missing_categories)}')

    missing_images = []
    for _, category, _, _, slug in CATALOG:
        src = SOURCE_IMAGES / category.lower() / f'{slug}.jpg'
        if not src.exists():
            missing_images.append(str(src))
    if missing_images:
        raise RuntimeError('Missing local images:\n' + '\n'.join(missing_images))

    # No OrderItem rows exist, so replacing the old catalog is safe.
    Product.objects.all().delete()

    products = []
    for pid, category, name, price, slug in CATALOG:
        src = SOURCE_IMAGES / category.lower() / f'{slug}.jpg'
        dst = STATIC_IMAGES / category.lower() / f'{slug}.jpg'
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        products.append(Product(
            id=pid,
            name=name,
            category=categories[category],
            description=f'{name} from Nawab.',
            price=Decimal(str(price)),
            image=f'/static/images/{category.lower()}/{slug}.jpg',
            stock=100,
            rating=Decimal('4.5'),
        ))

    Product.objects.bulk_create(products)

    try:
        sql = connection.ops.sequence_reset_sql(no_style(), [Product])
        with connection.cursor() as cursor:
            for statement in sql:
                cursor.execute(statement)
    except Exception:
        pass

    print('DONE: Nawab catalog replaced.')
    print('PRODUCT COUNT:', Product.objects.count())
    print('ID RANGE:', Product.objects.order_by('id').first().id, 'to', Product.objects.order_by('-id').first().id)
    print('ID 1:', Product.objects.get(id=1).name, '|', Product.objects.get(id=1).image)
    print('ID 142:', Product.objects.get(id=142).name, '|', Product.objects.get(id=142).image)
    print('ID 150:', Product.objects.get(id=150).name, '|', Product.objects.get(id=150).image)

if __name__ == "__main__":
    sync()

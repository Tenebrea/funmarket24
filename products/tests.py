from django.test import TestCase
from django.urls import reverse

from .models import Category, Chip, Product


class CatalogFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.chip = Chip.objects.create(name='Хит', color='#EB6279')
        cls.category = Category.objects.create(name='Шары', slug='shary')
        cls.other = Category.objects.create(name='Наборы', slug='nabory')

        def make(pk, **kwargs):
            defaults = {
                'artikul': f'{pk:06d}',
                'brand': 'Бренд',
                'in_stock': 10,
                'price_in_bulk': 900,
                'size': "14''",
                'color': 'Матовый',
                'material': 'Латекс',
                'theme': 'Праздник',
                'form': 'Круг',
                'category': cls.category,
                'chip': cls.chip,
            }
            defaults.update(kwargs)
            return Product.objects.create(id=pk, **defaults)

        make(1, title='BelBal красный', manufacturer='BelBal', price=990, color='Красный')
        make(2, title='Sempertex синий', manufacturer='Sempertex', price=1500, color='Синий', size="5''")
        make(3, title='Sempertex зелёный', manufacturer='Sempertex', price=3000, color='Зелёный')
        make(4, title='Чужой', manufacturer='BelBal', price=100, category=cls.other)

    def get_ids(self, **params):
        response = self.client.get(reverse('products:catalog', args=[self.category.slug]), params)
        self.assertEqual(response.status_code, 200)
        return [p.id for p in response.context['products']]

    def test_no_filters_returns_category_products(self):
        self.assertEqual(self.get_ids(), [1, 2, 3])

    def test_manufacturer_filter(self):
        self.assertEqual(self.get_ids(manufacturer='BelBal'), [1])

    def test_manufacturer_radio_keeps_selection(self):
        url = reverse('products:catalog', args=[self.category.slug])
        response = self.client.get(url, {'manufacturer': 'BelBal'})
        html = response.content.decode()
        self.assertIn('name="manufacturer" value="BelBal" checked', html)
        self.assertIn('name="manufacturer" value=""', html)

    def test_price_filter(self):
        self.assertEqual(self.get_ids(price_min=1000, price_max=2000), [2])

    def test_multi_value_filters(self):
        self.assertEqual(self.get_ids(size=["14''", "5''"]), [1, 2, 3])
        self.assertEqual(self.get_ids(color=['Красный', 'Зелёный']), [1, 3])

    def test_material_theme_form_filters(self):
        self.assertEqual(self.get_ids(material='Латекс'), [1, 2, 3])
        self.assertEqual(self.get_ids(theme='Праздник'), [1, 2, 3])
        self.assertEqual(self.get_ids(form='Круг'), [1, 2, 3])

    def test_sorting(self):
        self.assertEqual(self.get_ids(sort='-price'), [3, 2, 1])
        self.assertEqual(self.get_ids(sort='title'), [1, 3, 2])

    def test_unknown_sort_falls_back_to_price(self):
        self.assertEqual(self.get_ids(sort='bogus'), [1, 2, 3])

    def test_price_bounds_come_from_category(self):
        response = self.client.get(reverse('products:catalog', args=[self.category.slug]))
        self.assertEqual(response.context['price_lo'], 990)
        self.assertEqual(response.context['price_hi'], 3000)

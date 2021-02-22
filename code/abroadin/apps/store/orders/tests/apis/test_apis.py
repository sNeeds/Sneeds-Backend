from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status, serializers

from abroadin.apps.store.carts.models import Cart
from abroadin.apps.store.orders.models import Order
from abroadin.apps.store.storeBase.serializers import SoldTimeSlotSaleSerializer
from abroadin.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class OrderTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()

    def test_selling_cart_deletes_sold_products_from_other_carts(self):
        cart1_time_slot_sales = self.cart1.products.all().get_time_slot_sales()
        cart1_time_slot_sales_id = [obj.id for obj in cart1_time_slot_sales]

        cart2_time_slot_sales = self.cart2.products.all().get_time_slot_sales()
        cart2_time_slot_sales_id = [obj.id for obj in cart2_time_slot_sales]

        cart1_cart2_time_slot_sales_intersection = list(set(cart1_time_slot_sales_id) & set(cart2_time_slot_sales_id))
        if len(cart1_cart2_time_slot_sales_intersection) == 0:
            has_common_time_slot_sales = False
        else:
            has_common_time_slot_sales = True

        self.assertEqual(has_common_time_slot_sales, True)

        # Order creation
        Order.objects.sell_cart_create_order(self.cart1)

        cart2_time_slot_sales = self.cart2.products.all().get_time_slot_sales()
        cart2_time_slot_sales_id = [obj.id for obj in cart2_time_slot_sales]

        if len(list(set(cart1_cart2_time_slot_sales_intersection) & set(cart2_time_slot_sales_id))) == 0:
            has_common_time_slot_sales = False
        else:
            has_common_time_slot_sales = True

        self.assertEqual(has_common_time_slot_sales, False)

    def test_selling_cart_works(self):
        class TempTimeSlotSale:
            def __init__(self, consultant, price, start_time, end_time):
                self.consultant = consultant
                self.price = price
                self.start_time = start_time
                self.end_time = end_time

        self.cart1.refresh_from_db()

        cart1_time_slot_sales_qs = self.cart1.products.all().get_time_slot_sales()

        cart1_temp_time_slot_sales_list = []
        for obj in cart1_time_slot_sales_qs:
            cart1_temp_time_slot_sales_list.append(
                TempTimeSlotSale(obj.consultant, obj.price, obj.start_time, obj.end_time)
            )

        cart1_user = self.cart1.user
        cart1_total = self.cart1.total
        cart1_subtotal = self.cart1.subtotal

        self.cart1.refresh_from_db()
        order = Order.objects.sell_cart_create_order(self.cart1)

        order_sold_time_slot_sales = order.sold_products.all().get_sold_time_slot_sales()
        for sold_time_slot_sale in order_sold_time_slot_sales:
            self.assertEqual(
                order_sold_time_slot_sales.filter(
                    sold_to=cart1_user,
                    consultant=sold_time_slot_sale.consultant,
                    price=sold_time_slot_sale.price,
                    start_time=sold_time_slot_sale.start_time,
                    end_time=sold_time_slot_sale.end_time
                ).count(),
                1
            )

        self.assertEqual(order.user, cart1_user)
        self.assertEqual(order.status, "paid")
        self.assertEqual(order.total, cart1_total)
        self.assertEqual(order.subtotal, cart1_subtotal)

    def test_orders_list_get_pass(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = reverse("order:order-list", )
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted([obj.get("id") for obj in response.data]),
            sorted([order1.id, order2.id])
        )

    def test_orders_list_get_pass_with_permissions(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order3 = Order.objects.sell_cart_create_order(self.cart3)

        url = reverse("order:order-list", )
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted([obj.get("id") for obj in response.data]),
            sorted([order1.id])
        )
        self.assertFalse(order3.id in [obj.get("id") for obj in response.data])

    def test_orders_list_get_pass_created_ordering(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = "%s?%s=%s" % (reverse("order:order-list"), "ordering", "created")

        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [obj.get("id") for obj in response.data],
            [order1.id, order2.id]
        )

    def test_orders_list_get_pass_created_ordering_descending(self):
        order1 = Order.objects.sell_cart_create_order(self.cart1)
        order2 = Order.objects.sell_cart_create_order(self.cart2)

        url = "%s?%s=%s" % (reverse("order:order-list"), "ordering", "-created")
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            [obj.get("id") for obj in response.data],
            [order2.id, order1.id]
        )

    def test_orders_detail_pass(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        order1 = Order.objects.sell_cart_create_order(self.cart1)

        url = reverse("order:order-detail", args=(order1.id,))

        response = client.get(url, format='json')
        request = response.wsgi_request
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("id"), order1.id)
        self.assertEqual(response_data.get("order_id"), order1.order_id)
        self.assertEqual(response_data.get("status"), order1.status)
        self.assertEqual(
            response_data.get("sold_time_slot_sales"),
            SoldTimeSlotSaleSerializer(
                order1.sold_products.all().get_sold_time_slot_sales(), context={"request": request}, many=True
            ).data
        )
        self.assertEqual(
            response.data.get("created"),
            serializers.DateTimeField().to_representation(order1.created)
        )
        self.assertEqual(
            response.data.get("updated"),
            serializers.DateTimeField().to_representation(order1.updated)
        )
        self.assertEqual(response_data.get("subtotal"), order1.subtotal)
        self.assertEqual(response_data.get("total"), order1.total)

    def test_orders_detail_permission(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        order1 = Order.objects.sell_cart_create_order(self.cart1)

        url = reverse("order:order-detail", args=(order1.id,))
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_orders_list_post_fail(self):
        url = reverse("order:order-list", )
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        payload = {
            "sold_products": [p.id for p in self.cart2.products.all()],
            "user": self.user1.id,
        }
        response = client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_order_detail_put_patch_delete_post_denied(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')

        order1 = Order.objects.sell_cart_create_order(self.cart1)
        paylaod = {
            "subtotal": 5
        }
        url = reverse("order:order-detail", args=(order1.id,))

        response = client.post(url, paylaod, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.patch(url, paylaod, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.put(url, paylaod, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

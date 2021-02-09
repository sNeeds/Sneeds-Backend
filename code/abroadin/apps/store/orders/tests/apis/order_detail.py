from rest_framework import status

from .base import OrderAPITestBase


class OrderDetailAPITests(OrderAPITestBase):
    def setUp(self):
        super().setUp()

    def _test_order_detail(self, *args, **kwargs):
        return self._endpoint_test_method('store.order:order-detail', *args, **kwargs)

    def test_get_orders_200_1(self):
        res = self._test_order_detail('get', self.user1, status.HTTP_200_OK, reverse_args=self.a_order_1.id)

    def test_get_orders_403_1(self):
        res = self._test_order_detail('get', self.user2, status.HTTP_403_FORBIDDEN, reverse_args=self.a_order_1.id)

    def test_get_orders_401_1(self):
        res = self._test_order_detail('get', None, status.HTTP_401_UNAUTHORIZED, reverse_args=self.a_order_1.id)

    def test_list_orders_post_405(self):
        res = self._test_order_detail('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={}, reverse_args=self.a_order_1.id)

    def test_list_orders_put_405(self):
        res = self._test_order_detail('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={}, reverse_args=self.a_order_1.id)

    def test_list_orders_patch_405(self):
        res = self._test_order_detail('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={}, reverse_args=self.a_order_1.id)
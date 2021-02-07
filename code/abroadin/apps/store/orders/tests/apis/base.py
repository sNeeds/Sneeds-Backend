from rest_framework import status

from ..base import OrderTestBase


class OrderAPITestBase(OrderTestBase):

    def setUp(self):
        super().setUp()

    def _test_order_list(self, *args, **kwargs):
        return self._endpoint_test_method('store.order:order-list', *args, **kwargs)

    def test_get_orders_200_1(self):
        res = self._test_order_list('get',  self.user1, status.HTTP_200_OK)
        self.assertEqual(len(res), 2)

    def test_get_orders_401_1(self):
        res = self._test_order_list('get', None, status.HTTP_401_UNAUTHORIZED)

    def test_list_orders_post_405(self):
        res = self._test_order_list('post', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,  data={})

    def test_list_orders_put_405(self):
        res = self._test_order_list('put', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED, data={})

    def test_list_orders_patch_405(self):
        res = self._test_order_list('patch', self.user1, status.HTTP_405_METHOD_NOT_ALLOWED,  data={})



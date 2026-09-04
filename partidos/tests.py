from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto, Pedido
from partidos.dao.partidos_dao import ProductoDAO, PedidoDAO


class CafeteriaTestCase(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Café Americano",
            precio=45.00,
            disponible=True,
            categoria="BEBIDA"
        )
        self.staff_user = User.objects.create_user(
            username='cocina_test',
            password='password123',
            is_staff=True
        )

    def test_crear_pedido_dao(self):
        pedido = PedidoDAO.crear_pedido_con_producto("Carlos", self.producto.id)
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.cliente_nombre, "Carlos")
        self.assertEqual(pedido.total, 45.00)

    def test_cambiar_estado_dao(self):
        pedido = PedidoDAO.crear_pedido_con_producto("Ana", self.producto.id)
        pedido_actualizado = PedidoDAO.cambiar_estado(pedido.id, "EN_PREPARACION")
        self.assertEqual(pedido_actualizado.estado, "EN_PREPARACION")

    ## para probar los endpoint rest, verifica que la api nos responda
    def test_api_list_productos(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, 200)

    def test_crear_pedido_action_web(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('crear_pedido'), {
            'cliente_nombre': 'Yuri',
            'producto_id': self.producto.id
        })
        self.assertRedirects(response, reverse('cocina'))
        self.assertEqual(Pedido.objects.count(), 1)
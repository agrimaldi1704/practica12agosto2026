from typing import List, Optional
from partidos.models import Producto, Pedido


class ProductoDAO:
    """Capa DAO para operaciones de Productos"""

    @staticmethod
    def obtener_todos() -> List[Producto]:
        return Producto.objects.all()

    @staticmethod
    def obtener_disponibles() -> List[Producto]:
        return Producto.objects.filter(disponible=True)

    @staticmethod
    def obtener_por_id(producto_id: int) -> Optional[Producto]:
        try:
            return Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return None

    @staticmethod
    def crear_producto(nombre: str, precio: float, categoria: str, disponible: bool = True) -> Producto:
        """Alta de un nuevo producto"""
        return Producto.objects.create(
            nombre=nombre,
            precio=precio,
            categoria=categoria,
            disponible=disponible
        )

    @staticmethod
    def actualizar_producto(producto_id: int, **campos) -> Optional[Producto]:
        """Cambio de datos de un producto existente"""
        producto = ProductoDAO.obtener_por_id(producto_id)
        if producto:
            for campo, valor in campos.items():
                setattr(producto, campo, valor)
            producto.save()
            return producto
        return None

    @staticmethod
    def eliminar_producto(producto_id: int) -> bool:
        """Baja de un producto"""
        producto = ProductoDAO.obtener_por_id(producto_id)
        if producto:
            producto.delete()
            return True
        return False


class PedidoDAO:
    """Capa DAO para operaciones de Pedidos"""

    @staticmethod
    def obtener_todos() -> List[Pedido]:
        return Pedido.objects.all().order_by('-fecha')

    @staticmethod
    def obtener_por_id(pedido_id: int) -> Optional[Pedido]:
        try:
            return Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return None

    @staticmethod
    def crear_pedido_con_producto(cliente_nombre: str, producto_id: int) -> Optional[Pedido]:
        """Alta de un nuevo pedido, vinculado correctamente a su producto"""
        producto = ProductoDAO.obtener_por_id(producto_id)
        if producto:
            return Pedido.objects.create(
                cliente_nombre=cliente_nombre,
                producto=producto,
                total=producto.precio
            )
        return None

    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str) -> Optional[Pedido]:
        """Cambio del estado de un pedido"""
        pedido = PedidoDAO.obtener_por_id(pedido_id)
        if pedido:
            pedido.estado = nuevo_estado
            pedido.save()
            return pedido
        return None

    @staticmethod
    def eliminar_pedido(pedido_id: int) -> bool:
        """Baja de un pedido"""
        pedido = PedidoDAO.obtener_por_id(pedido_id)
        if pedido:
            pedido.delete()
            return True
        return False
import json
import aiofiles
import asyncio

ARCHIVO_BD = "Inventario.json"
db_lock = asyncio.Lock()  
async def leer_base_datos():
    try:
        async with aiofiles.open(ARCHIVO_BD, mode="r", encoding="utf-8") as f:
            contenido = await f.read()
            return json.loads(contenido)
    except FileNotFoundError:
        return []
async def guardar_base_datos(datos):
    async with aiofiles.open(ARCHIVO_BD, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(datos, indent=4, ensure_ascii=False))
async def crear_producto(codigo, nombre, stock):
    async with db_lock: 
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        for dato in datos:
            if dato["codigo"] == codigo:
                raise ValueError(f"El producto con el codigo {codigo} ya existe")
        nuevo_producto = {"codigo": codigo, "nombre": nombre, "stock": stock}
        datos.append(nuevo_producto)
        await guardar_base_datos(datos)
        return nuevo_producto
async def obtener_producto(codigo):
    await asyncio.sleep(0.2)
    datos = await leer_base_datos()
    for dato in datos:
        if dato["codigo"] == codigo:
            return dato
    raise KeyError(f"Producto {codigo} no ha sido encontrado.") 
async def actualizar_stock(nuevo_stock, codigo):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                dato["stock"] = nuevo_stock
                await guardar_base_datos(datos)
                return dato
        raise KeyError(f"Producto {codigo} no ha sido encontrado.")
async def eliminar_producto(codigo):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        nuevos_datos = [dato for dato in datos if dato["codigo"] != codigo]

        if len(datos) == len(nuevos_datos):
            raise KeyError(f"producto {codigo} no encontrado")

        await guardar_base_datos(nuevos_datos)
        return True
async def alerta_stock_bajo(codigo, nombre, stock_actual):
    """Simula el envío de una alerta en segundo plano cuando el stock es menor a 3."""
    await asyncio.sleep(2)
    print(f"\n ALERTA CRÍTICA: El producto {nombre} ({codigo}) ha bajado a {stock_actual} unidades. Solicitar restock inmediato.\n")

async def vender_producto(codigo, cantidad_vendida):
    """Realiza la venta de forma asíncrona validando stock y usando el bloqueo seguro (db_lock)."""
    async with db_lock:
        await asyncio.sleep(0.3)
        datos = await leer_base_datos()
        producto_encontrado = None
        for dato in datos:
            if dato["codigo"] == codigo:
                producto_encontrado = dato
                break

        if not producto_encontrado:
            raise KeyError(f"Producto {codigo} no ha sido encontrado.")
        stock_actual = producto_encontrado["stock"]
        if cantidad_vendida > stock_actual:
            raise ValueError(f"Stock insuficiente para el producto '{producto_encontrado['nombre']}'. Stock actual: {stock_actual}, Solicitado: {cantidad_vendida}.")
        stock_resultante = stock_actual - cantidad_vendida
        producto_encontrado["stock"] = stock_resultante
        await guardar_base_datos(datos)
        if stock_resultante < 3:
            asyncio.create_task(
                alerta_stock_bajo(codigo, producto_encontrado["nombre"], stock_resultante)
            )
        return {"codigo": codigo, "nombre": producto_encontrado["nombre"], "cantidad_vendida": cantidad_vendida, "stock_restante": stock_resultante, "mensaje": "Venta realizada con éxito"}
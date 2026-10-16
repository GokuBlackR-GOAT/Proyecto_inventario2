import asyncio
from database import crear_producto, obtener_producto, actualizar_stock, eliminar_producto, vender_producto

async def prueba_de_estres():
    print("Iniciando prueba...")
    
    
    tareas_creacion = [
        crear_producto("M001", "Llanta trasera", 10),
        crear_producto("M002", "Filtro de aire", 25),
        crear_producto("M003", "Bujía", 2), 
    ]
    try:
        await asyncio.gather(*tareas_creacion)
        print("Productos creados exitosamente.")
    except Exception as e:
        print(f"Error de creación (es posible que ya existan): {e}")

   
    print("\nActualizar y consultar...")
    try:
        resultado = await asyncio.gather(
            actualizar_stock(8, "M001"), 
            obtener_producto("M002")
        )
        print(" Operaciones mixtas completadas.")
        print(f"   Update devolvió: {resultado[0]}")
        print(f"   Get devolvió: {resultado[1]}")
    except Exception as e:
        print(f" Error en operaciones mixtas: {e}")

    print("\nProbando flujo de ventas concurrentes y alertas...")
    try:
        res_venta = await vender_producto("M003", 1)
        print(f" Venta procesada: {res_venta}")
    except Exception as e:
        print(f" Error en venta: {e}")
    print("\nEsperando tareas en segundo plano...")
    await asyncio.sleep(3)
    print("=== FIN DE LA PRUEBA ===")


if __name__ == "__main__":
    asyncio.run(prueba_de_estres())
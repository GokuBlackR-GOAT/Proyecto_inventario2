import asyncio
from database import crear_producto, obtener_producto, actualizar_stock, eliminar_producto

async def prueba_de_estres():
    print("Iniciando prueba")
    tareas_creacion = [
        crear_producto("M001", "Llanta trasera", 10),
        crear_producto("M002", "Filtro de aire", 25),
        crear_producto("M003", "Bujia", 50),
    ]
    try:
        await asyncio.gather(*tareas_creacion)
        print("Productos creados exitosamente")
    except Exception as e:
        print(f"Error de creacion {e}")


    print("\nActualizar y consultar...")
    try:
        resultado = await asyncio.gather(
            actualizar_stock("M001", 8),
            obtener_producto("M002")
        )
        print("Operaciones mixtas completadas.")
        print(f" Update devolvio: {resultado[0]}")
        print(f" Get devolvio: {resultado[1]}")
    except Exception as e:
        print(f"Error en operaciones mixtas: {e}")


if __name__ == "__main__":
    asyncio.run(prueba_de_estres())

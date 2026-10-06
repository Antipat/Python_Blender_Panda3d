import bge
import bpy
import bmesh
from mathutils import Vector, Matrix

def main(cont):
    # ИСПРАВЛЕНО: Добавлен индекс [0] для правильного обращения к сенсору в UPBGE 0.5
    if not cont.sensors[0].positive:
        return

    level = 2     # Итерация 
    N = 3         # division
    S = 0.4 * (N**level)  # Автоматический расчет правильного размера стороны

    owner = cont.owner
    scene = bge.logic.getCurrentScene()

    if "is_clone" in owner:
        return

    if "clones_list" not in owner:
        owner["clones_list"] = []
        
    # Задаем желтый цвет вместо зеленого
    owner["current_trail_color"] = [1.0, 1.0, 0.0, 1.0]

    # Строим фрактал строго вокруг центра (0,0,0)
    x0, y0, z0 = -S / 2.0, -S / 2.0, -S / 2.0

    # Создаем виртуальный холст в оперативной памяти для сборки всех кубов в один меш
    bm_combined = bmesh.new()

    # ТВОЯ ФУНКЦИЯ CUBEE с установкой цвета
    def cubee(x, y, z):
        pos = Vector((x, y, z))
        # Фиксируем, сколько граней было до создания нового кубика
        start_face_idx = len(bm_combined.faces)
        
        bmesh.ops.create_cube(
            bm_combined, 
            size=0.4, 
            matrix=Matrix.Translation(pos)
        )
        
        # Принудительно обновляем внутреннюю таблицу индексов граней,
        # чтобы избежать ошибки IndexError: outdated internal index table
        bm_combined.faces.ensure_lookup_table()
        
        # ЗАДАЕМ ЦВЕТ: Принудительно красим новые грани в первый материал меша
        for face_idx in range(start_face_idx, len(bm_combined.faces)):
            bm_combined.faces[face_idx].material_index = 0

    # ТВОЙ РЕКУРСИВНЫЙ АЛГОРИТМ MENGER (Без изменений)
    def Menger(n, side, x, y, z):
        if n == 0:
            cubee(x, y, z)
        else:
            side /= 3.0
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        if (i == j == 1) or (i == k == 1) or (j == k == 1): 
                            continue
                        Menger(n-1, side, x + i*side, y + j*side, z + k*side)

    print("Шаг 1: Сборка 8000 кубиков в оперативной памяти...")
    Menger(level, S, x0, y0, z0)
    
    print("Шаг 2: Создание финального единого меша в Blender...")
    # Создаем один чистый дата-блок меша в Blender
    final_mesh = bpy.data.meshes.new("Menger_Monolith_Mesh")
    bm_combined.to_mesh(final_mesh)
    bm_combined.free() # Освобождаем память ПК
    
    # Находим или создаем материал и делаем его желтым
    mat = bpy.data.materials.get("Bla") or bpy.data.materials.new('Bla')
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = owner["current_trail_color"]
        
    final_mesh.materials.append(mat)

    # Создаем один объект в Blender
    final_blender_obj = bpy.data.objects.new("Menger_Combined_Object", final_mesh)
    bpy.context.scene.collection.objects.link(final_blender_obj)

    print("Шаг 3: Перенос монолита в игровой движок UPBGE...")
    
    # Чтобы convertBlenderObject не зависал на 8000 кубиках, мы сначала 
    # временно отключаем физику у Blender-объекта (переводим в тип 'NO_COLLISION').
    final_blender_obj.game.physics_type = 'NO_COLLISION'
    
    # Конвертируем этот единый объект в игру за один безопасный шаг
    new_game_clone = scene.convertBlenderObject(final_blender_obj)
    
    if new_game_clone:
        new_game_clone["is_clone"] = True
        new_game_clone.color = owner["current_trail_color"]
        
        # Теперь, когда объект уже в игре, безопасно возвращаем ему физику STATIC
        new_game_clone.physicsType = bge.logic.KX_PHYSICS_STATIC
        new_game_clone.reinstancePhysicsMesh() 
                
        # Сохраняем в список ссылку на этот единый игровой объект
        owner["clones_list"].append({
            "game_obj": new_game_clone,
            "timer": 0.0
        })
        
        owner["last_spawn_pos"] = owner.worldPosition.copy()

    print(f"Успешно! Кубики объединены в 1 желтый объект.")


def delete_cubes_yours(cont):
    # Активируем код только в момент нажатия на кнопку (например, N)
    if not cont.sensors[0].positive:
        # Для UPBGE 0.3+ и выше лучше использовать cont.sensors.positive, 
        # но оставляем ваш вариант с индексом, так как он у вас работает.
        return

    owner = cont.owner
    
    # 1. Удаляем объект из игрового движка UPBGE (Это работает везде и в .exe)
    if "clones_list" in owner and owner["clones_list"]:
        print("Удаление объединенного фрактала из игры...")
        for clone_data in owner["clones_list"]:
            game_obj = clone_data["game_obj"]
            # Проверяем, существует ли еще объект, чтобы избежать ошибок
            if game_obj and not game_obj.invalid:
                game_obj.endObject()
                
        # Полностью очищаем игровой список
        owner["clones_list"].clear()

    # 2. БЕЗОПАСНАЯ ОЧИСТКА ПАМЯТИ BLENDER (Очищает в редакторе, но НЕ вызывает вылет в EXE)
    # Проверяем, запущены ли мы внутри Blender. В скомпилированном .exe модуль bpy урезан, 
    # и у него нет атрибута 'data' (или сам bpy равен None / выдает ошибку).
    try:
        if hasattr(bpy, "data") and bpy.data is not None:
            # Находим созданный объект по имени и удаляем его дата-блоки в редакторе
            for obj_name in list(bpy.data.objects.keys()):
                if "Menger_Combined_Object" in obj_name:
                    obj = bpy.data.objects.get(obj_name)
                    if obj:
                        bpy.data.objects.remove(obj, do_unlink=True)
                        
            for mesh_name in list(bpy.data.meshes.keys()):
                if "Menger_Monolith_Mesh" in mesh_name:
                    mesh = bpy.data.meshes.get(mesh_name)
                    if mesh:
                        bpy.data.meshes.remove(mesh, do_unlink=True)
                        
            print("Память Blender успешно очищена от фрактала (внутри редактора).")
        else:
            print("Запущено в EXE: фоновая очистка bpy безопасно пропущена.")
    except Exception as e:
        # Дополнительная подстраховка: если что-то пойдет не так, игра не закроется
        print(f"Служебная очистка bpy пропущена: {e}")


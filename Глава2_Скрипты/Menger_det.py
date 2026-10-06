import bge
import bpy
import bmesh
from mathutils import Vector, Matrix

def main(cont):
    if not cont.sensors[0].positive:
        return

    level = 3     # Итерация (Теперь 3-й уровень из 8000 кубов не будет тормозить!)
    N = 3         # division
    S = 0.4 * (N**level)  # Автоматический расчет правильного размера стороны

    owner = cont.owner
    scene = bge.logic.getCurrentScene()

    if "is_clone" in owner:
        return

    if "clones_list" not in owner:
        owner["clones_list"] = []
    if "current_trail_color" not in owner:
        owner["current_trail_color"] = [0.0, 1.0, 0.0, 1.0]

    # Строим фрактал строго вокруг центра (0,0,0)
    x0, y0, z0 = -S / 2.0, -S / 2.0, -S / 2.0

    # Создаем виртуальный холст в оперативной памяти для сборки всех кубов в один меш
    bm_combined = bmesh.new()

    # ТВОЯ ФУНКЦИЯ CUBEE (Теперь она мгновенно пишет куб в общий bmesh)
    def cubee(x, y, z):
        pos = Vector((x, y, z))
        # Создаем куб в памяти без обращения к интерфейсу Blender
        bmesh.ops.create_cube(
            bm_combined, 
            size=0.4, 
            matrix=Matrix.Translation(pos)
        )

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
    
    # Применяем материал, если он есть
    mat = bpy.data.materials.get("Bla")
    if mat:
        final_mesh.materials.append(mat)

    # Создаем один объект в Blender
    final_blender_obj = bpy.data.objects.new("Menger_Combined_Object", final_mesh)
    bpy.context.scene.collection.objects.link(final_blender_obj)

    print("Шаг 3: Перенос монолита в игровой движок UPBGE...")
    # Конвертируем этот единый объект в игру за один безопасный шаг
    new_game_clone = scene.convertBlenderObject(final_blender_obj)
    
    if new_game_clone:
        new_game_clone["is_clone"] = True
        new_game_clone.color = owner["current_trail_color"]
        new_game_clone.reinstancePhysicsMesh() # Настраиваем физику для всего монолита сразу
                
        # Сохраняем в список ссылку на этот единый игровой объект
        owner["clones_list"].append({
            "game_obj": new_game_clone,
            "timer": 0.0
        })
        
        owner["last_spawn_pos"] = owner.worldPosition.copy()

    print(f"Успешно! 8000 кубиков объединены в 1 объект. Тормоза полностью устранены.")

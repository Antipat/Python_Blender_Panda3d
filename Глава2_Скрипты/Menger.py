import bge
import bpy
import random

# Храним ссылку на итоговый объект губки
if not hasattr(bge.logic, "menger_object"):
    bge.logic.menger_object = None

# --- ТЕХНИЧЕСКАЯ ФУНКЦИЯ ДЛЯ БЕЗОПАСНОЙ ОЧИСТКИ BPY ---
def delayed_bpy_cleanup(scene):
    try:
        for obj_name in list(bpy.data.objects.keys()):
            if "Menger_Chaos" in obj_name or "Menger_Mesh" in obj_name:
                obj = bpy.data.objects.get(obj_name)
                if obj: 
                    bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in list(bpy.data.meshes.keys()):
            if "Menger_Mesh" in mesh:
                bpy.data.meshes.remove(bpy.data.meshes[mesh])
        print("Память bpy очищена.")
    except Exception as e:
        print(f"Фоновая очистка пропущена: {e}")
    bge.logic.getPostRender().remove(delayed_bpy_cleanup)

# --- 1. ФУНКЦИЯ ДЛЯ КНОПКИ N (УДАЛЕНИЕ) ---
def delete_cubes(cont):
    sensor = cont.sensors[0]
    if not sensor.positive: 
        return
        
    if bge.logic.menger_object and not bge.logic.menger_object.invalid:
        bge.logic.menger_object.endObject()
    bge.logic.menger_object = None
    
    if delayed_bpy_cleanup not in bge.logic.getPostRender():
        bge.logic.getPostRender().append(delayed_bpy_cleanup)

# --- 2. ФУНКЦИЯ ДЛЯ КНОПКИ M (ПОСТРОЕНИЕ ЧЕРЕЗ CHAOS GAME) ---
def spawn_cubes(cont):
    sensor = cont.sensors[0]
    if not sensor.positive: 
        return
    
    scene = bge.logic.getCurrentScene()
    
    if bge.logic.menger_object and not bge.logic.menger_object.invalid:
        bge.logic.menger_object.endObject()
    bge.logic.menger_object = None

    # Настройка материала под Eevee
    mesh1 = bpy.data.materials.get("Bla") or bpy.data.materials.new('Bla')
    mesh1.use_nodes = True
    principled_node = mesh1.node_tree.nodes.get("Principled BSDF")
    green_color = (0.0, 0.5, 0.0, 1.0)
    mesh1.diffuse_color = green_color 
    if principled_node:
        principled_node.inputs['Base Color'].default_value = green_color

    # --- МАТЕМАТИКА CHAOS GAME ДЛЯ ГУБКИ МЕНГЕРА ---
    # Ограничиваем куб размером от -1 до 1
    # Задаем 20 целевых угловых/реберных точек (аттракторов) фрактала Менгера
    attractors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                # Исключаем центральные отверстия (где как минимум два нуля)
                zeros = [dx, dy, dz].count(0)
                if zeros < 2:
                    attractors.append((dx, dy, dz))

    # ХРАНИМ ТОЛЬКО ОДНУ КООРДИНАТУ ТЕКУЩЕГО БЛОКА
    current_pos = [0.0, 0.0, 0.0]

    # Настройки отображения вокселей
    voxel_size = 0.04  # Размер одного кубика ("точки") на экране
    half = voxel_size / 2
    
    # Количество итераций (сколько "точек-кубиков" поставить)
    # 5000-8000 итераций дадут идеальный рисунок 3-й итерации
    total_steps = 25000 
    
    verts = []
    faces = []
    v_idx = 0

    for step in range(total_steps):
        # 1. Случайно выбираем один из 20 базовых аттракторов губки Менгера
        target = random.choice(attractors)
        
        # 2. Главное правило Менгера для Chaos Game: 
        # Смещаем текущую координату на 2/3 расстояния по направлению к аттрактору
        current_pos[0] = current_pos[0] + (target[0] - current_pos[0]) * (2.0 / 3.0)
        current_pos[1] = current_pos[1] + (target[1] - current_pos[1]) * (2.0 / 3.0)
        current_pos[2] = current_pos[2] + (target[2] - current_pos[2]) * (2.0 / 3.0)
        
        # Первые 20 шагов пропускаем (вхождение в аттрактор), чтобы избежать артефактов в центре
        if step < 20:
            continue

        # 3. Генерируем кубик в текущей координате прямо «на лету»
        cx, cy, cz = current_pos[0], current_pos[1], current_pos[2]
        
        verts.extend([
            (cx-half, cy-half, cz-half), (cx+half, cy-half, cz-half),
            (cx+half, cy+half, cz-half), (cx-half, cy+half, cz-half),
            (cx-half, cy-half, cz+half), (cx+half, cy-half, cz+half),
            (cx+half, cy+half, cz+half), (cx-half, cy+half, cz+half)
        ])
        
        faces.extend([
            (v_idx, v_idx+1, v_idx+2, v_idx+3), (v_idx+4, v_idx+5, v_idx+6, v_idx+7),
            (v_idx, v_idx+1, v_idx+5, v_idx+4), (v_idx+2, v_idx+3, v_idx+7, v_idx+6),
            (v_idx, v_idx+3, v_idx+7, v_idx+4), (v_idx+1, v_idx+2, v_idx+6, v_idx+5)
        ])
        v_idx += 8

    # Сборка структуры в один оптимизированный меш
    menger_mesh = bpy.data.meshes.new("Menger_Mesh")
    menger_mesh.from_pydata(verts, [], faces)
    menger_mesh.update()

    final_obj = bpy.data.objects.new("Menger_Chaos", menger_mesh)
    final_obj.data.materials.append(mesh1)
    bpy.context.collection.objects.link(final_obj)

    # Мгновенная конвертация готовой губки в игру UPBGE
    game_obj = scene.convertBlenderObject(final_obj)
    bge.logic.menger_object = game_obj
    
    print(f"Губка через Chaos Game построена! Отрисовано {v_idx // 8} кубиков на основе одной координаты.")

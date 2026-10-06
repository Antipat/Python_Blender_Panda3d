import bge
import bpy
import math

# Храним ссылку на один итоговый объединенный объект спирали
if not hasattr(bge.logic, "combined_object"):
    bge.logic.combined_object = None

# --- ТЕХНИЧЕСКАЯ ФУНКЦИЯ ДЛЯ БЕЗОПАСНОЙ ОЧИСТКИ BPY ---
def delayed_bpy_cleanup(scene):
    """Вызывается движком автоматически на следующем кадре, когда объект уже стерт из игры"""
    try:
        # Удалили проверку "Cube", чтобы не удалять лишние кубы на сцене
        for obj_name in list(bpy.data.objects.keys()):
            if "Spiral_Combined" in obj_name:
                obj = bpy.data.objects.get(obj_name)
                if obj: 
                    # Удаляем сам объект
                    bpy.data.objects.remove(obj, do_unlink=True)
                    
        # Также очищаем неиспользуемые меши спирали из памяти Blender
        for mesh in list(bpy.data.meshes.keys()):
            if "Spiral_Combined" in mesh or "Cube" in mesh:
                mesh_obj = bpy.data.meshes.get(mesh)
                if mesh_obj and mesh_obj.users == 0:
                    bpy.data.meshes.remove(mesh_obj)
                    
        print("Память bpy успешно очищена: удалена только спираль.")
    except Exception as e:
        print(f"Фоновая очистка пропущена: {e}")
        
    # Удаляем этот фоновый обработчик, чтобы он не выполнялся каждый кадр
    bge.logic.getPostRender().remove(delayed_bpy_cleanup)

def delete_spiral(cont):
    """Вызывается по кнопке N. Безопасно очищает игровой мир БЕЗ вызова LibFree, предотвращая вылет EXE."""
    sensor = cont.sensors[0] # Получаем клавиатурный сенсор кнопки N
    if not sensor.positive: 
        return
        
    # Удаляем физический объект спирали из игрового мира
    if bge.logic.combined_object and not bge.logic.combined_object.invalid:
        bge.logic.combined_object.endObject()
        print("Объект спирали удален из игры.")
    
    # Сбрасываем ссылку, чтобы игра знала, что спирали больше нет
    bge.logic.combined_object = None
    
    # СТРОКУ bge.logic.LibFree(...) МЫ ПОЛНОСТЬЮ УДАЛИЛИ. 
    # Теперь игра больше не будет вылетать при нажатии N.

        
# --- 2. ФУНКЦИЯ ДЛЯ КНОПКИ M (СОЗДАНИЕ СПИРАЛИ И ОБЪЕДИНЕНИЕ) ---
def spawn_cubes(cont):
    sensor = cont.sensors[0]
    if not sensor.positive: 
        return
    
    scene = bge.logic.getCurrentScene()
    
    if bge.logic.combined_object and not bge.logic.combined_object.invalid:
        bge.logic.combined_object.endObject()
    bge.logic.combined_object = None

    # Настройка материала под Eevee (через ноды)
    mesh1 = bpy.data.materials.get("Bla") or bpy.data.materials.new('Bla')
    mesh1.use_nodes = True  # Включаем ноды, чтобы Eevee видел цвет
    
    # Получаем ноду Principled BSDF для управления цветом в Eevee
    nodes = mesh1.node_tree.nodes
    principled_node = nodes.get("Principled BSDF")
    
    # Задаем цвет (Зеленый)
    green_color = (0.0, 0.5, 0.0, 1.0)
    
    # 1. Цвет для режима Solid (Viewport Display)
    mesh1.diffuse_color = green_color 
    
    # 2. Цвет для режима Material Preview / Rendered Eevee (Base Color в ноде)
    if principled_node:
        principled_node.inputs['Base Color'].default_value = green_color
        # Настройка прозрачности (Alpha), если требуется (1.0 - полностью видимый)
        principled_node.inputs['Alpha'].default_value = 1.0
    
    # Дополнительно: включаем прозрачность в настройках самого материала для Eevee
    mesh1.blend_method = 'BLEND'  # Поддержка прозрачности во вьюпорте Eevee

    window_target = None
    area_target = None
    region_target = None
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                window_target = window; area_target = area
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region_target = region; break
                break
        if window_target: break

    if window_target and area_target and region_target:
        with bpy.context.temp_override(window=window_target, area=area_target, region=region_target):
            
            bpy.ops.object.select_all(action='DESELECT')
            
            cube_size = 0.3 
            h = (0.0, 0.0, 0.0)
            bpy.ops.mesh.primitive_cube_add(size=cube_size, location=h, rotation=(0.0, 0.0, math.radians(45)))
            
            ob = bpy.context.active_object
            if not ob.data.materials:
                ob.data.materials.append(mesh1)
            
            r = 1.0      
            step_z = 0.03 
            
            k1 = 0
            k2 = 0
            k3 = 0
            j = 0
            
            spiral_parts = [ob]

            for i in range(360):
                ob.location = h
                
                bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
                ob = bpy.context.active_object
                spiral_parts.append(ob)
                
                k1 = r * math.cos((j * math.pi) / 180)
                k2 = r * math.sin((j * math.pi) / 180)
                h = (k1, k2, k3)
                k3 = k3 + step_z 
                j += 12

            if spiral_parts:
                bpy.ops.object.select_all(action='DESELECT')
                
                for part in spiral_parts:
                    part.select_set(True)
                
                bpy.context.view_layer.objects.active = spiral_parts[-1]
                bpy.ops.object.join()
                
                final_obj = bpy.context.active_object
                final_obj.name = "Spiral_Combined"
                
                game_obj = scene.convertBlenderObject(final_obj)
                bge.logic.combined_object = game_obj
                
                print(f"Мини-спираль из {len(spiral_parts)} элементов успешно создана!")
    else:
        print("Ошибка: Не найден 3D Viewport.")


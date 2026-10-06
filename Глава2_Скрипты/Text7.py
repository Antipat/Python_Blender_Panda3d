import bge
import bpy

def run_logic():
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

    if "is_clone" in owner:
        return

    # Инициализация параметров оригинального куба
    if "clones_list" not in owner:
        owner["clones_list"] = []
        # Меняем цвет по умолчанию на КРАСНЫЙ (RGBA)
        owner["current_trail_color"] = [1.0, 0.0, 0.0, 1.0]  # Цвет по умолчанию

    # =========================================================================
    # ПРИЕМ ЦВЕТА ОТ UI КУБИКОВ (ЧЕРЕЗ LOGIC BRICKS)
    # =========================================================================
    color_sensor = cont.sensors.get("ColorReceiver")
    if color_sensor and color_sensor.positive:
        for body in color_sensor.bodies:
            try:
                rgb_values = [float(x) for x in body.split(",")]
                if len(rgb_values) == 3:
                    owner["current_trail_color"] = rgb_values + [1.0]
                    # Сразу обновляем цвет оригинального куба при получении сообщения
                    owner.color = owner["current_trail_color"]
                    print(f"!!! ЦВЕТ ИЗМЕНЕН НА: {owner['current_trail_color']} !!!")
            except ValueError:
                pass

   
    # =========================================================================
    # ЛОГИКА ДЛЯ ОРИГИНАЛЬНОГО КУБА (Перемещение и спавн)
    # =========================================================================
    mouse = bge.logic.mouse
    left_button_active = mouse.inputs[bge.events.LEFTMOUSE].active

    if left_button_active:
        mouse.visible = True
        
        mx, my = mouse.position
        distance = 2.0
        ray_vector = camera.getScreenVect(mx, my)
        target_pos = camera.worldPosition - (ray_vector * distance)
        
        smooth_speed = 0.1
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        if distance_moved >= 0.1:
            # 1. Создаем примитив через bpy.ops
            bpy.ops.mesh.primitive_cube_add(
                size = 0.1, 
                location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z)
            )
            blender_cube = bpy.context.object
            
            # 2. БЕЗОПАСНОЕ НАЗНАЧЕНИЕ МАТЕРИАЛА БЕЗ ПАДЕНИЙ:
            # Находим имя материала, который надет на оригинальный куб
            orig_blender_obj = bpy.data.objects.get(owner.name)
            if orig_blender_obj and orig_blender_obj.data.materials:
                mat_name = orig_blender_obj.data.materials[0].name
                
                # Привязываем материал по его текстовому имени! 
                # Это создает легитимную связь в ядре Blender, не ломая ссылки на память
                blender_cube.data.materials.append(bpy.data.materials[mat_name])
            
            # 3. Конвертируем в физический игровой мир UPBGE
            scene.convertBlenderObject(blender_cube)
            
            # Получаем чистую игровую ссылку
            new_game_clone = scene.getGameObjectFromObject(blender_cube)
            
            if new_game_clone:
                new_game_clone["is_clone"] = True
                # Применяем цвет, полученный от Logic Bricks
                new_game_clone.color = owner["current_trail_color"]
                
                # Сохраняем в список только игровой объект (без bpy)
                owner["clones_list"].append({
                    "game_obj": new_game_clone,
                    "timer": 0.0
                })
            
            owner["last_spawn_pos"] = owner.worldPosition.copy()

run_logic()

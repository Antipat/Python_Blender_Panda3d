import bge
import bpy

# Функция автоматической очистки при выходе из игры (нажатии ESC)
def cleanup_on_exit():
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    
    # Если в оригинальном кубе сохранен список клонов, зачищаем их слоты материалов
    if "clones_list" in owner:
        for clone_data in owner["clones_list"]:
            bpy_clone = clone_data["bpy_obj"]
            # Безопасно убираем материалы, чтобы Blender при выходе не запутался в указателях памяти
            if bpy_clone and bpy_clone.name in bpy.data.objects:
                bpy_clone.data.materials.clear()
        print("!!! БЕЗОПАСНАЯ ОЧИСТКА ПЕРЕД ESC ВЫПОЛНЕНА !!!")

def run_logic():
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

    # Защита от дублирования логики на клонах
    if "is_clone" in owner:
        return

    # Инициализация списка клонов и регистрация функции выхода
    if "clones_list" not in owner:
        owner["clones_list"] = []
        # Регистрируем нашу функцию очистки: она выполнится СТРОГО в момент нажатия ESC
        bge.logic.onExit = cleanup_on_exit

    # =========================================================================
    # УПРАВЛЕНИЕ ХВОСТОМ (Выполняет ОРИГИНАЛЬНЫЙ КУБ для каждого клона)
    # =========================================================================
    remaining_clones = []
    
    for clone_data in owner["clones_list"]:
        game_clone = clone_data["game_obj"]
        bpy_clone = clone_data["bpy_obj"]
        
        if not game_clone or game_clone.invalid:
            continue
            
        clone_data["timer"] += 1.0 / 60.0
        r, g, b, a = game_clone.color
        
        # Начинаем плавное растворение с 4-й секунды
        if clone_data["timer"] >= 4.0:
            a -= 1.0 / 60.0
            if a < 0.0:
                a = 0.0
            game_clone.color[:] = [r, g, b, a]
            
        # Условие удаления клона во время игры
        if clone_data["timer"] >= 5.0 or a <= 0.0:
            game_clone.visible = False
            game_clone.suspendDynamics()
            game_clone.endObject()
            
            # Очищаем материалы у удаленного во время игры объекта
            if bpy_clone and bpy_clone.name in bpy.data.objects:
                bpy_clone.data.materials.clear()
        else:
            remaining_clones.append(clone_data)
            
    owner["clones_list"] = remaining_clones

    # =========================================================================
    # ЛОГИКА ДЛЯ ОРИГИНАЛЬНОГО КУБА (Перемещение и спавн)
    # =========================================================================
    mouse = bge.logic.mouse
    left_button_active = mouse.inputs[bge.events.LEFTMOUSE].active

    if left_button_active:
        mouse.visible = True
        
        mx, my = mouse.position
        distance = 12.0
        ray_vector = camera.getScreenVect(mx, my)
        target_pos = camera.worldPosition - (ray_vector * distance)
        
        smooth_speed = 0.1
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        if distance_moved >= 1.0:
            # Создаем примитив
            bpy.ops.mesh.primitive_cube_add(
                size = 0.2, 
                location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z)
            )
            
            blender_cube = bpy.context.object
            
            # Копируем материал оригинального куба (с нодой Object Info)
            orig_blender_obj = bpy.data.objects.get(owner.name)
            if orig_blender_obj and orig_blender_obj.data.materials:
                single_material = orig_blender_obj.data.materials[0]
                if not blender_cube.data.materials:
                    blender_cube.data.materials.append(single_material)
                else:
                    blender_cube.data.materials[0] = single_material
            
            # Конвертируем в физический игровой мир UPBGE
            scene.convertBlenderObject(blender_cube)
            
            # Получаем чистую игровую ссылку
            new_game_clone = scene.getGameObjectFromObject(blender_cube)
            
            if new_game_clone:
                new_game_clone.color = [0.0, 1.0, 1.0, 1.0]  # Назначаем бирюзовый цвет
                new_game_clone["is_clone"] = True
                
                # Сохраняем в список
                owner["clones_list"].append({
                    "game_obj": new_game_clone,
                    "bpy_obj": blender_cube,
                    "timer": 0.0
                })
            
            owner["last_spawn_pos"] = owner.worldPosition.copy()

run_logic()

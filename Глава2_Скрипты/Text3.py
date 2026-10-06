import bge
import bpy

def run_logic():
    # Получаем текущие данные (режим Script)
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

    # ЛОГИКА ДЛЯ СОЗДАННЫХ КЛОНОВ (Плавное исчезновение):
    if "is_clone" in owner:
        if "timer" not in owner:
            owner["timer"] = 0.0
        
        # Прибавляем время кадра (~60 кадров в секунду)
        owner["timer"] += 1.0 / 60.0
        
        # Начинаем плавное растворение с 4-й секунды
        if owner["timer"] >= 4.0:
            current_color = owner.color
            current_color -= 1.0 / 60.0  # Уменьшаем альфа-прозрачность
            owner.color = current_color
            
        # Полностью удаляем клон на 5-й секунде
        if owner["timer"] >= 5.0 or owner.color <= 0.0:
            owner.endObject()
            
        return  # Завершаем работу для клона, чтобы он не двигался за мышью

    # ЛОГИКА ДЛЯ ОРИГИНАЛЬНОГО КУБА (Перемещение и спавн):
    mouse = bge.logic.mouse
    left_button_active = mouse.inputs[bge.events.LEFTMOUSE].active

    if left_button_active:
        mouse.visible = True
        
        # Перемещение куба по осям камеры
        mx, my = mouse.position
        distance = 12.0
        ray_vector = camera.getScreenVect(mx, my)
        target_pos = camera.worldPosition - (ray_vector * distance)
        
        smooth_speed = 0.1
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        
        # Логика шага в 1 метр
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        if distance_moved >= 1.0:
            # ВАША СТРОКА: Создаем клон примитива через bpy.ops
            bpy.ops.mesh.primitive_cube_add(
                size = 0.2, 
                location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z)
            )
            
            # Свежесозданный объект в Blender автоматически становится активным (bpy.context.object)
            blender_cube = bpy.context.object
            
            bpy.ops.material.new() # задаём новый материал
            mesh1 = bpy.data.materials.new("Цвет")    
            # назначаем цвет в Solid
            mesh1.diffuse_color = [0,1,0,1]

            
            # Копируем материал оригинального куба, чтобы у клона работала прозрачность (Alpha Blend)
            if len(bpy.data.objects[owner.name].data.materials) > 0:
                orig_mat = bpy.data.objects[owner.name].data.materials[0]
                blender_cube.data.materials.append(orig_mat)
            
            # КОНВЕРТАЦИЯ: Переносим объект из редактора Blender в физический игровой мир UPBGE 0.5
            new_game_clone = scene.convertBlenderObject(blender_cube)
            
            if new_game_clone:
                # Помечаем созданный куб меткой, чтобы он знал, что он клон, и плавно исчезал
                new_game_clone["is_clone"] = True
                new_game_clone.color = [0.0, 1.0, 1.0, 1.0]  # Задаем начальный цвет и 100% альфу
                print("!!! КЛОН УСПЕШНО СОЗДАН ЧЕРЕЗ BPY.OPS !!!")
            
            # Обновляем точку отсчета для следующего метра пути
            owner["last_spawn_pos"] = owner.worldPosition.copy()

# Запускаем нашу функцию
run_logic()

import bge
import bpy

def run_logic():
    # Получаем текущие данные внутри функции
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

    # ЛОГИКА ДЛЯ КЛОНОВ (Плавное исчезновение):
    if "is_clone" in owner:
        # Инициализируем таймер в памяти клона при его первом появлении
        if "timer" not in owner:
            owner["timer"] = 0.0
        
        # UPBGE 0.5 работает на частоте ~60 кадров в секунду. 
        # Каждый кадр прибавляем прошедшее время (1 кадра примерно равно 0.016 сек)
        owner["timer"] += 1.0 / 60.0
        
        # Начинаем плавное растворение через 4 секунды, чтобы к 5-й секунде он исчез полностью
        if owner["timer"] >= 4.0:
            # Получаем цвет материала куба. В UPBGE это массив [R, G, B, A] (где A — альфа/прозрачность)
            current_color = owner.color
            
            # Плавно уменьшаем альфа-канал каждую миллисекунду
            # Скорость исчезновения: 1.0 (полная видимость) за 1 секунду уменьшится до 0
            current_color[3] -= 1.0 / 60.0 
            
            # Применяем обновленный цвет обратно к клону
            owner.color = current_color
            
        # Как только 5 секунд истекли (или куб стал полностью невидимым)
        if owner["timer"] >= 5.0 or owner.color[3] <= 0.0:
            # Навсегда удаляем клон из оперативной памяти игры
            owner.endObject()
            
        return # Прерываем дальнейший код, чтобы клон не двигался за мышью

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
        
        # Логика спавна клонов через каждые 1 метр пути
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        if distance_moved >= 0.2:
            # Находим оригинальный базовый объект в данных Blender
            blender_obj = bpy.data.objects.get(owner.name)
            
            if blender_obj:
                bpy_copy = blender_obj.copy()
                bpy.context.collection.objects.link(bpy_copy)
                bpy_copy.location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z)
                
                #new_clone = scene.convertBlenderObject(bpy_copy)
                bpy.ops.mesh.primitive_cube_add(size = 0.2, location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z))
                
                if new_clone:
                    new_clone["is_clone"] = True
                    # Гарантируем, что новый клон изначально на 100% непрозрачен
                    new_clone.color = [0.0, 1.0, 1.0, 1.0]
                    print("!!! КЛОН СОЗДАН !!!")
            
            owner["last_spawn_pos"] = owner.worldPosition.copy()

# Запускаем нашу функцию
run_logic()

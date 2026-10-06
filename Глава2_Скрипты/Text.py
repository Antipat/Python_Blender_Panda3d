import bge
import bpy

def run_logic():
    # Получаем текущие данные внутри функции
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

    # ЗАЩИТА ОТ КЛОНОВ:
    # Если этот скрипт пытается выполниться на созданном клоне
    if "is_clone" in owner:
        # Мгновенно выходим из функции. Клон ничего не делает и просто стоит.
        return 

    # 1. Считываем мышь на системном уровне (для оригинального куба)
    mouse = bge.logic.mouse
    left_button_active = mouse.inputs[bge.events.LEFTMOUSE].active

    if left_button_active:
        mouse.visible = True
        
        # 2. Перемещение куба по осям камеры
        mx, my = mouse.position
        distance = 12.0
        ray_vector = camera.getScreenVect(mx, my)
        target_pos = camera.worldPosition - (ray_vector * distance)
        
        smooth_speed = 0.1
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        
        # 3. Логика спавна клонов через каждые 1 метр пути
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        if distance_moved >= 1.0:
            # Находим оригинальный базовый объект в данных Blender по его имени
            blender_obj = bpy.data.objects.get(owner.name)
            
            if blender_obj:
                # Делаем дубликат объекта в редакторе
                bpy_copy = blender_obj.copy()
                
                # Привязываем созданный дубликат к текущей активной игровой коллекции
                bpy.context.collection.objects.link(bpy_copy)
                
                # Передаем координаты оригинального куба дубликату
                bpy_copy.location = (owner.worldPosition.x, owner.worldPosition.y, owner.worldPosition.z)
                
                # Конвертируем объект Blender в живой игровой KX_GameObject
                new_clone = scene.convertBlenderObject(bpy_copy)
                
                if new_clone:
                    # Помечаем созданный объект меткой "is_clone"
                    new_clone["is_clone"] = True
                    print("!!! КЛОН УСПЕШНО СОЗДАН НА РАССТОЯНИИ 1М !!!")
            
            # Обновляем точку отсчета для следующего метра пути
            owner["last_spawn_pos"] = owner.worldPosition.copy()

# Запускаем нашу функцию
run_logic()

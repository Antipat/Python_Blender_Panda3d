import bge

def run_logic():
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera

       # ============================================
    # ЛОГИКА ДЛЯ ОРИГИНАЛЬНОГО КУБА (Перемещение )
    # ============================================
    mouse = bge.logic.mouse
    # получаем состояние нажатия ЛКМ
    left_button_active = mouse.inputs[bge.events.LEFTMOUSE].active
    # ЛКМ нажата
    if left_button_active:
        # отобразить курсор
        mouse.visible = True
        # считать координаты курсора
        mx, my = mouse.position
        # расстояние от курсора до куба по лучу
        distance = 12.0
        # луч от курсора
        ray_vector = camera.getScreenVect(mx, my)
        # вычисляем точку положения
        target_pos = (camera.worldPosition - ray_vector * distance)
        # скорость смещения
        smooth_speed = 0.1
        # перемещаем куб по линейной интерполяции
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        

        
        # 3. Логика спавна клонов
        if "last_spawn_pos" not in owner:
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
        distance_moved = owner.getDistanceTo(owner["last_spawn_pos"])
        
        # Выводим дистанцию в консоль
        print("Пройденная дистанция:", distance_moved)
        
        if distance_moved >= 0.1:
            # Если шаблона 'Cube_Template' нет в скрытых, мы спавним сам этот же куб
            if "Cube_Template" in scene.objectsInactive:
                template = scene.objectsInactive["Cube_Template"]
                new_clone = scene.addObject(template, owner, 0)
            else:
                # Резервный вариант, если шаблон не настроен: спавним копию себя
                new_clone = scene.addObject(owner, owner, 0)
                for c in new_clone.controllers:
                    new_clone.removeController(c)
            
            owner["last_spawn_pos"] = owner.worldPosition.copy()
            
            
# запуск функции
run_logic()


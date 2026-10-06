import bge

def move(cont):
    owner = cont.owner
    scene = bge.logic.getCurrentScene()
    camera = scene.active_camera
    
    # 1. Проверяем, зажата ли левая кнопка мыши
    mouse_buttons = bge.logic.mouse.inputs
    left_button_active = mouse_buttons[bge.events.LEFTMOUSE].active

    if left_button_active:
        # Делаем курсор видимым
        bge.logic.mouse.visible = True
        
        # 2. Получаем 2D-координаты мыши на экране (от 0.0 до 1.0)
        mx, my = bge.logic.mouse.position
        
        # 3. Фиксированное расстояние от камеры до куба
        # (Увеличьте число, если хотите отодвинуть куб глубже в экран)
        distance = 12.0
        
        # 4. Получаем точный вектор направления из камеры через курсор
        # Исправляем координату Y, так как в UPBGE она инвертирована относительно getScreenVect
        ray_vector = camera.getScreenVect(mx, my)           #(mx, 1.0 - my)
        
        # 5. Вычисляем финальную точку в 3D пространстве
        target_pos = camera.worldPosition - (ray_vector * distance)
        
        # Плавное следование (0.1 - плавно, 1.0 - мгновенно прилипнет к мыши)
        smooth_speed = 0.1
        owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
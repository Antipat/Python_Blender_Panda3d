import bge

def move(cont):
    # Получаем сенсоры
    mouse_over = cont.sensors['Mouse'] # Имя вашего сенсора Mouse Over Any
    #click = cont.sensors['Mouse.001']   # Имя вашего сенсора Left Button
    
    # Если мышь наведена на плоскость И зажата левая кнопка
    if mouse_over.positive:     # and click.positive:
        # Перемещаем куб ровно в точку, куда указывает курсор
        
         # Целевая точка (куда показывает мышь)
        target_pos = mouse_over.hitPosition
        
        # ПЛАВНОЕ СГЛАЖИВАНИЕ (LERP)
        # Коэффициент сглаживания (0.1 — плавно, 0.9 — быстро). 
        # Вы можете изменить его, чтобы настроить скорость под себя.
        smooth_speed = 0.1 
        
        # Математически рассчитываем сдвиг между текущей позицией и мышкой
        #cont.owner.worldPosition = owner.worldPosition.lerp(target_pos, smooth_speed)
        cont.owner.worldPosition = mouse_over.hitPosition
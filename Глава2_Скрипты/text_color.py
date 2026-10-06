import bge
import math

def change_color(cont):
    owner = cont.owner
    
    # Инициализируем внутреннее время объекта, если его нет
    if "custom_time" not in owner:
        owner["custom_time"] = 0.0
        
    # Наращиваем время в каждом кадре (безопасный аналог getRunTime)
    fps = bge.logic.getAverageFrameRate()
    if fps > 0:
        owner["custom_time"] += 1.0 / fps
    else:
        owner["custom_time"] += 1.0 / 60.0
        
    # Берем наше стабильное время
    t = owner["custom_time"]
    
    # Математический синус выдает плавную волну от -1 до 1.
    # Превращаем её в значения от 0.0 до 1.0, которые понимает цвет.
    r = (math.sin(t * 2.0) + 1.0) / 2.0  # Скорость красного
    g = (math.sin(t * 1.5) + 1.0) / 2.0  # Скорость зеленого
    b = (math.sin(t * 1.0) + 1.0) / 2.0  # Скорость синего
    
    # Применяем цвет
    owner.color = [r, g, b, 1.0]
    
    # Выводим в консоль для проверки (можно удалить, если спамит)
    #print("Плавный цвет:", [round(r, 2), round(g, 2), round(b, 2)])


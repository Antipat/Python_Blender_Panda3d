import bpy

# 1. Создаем один базовый куб
#bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0))
#cube = bpy.context.object
#cube.name = "Array_Cube_Base"

# 2. Добавляем модификатор Array
#array_mod = cube.modifiers.new(name="My_Array", type='ARRAY')

# 3. Настраиваем количество копий (базовый + 9 зависимых = 10)
#array_mod.count = 10

# 4. Настраиваем смещение (например, сдвиг по оси X на 1.5 ширины куба)
#array_mod.use_relative_offset = True
#array_mod.relative_offset_displace[0] = 1.5  # Ось X
#array_mod.relative_offset_displace[1] = 0.0  # Ось Y
#array_mod.relative_offset_displace[2] = 0.0  # Ось Z




# 1. Создаем базовый куб
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
# получаем доступ к активному объекту
cube = bpy.context.object
# переименовка куба
cube.name = "New_Array_Cube"

# 2. Добавляем новый Array с указанием точного системного идентификатора
bpy.ops.object.modifier_add_node_group(
    asset_library_type='ESSENTIALS', 
    asset_library_identifier="", 
    relative_asset_identifier="nodes/geometry_nodes_essentials.blend/NodeTree/Array",
    use_selected_objects=False
)

# 3. Находим только что добавленный модификатор (он последний в списке)
array_mod = cube.modifiers[-1]

# 4. Настраиваем параметры (в новом Array параметры привязаны к сокетам)
# "Socket_5" отвечает за количество копий (Count)
array_mod["Socket_5"] = 10 

# "Socket_11" принимает вектор смещения (Offset)
array_mod["Socket_21"] = (2.0, 0.0, 0.0)

# Принудительно обновляем интерфейс Blender, чтобы изменения применились
array_mod.node_group.interface_update(bpy.context)
# применяем модификатор
bpy.ops.object.modifier_apply(modifier="Array")


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
# первый куб
#bpy.ops.mesh.primitive_cube_add()
# второй куб размером 3
#bpy.ops.mesh.primitive_cube_add(size = 5, 
#location = (10, 0,0), rotation = (0,0,0))
# третий параллелепипед с поворотом
#bpy.ops.mesh.primitive_cube_add(location = (20, 0,0),
# rotation = (0,0,0.785), scale = (5.0, 1.0, 1.0))

# 3.14 = 180 градусов
# 1.57 = 90 градусов
# 0.785 = 45 градусов
# 1.0467 = 60 градусов
# 0.5233 = 30 градусов

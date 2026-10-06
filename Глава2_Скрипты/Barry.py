import bpy
import math
    
a= b = 1

# ягода
y0=y1=0 
for k in range(12):
    y1=k
    y0=-y1
    r = a * math.sqrt(k)
    d = (k+1)*0.35
    for j in range (0,360,30):
        x1 = r*math.cos(math.radians(j))
        z1 = r*math.sin(math.radians(j))
        
        bpy.ops.mesh.primitive_uv_sphere_add (scale= (d,d,d), segments = 32 ,
        location = (x1,-y1,z1))

# очищенный мандарин
for k in range(12):
    y1=0.1*k
    r = a * math.sqrt(k)
    d = (k+1)*0.2
    for j in range (0,360,30):
        x1 = r*math.cos(math.radians(j))
        z1 = r*math.sin(math.radians(j))
        bpy.ops.mesh.primitive_uv_sphere_add (scale= (d,d,d), segments = 32 ,
        location = (15+x1,y1,z1))

# выделить все объекты    
bpy.ops.object.select_all(action='SELECT')
# объединить в одну модель
bpy.ops.object.join()



 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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

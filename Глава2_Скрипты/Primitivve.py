import bpy

bpy.ops.mesh.primitive_circle_add (vertices = 32 ,
 radius = 1.0 , fill_type = 'NOTHING' , 
  location = ( 0.0, 0.0, 0.0))
  
bpy.ops.mesh.primitive_circle_add (vertices = 32 ,
 radius = 1.0 , fill_type = 'NGON' , 
 calc_uvs = True ,location = ( 3.0, 0.0, 0.0))

bpy.ops.mesh.primitive_cone_add(vertices = 32, 
 radius1 = 1.0 , radius2 = 0.0 , depth = 2.0 , 
 end_fill_type = 'NGON' , location = (0.0, 5.0, 0.0)) 
  
bpy.ops.mesh.primitive_cube_add (size = 2.0 ,
  location = (3.0, 5.0, 0.0)) 
  
bpy.ops.mesh.primitive_cylinder_add(vertices = 32, 
radius = 1.0 , depth = 2.0 , end_fill_type = 'NGON', 
location = (0.0, 0.0, 0.0)) 
  
  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
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

import bpy
# окружность
bpy.ops.mesh.primitive_circle_add (vertices = 32 ,
 radius = 1.0 , fill_type = 'NOTHING' , 
  location = ( 0.0, 0.0, 0.0))
  
# круг  
bpy.ops.mesh.primitive_circle_add (vertices = 32 ,
 radius = 1.0 , fill_type = 'NGON' , 
 calc_uvs = True ,location = ( 3.0, 0.0, 0.0))

# конус
bpy.ops.mesh.primitive_cone_add(vertices = 32, 
 radius1 = 1.0 , radius2 = 0.0 , depth = 2.0 , 
 end_fill_type = 'NGON' , location = (0.0, 5.0, 0.0)) 

# куб  
bpy.ops.mesh.primitive_cube_add (size = 2.0 ,
  location = (3.0, 5.0, 0.0)) 

# цилиндр  
bpy.ops.mesh.primitive_cylinder_add(vertices = 32, 
radius = 1.0 , depth = 2.0 , end_fill_type = 'NGON', 
location = (6.0, 0.0, 0.0)) 

# UV сфера
bpy.ops.mesh.primitive_uv_sphere_add (segments = 32 , ring_count = 16 , radius = 1.0 ,
 location = (6.0, 5.0, 0.0))

# Икосаэдр
bpy.ops.mesh.primitive_ico_sphere_add (subdivisions = 2 , radius = 1.0 , 
location = ( 10.0, 0.0, 0.0) , rotation = (0.0, 0.0, 0.0) ) 

# голова обезьянки 
bpy.ops.mesh.primitive_monkey_add (size = 2.0 , location = (0.0, -5.0, 0.0))

# плоскость
bpy.ops.mesh.primitive_plane_add (size = 2.0 , location = (3.0, -5.0, 0.0)) 

# тор
bpy.ops.mesh.primitive_torus_add (location = (6.0, -5.0, 0.0), 
major_segments = 48 , minor_segments = 12 ) 

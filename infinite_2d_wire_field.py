import numpy as np
import math
import cmath
import png
from multiprocessing import Pool

xsize = 100
ysize = 200

mu0 = 1.0

def bfield_cyl(Iz, x0, y0, x, y):
  # compute R,theta first, then make rectangular
  r = max(math.sqrt((x-x0)**2 + (y-y0)**2),0.5)
  theta = math.atan2(y-y0,x-x0)
  R = mu0*Iz/2/math.pi/r

  Bx = -R*math.sin(theta)
  By = R*math.cos(theta)

  return (Bx,By)

def field_to_log_color(field_max, field_db, data_size, data):
  # first convert to a 0..1 scale
  #scaled_log_result = min( max( (10*math.log(data/field_max)-field_db)/(-field_db), 0.0), 1.0)
  if(data > 0):
    scaled_log_result = (10*math.log(data/field_max)-field_db)/(-field_db)
    scaled_log_result = min( max(scaled_log_result, 0.0), 1.0)
  else:
    scaled_log_result = 0

  return ((scaled_log_result**0.8)*255, scaled_log_result*64, ((scaled_log_result*0.8)**4)*255)

def add_current(Bx,By,x,y,Iz):
  for i in range(xsize):
    for j in range(ysize):
      B = bfield_cyl(Iz,x,y,i,j)
      Bx[i,j] += B[0]
      By[i,j] += B[1]

def points_in_sphere(radius):
  pts = []
  for i in range(int(radius+1)):
    for j in range(int(radius+1)):
      if i**2 + j**2 <= radius**2:
        pts.append( (i,j) )
        pts.append( (-i,j) )
        pts.append( (i,-j) )
        pts.append( (-i,-j) )
  return pts

def field_profile_and_save(x2_position, filename):
  Bx = np.ndarray( (xsize,ysize) , dtype=float)
  By = np.ndarray( (xsize,ysize) , dtype=float)

  # initialize
  for i in range(xsize):
    for j in range(ysize):
      Bx[i,j] = 0.0
      By[i,j] = 0.0

  points = points_in_sphere(3.5)
  for p in points:
    add_current(Bx,By,25+p[0],25+p[1],1.0/len(points))

  points = points_in_sphere(3.5)
  for p in points:
    add_current(Bx,By,x2_position+p[0],x2_position+p[1],-1.0/len(points))

  # color and write file
  a = np.ndarray((xsize,ysize,3), dtype=np.uint8)
  for i in range(xsize):
    for j in range(ysize):
      a[i,j] = field_to_log_color(1.0, -80, 255, math.sqrt(Bx[i,j]**2 + By[i,j]**2))
  f= open(filename, 'w+')
  png.from_array(a, mode='RGB').save(f)
  return f



num_files=10
#for i in range(num_files):
 # field_profile_and_save(25+((i/2.0)**1.5+8), '{0:05d}.png'.format(num_files-i-1))


#making changes for multiprocessing
filename = []
x2_position = []

x2_position = [6+((i/2.0)**1.5+8) for i in range(num_files)]
filename = ['{0:05d}.png'.format(num_files-i-1) for i in range(num_files)]

print map(field_profile_and_save, x2_position, filename)


pool = Pool()
pool.map(field_profile_and_save, x2_position, filename)
pool.close()
pool.join()

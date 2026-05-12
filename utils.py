# METRICS: methods to compute distances and angles from coordinates
import numpy as np
from geopy.distance import great_circle

def distance_coords_to_meters(lon0, lat0, lon1, lat1):
  return great_circle((lat1, lon1), (lat0, lon0)).m

def directionNE(dx, dy):
  return np.mod(np.pi/2.-np.arctan2(dy,dx),2.*np.pi)

# DIRECTIONS: computing changes in orientation and averages
import numpy as np

def abs_directional_change_rad(alp0, alp1):
  dalp = np.abs(alp1-alp0)
  if dalp > np.pi:
    dalp = 2*np.pi - dalp
  return dalp

def directional_change_rad(alp0, alp1):
  dalp = alp1-alp0
  if dalp > np.pi:
    dalp = dalp - 2*np.pi
  if dalp < -np.pi:
    dalp = dalp + 2*np.pi
  return dalp

def average_angle(alps, unit_is_rads):
  alps = alps if unit_is_rads else [np.deg2rad(alp) for alp in alps]
  dxdy = np.sum(np.array([[np.cos(alp),np.sin(alp)] for alp in alps]),axis=0)
  average = np.arctan2(dxdy[1],dxdy[0])
  return average if unit_is_rads else np.rad2deg(average)

# PLOTTING
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def map_plot(title="", figsize=(10,8), add_land_coastline=[True,True], extent=None, grid_ticks=None, colors=[], add_tiles=False): #[(0.86,1.,0.73),(0.69,0.77,0.8),'gold']
  fig = plt.figure(figsize=figsize)
  ax = plt.axes(projection=ccrs.PlateCarree())
  if add_land_coastline[0]:
    if colors:
      ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=4, zorder=99, edgecolor=colors[2])
    else:
      ax.add_feature(cfeature.COASTLINE.with_scale('10m'), zorder=99)
  if add_land_coastline[1]:
    if colors:
      ax.add_feature(cfeature.LAND.with_scale('10m'),facecolor=colors[0])
      ax.add_feature(cfeature.OCEAN, facecolor=colors[1])
    else:
      ax.add_feature(cfeature.LAND.with_scale('10m'))
  gl = ax.gridlines(draw_labels=['left','bottom'])
  if extent:
    ax.set_xlim(extent[0])
    ax.set_ylim(extent[1])
    if grid_ticks:
      gl.xlocator = mticker.FixedLocator(np.linspace(extent[0][0],extent[0][1],grid_ticks[0]))
      gl.ylocator = mticker.FixedLocator(np.linspace(extent[1][0],extent[1][1],grid_ticks[1]))
      gl.xformatter = LONGITUDE_FORMATTER
      gl.yformatter = LATITUDE_FORMATTER
  if add_tiles:
    tiles = cimgt.OSM()
    ax.add_image(tiles, 19)
  if title:
    ax.set_title(title)
  return fig, ax

# SAMPLING: access and process multi-dimensional data (position, time)
import numpy as np

def sample_area_mesh_values(mesh, sample, area_radius_meters):
  # mesh = {"lons":lons, "lats":lats, "times":times, "vals":vals} with time optional, assert order vals[time_index][position_index] or vals[position_index]
  # sample = {"lon":lon, "lat":lat, "time":time} with time optional
  # sample_nearest_mesh_value({"lons":,"lats":,"times":,"vals":},{"lon":,"lat":,"time":})  with times and time optional
  # indexing
  vals = mesh["vals"][np.argmin(np.abs(sample["time"]-np.array(mesh["times"])))] if "time" in sample else mesh["vals"]
  coords = np.array([mesh["lons"],mesh["lats"]]).T
  coords_flat = flatten_coords_deg_NE(coords)
  vals, coords_flat = extract_nans_from_mesh(vals, coords_flat)
  sample_coords_flat = flatten_coords_deg_NE(np.array([[sample["lon"]],[sample["lat"]]]).T)[0]
  # sampling
  vals_area, _, _, dists_norm, inds_area = get_area_eulerian_fast_values_from_mesh(sample_coords_flat, vals, coords_flat, area_radius_meters)
  return vals_area, coords[inds_area], dists_norm

def get_area_eulerian_fast_values_from_mesh(pos, vals, mesh, area_radius):
  taxicab_dists = np.abs(pos[0]-mesh[:,0])+np.abs(pos[1]-mesh[:,1])
  inds_close = np.where(taxicab_dists < 1.5*area_radius)[0]
  vals_area, mesh_area, mesh_dist, dists_norm, inds_area = get_area_eulerian_value_from_mesh(pos, vals[inds_close], mesh[inds_close], area_radius)
  return vals_area, mesh_area, mesh_dist, dists_norm, inds_close[inds_area]

def get_area_eulerian_value_from_mesh(pos, vals, mesh, area_radius):
  dists = np.linalg.norm(np.subtract(pos,mesh), axis=1)
  inds_area = np.where(dists<=area_radius)[0]
  mesh_area = mesh[inds_area,:]
  mesh_dist = pos-mesh_area
  dists_norm = np.linalg.norm(mesh_dist,axis=1)
  return vals[inds_area], mesh_area, mesh_dist, dists_norm, inds_area

def sample_nearest_mesh_value(mesh, sample, surroundings_distance_meters=None):
  # mesh = {"lons":lons, "lats":lats, "times":times, "vals":vals} with time optional, assert order vals[time_index][position_index] or vals[position_index]
  # sample = {"lon":lon, "lat":lat, "time":time} with time optional
  # sample_nearest_mesh_value({"lons":,"lats":,"times":,"vals":},{"lon":,"lat":,"time":})
  # indexing
  vals = mesh["vals"][np.argmin(np.abs(sample["time"]-np.array(mesh["times"])))] if "time" in sample else mesh["vals"]
  coords_flat = flatten_coords_deg_NE(np.array([mesh["lons"],mesh["lats"]]).T)
  vals, coords_flat = extract_nans_from_mesh(vals, coords_flat)
  sample_coords_flat = flatten_coords_deg_NE(np.array([[sample["lon"]],[sample["lat"]]]).T)[0]
  # sampling
  vs, _, _, dist_vs = get_closest_eulerian_fast_value_from_mesh(sample_coords_flat, vals, coords_flat)
  vs_surroundings = np.zeros(4) if surroundings_distance_meters else None
  if surroundings_distance_meters:
    dx = surroundings_distance_meters
    displacements = [[+dx,0],[-dx,0],[0,+dx],[0,-dx]]
    for i, disp in enumerate(displacements):
      vs_surroundings[i], _, _, _ = get_closest_eulerian_fast_value_from_mesh(sample_coords_flat+disp, vals, coords_flat)
  return vs, dist_vs, vs_surroundings

def get_closest_eulerian_fast_value_from_mesh(pos, vals, coords, max_distance=None):
  taxicab_dists = np.abs(pos[0]-coords[:,0])+np.abs(pos[1]-coords[:,1])
  ind_min = np.argmin(taxicab_dists)
  inds_close = np.where(taxicab_dists < 1.5*taxicab_dists[ind_min])
  val_minpos, coords_minpos, coords_dist, dist_norm = get_closest_eulerian_value_from_mesh(pos, vals[inds_close], coords[inds_close])
  if max_distance != None:
    if dist_norm > max_distance:
      return None, None, None, None
  return val_minpos, coords_minpos, coords_dist, dist_norm

def get_closest_taxicab_value_from_mesh(pos, vals, coords):
  ind_min = np.argmin(np.abs(pos[0]-coords[:,0])+np.abs(pos[1]-coords[:,1]))
  coords_minpos = coords[ind_min,:]
  coords_dist = pos-coords_minpos
  return vals[ind_min], coords_minpos, coords_dist

def get_closest_eulerian_value_from_mesh(pos, vals, coords):
  dists = np.linalg.norm(np.subtract(pos,coords), axis=1)
  ind_min = np.argmin(dists)
  coords_minpos = coords[ind_min,:]
  coords_dist = pos-coords_minpos
  dist_norm = np.linalg.norm(coords_dist)
  return vals[ind_min], coords_minpos, coords_dist, dist_norm

# TODO replace with distance metric?
def flatten_coords_deg_NE(coords):
  R_earth = 6378*1000
  C_earth = np.pi * 2 * R_earth
  coords_flat = coords * (C_earth/360)
  coords_flat[:,0] *= np.cos(np.deg2rad(coords[:,1]))
  return coords_flat

def extract_nans_from_mesh(vals, coords):
  nonnan_indices = ~np.isnan(vals)
  vals_nonnan = vals[nonnan_indices]
  coords_nonnan = coords[nonnan_indices]
  return vals_nonnan, coords_nonnan

def get_gradient_direction_NE_from_rectangular_grid_axes(vals, axes_ticks):
  lon = axes_ticks[0]
  lat = axes_ticks[1]
  dlon = np.mean(lon[1:]-lon[:-1])*np.cos(np.deg2rad(lat))
  dlat = np.mean(lat[1:]-lat[:-1])
  dvdlon, dvdlat = np.gradient(vals)
  direction = np.arctan2(dvdlat*dlat, dvdlon*dlon)
  directionNE = (-direction-np.pi/2.)%(2.*np.pi)
  return directionNE

def downsample_set_with_rectangular_grid_axes(vals, axes_ticks, downsample_step):
  axis_ticks_x = axes_ticks[0]
  axis_ticks_y = axes_ticks[1]
  n_ticks_x = (int) (axis_ticks_x.shape[0]/downsample_step)-1
  n_ticks_y = (int) (axis_ticks_y.shape[0]/downsample_step)-1
  vals_ds = np.zeros((n_ticks_x, n_ticks_y))
  axis_ticks_x_ds = np.zeros(n_ticks_x)
  axis_ticks_y_ds = np.zeros(n_ticks_y)
  for ix in range(0, n_ticks_x):
    for iy in range(0, n_ticks_y):
      indx = ix*downsample_step
      indy = iy*downsample_step
      axis_ticks_x_ds[ix] = np.mean(axis_ticks_x[indx:indx+downsample_step])
      axis_ticks_y_ds[iy] = np.mean(axis_ticks_y[indy:indy+downsample_step])
      vals_ds[ix,iy] = np.mean(vals[indx:indx+downsample_step,indy:indy+downsample_step])
  return vals_ds, (axis_ticks_x_ds, axis_ticks_y_ds)

def get_mesh_from_rectangular_grid_axes(vals, axes_ticks, downsample_step=None):
  if downsample_step is not None:
    vals, axes_ticks = downsample_set_with_rectangular_grid_axes(vals, axes_ticks, downsample_step)
  axis_ticks_x = axes_ticks[0]
  axis_ticks_y = axes_ticks[1]
  n_ticks_x = axis_ticks_x.shape[0]
  n_ticks_y = axis_ticks_y.shape[0]
  n_positions = n_ticks_x*n_ticks_y
  vals_mesh = np.zeros(n_positions)
  coords_mesh = np.zeros((n_positions,2))
  mesh_index_from_grid_indices = np.zeros((n_ticks_x,n_ticks_y),dtype=int)
  for ix in range(0, n_ticks_x):
    for iy in range(0, n_ticks_y):
      ind_mesh = ix*n_ticks_y+iy
      vals_mesh[ind_mesh] = vals[ix,iy]
      coords_mesh[ind_mesh] = [axis_ticks_x[ix],axis_ticks_y[iy]]
      mesh_index_from_grid_indices[ix,iy] = ind_mesh
  return vals_mesh, coords_mesh, mesh_index_from_grid_indices

def get_closest_taxicab_value_from_rectangular_grid_axes(pos, vals, axes_ticks):
  ix_min = np.argmin(np.abs(pos[0]-axes_ticks[0]))
  iy_min = np.argmin(np.abs(pos[1]-axes_ticks[1]))
  coords_minpos = np.array([axes_ticks[0][ix_min], axes_ticks[1][iy_min]])
  coords_dist = pos-coords_minpos
  return vals[ix_min,iy_min], coords_minpos, coords_dist

def get_nonuniform_range_window(nonuniform_range, target_center_value, target_window_size):
  i_center_value = np.argmin(np.abs(nonuniform_range-target_center_value))
  i_start_window = np.argmin(np.abs(nonuniform_range-(target_center_value-target_window_size/2.)))
  n_size_window = np.argmin(np.abs(nonuniform_range-(target_center_value+target_window_size/2.)))-i_start_window
  window_size = nonuniform_range[i_start_window+n_size_window]-nonuniform_range[i_start_window]
  center_value = nonuniform_range[i_center_value]
  return i_start_window, n_size_window, window_size, i_center_value, center_value

# takes two lists of indices 'inds' and 'inds_target'
# maps each index in 'inds' to the next >= index in 'inds_target'
# returns the projected indices and the indices of the this projection 'inds'>'inds_target'
def map_to_next_available_index(inds, inds_target):
  N = inds.shape[0]
  it_ind_max = inds_target.shape[0]-1
  inds_projected = np.zeros((N,2),dtype=np.int32)
  for i in range(N):
    inds_gt = np.where(inds_target >= inds[i])[0]
    if len(inds_gt):
      it_ind = inds_gt[0]
    else:
      it_ind = it_ind_max
    inds_projected[i,0] = inds_target[it_ind]
    inds_projected[i,1] = it_ind
  return inds_projected

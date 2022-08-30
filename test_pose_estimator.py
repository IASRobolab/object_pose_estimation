from pathlib import Path
from pose_estimator import PoseEstimator
import open3d as o3d
import copy

yolact_weights = str(Path.home()) + "/Code/Vision/yolact/weights/yolact_plus_resnet50_54_800000.pth"
estimator = PoseEstimator(camera_type = 'REALSENSE',
                            obj_label = 'cup', 
                            obj_model_file = 'cup.ply', 
                            yolact_weights = yolact_weights, 
                            voxel_size = 0.0025)

filt_type = 'STATISTICAL'
filt_params_dict = {'nb_neighbors': 100, 'std_ratio': 0.1}

# filt_type = 'RADIUS'
# filt_params_dict = {'nb_points': 16, 'radius': 0.0025*2.5}

obs_pcd = estimator.get_yolact_pcd(filt_type, filt_params_dict)
obs_pcd.paint_uniform_color([0, 0.651, 0.929])
T_gl = estimator.global_registration(obs_pcd)

model_glob = copy.deepcopy(estimator.model_pcd).transform(T_gl)
model_glob.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([model_glob, obs_pcd], window_name = 'Global registration')

T_icp = estimator.local_registration(obs_pcd, T_gl)


model_icp = copy.deepcopy(estimator.model_pcd).transform(T_icp)
model_icp.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([model_icp, obs_pcd], window_name = 'Point-to-point ICP')





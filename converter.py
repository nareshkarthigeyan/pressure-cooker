import os
import trimesh
import open3d as o3d
import numpy as np

def ensure_output_dir(output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def create_sample_cad(filename='sample.stl', output_dir='output'):
    """Creates a sample torus mesh in the output directory."""
    full_path = os.path.join(output_dir, filename)
    mesh = trimesh.creation.torus(major_radius=1.0, minor_radius=0.25)
    mesh.export(full_path)
    print(f"[Generator] Created sample CAD file: {full_path}")
    return full_path

def to_point_cloud(input_mesh_path, output_filename='cloud.pcd', output_dir='output', num_points=4096):
    """Converts mesh file to point cloud."""
    print(f"[Converter] Converting {input_mesh_path} to Point Cloud...")
    mesh = trimesh.load(input_mesh_path)
    
    # Sample points
    points, _ = trimesh.sample.sample_surface(mesh, num_points)
    
    # Create Open3D PointCloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    
    output_path = os.path.join(output_dir, output_filename)
    o3d.io.write_point_cloud(output_path, pcd)
    print(f"[Converter] Saved Point Cloud to {output_path}")
    return output_path

def to_voxel(input_mesh_path, output_filename='voxel.ply', output_dir='output', pitch=0.05):
    """Converts mesh file to voxel grid."""
    print(f"[Converter] Converting {input_mesh_path} to Voxel Grid...")
    mesh = trimesh.load(input_mesh_path)
    
    # Voxelize using trimesh
    voxel_grid = mesh.voxelized(pitch=pitch)
    
    # Convert to Open3D VoxelGrid for consistency in file format (save as PLY)
    # We create a VoxelGrid from the filled points
    points = voxel_grid.points
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Create o3d voxel grid
    v_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=pitch)
    
    output_path = os.path.join(output_dir, output_filename)
    o3d.io.write_voxel_grid(output_path, v_grid)
    print(f"[Converter] Saved Voxel Grid to {output_path}")
    return output_path

def to_mesh_format(input_mesh_path, output_filename='mesh.ply', output_dir='output'):
    """Standardizes input CAD to PLY mesh format in output folder."""
    print(f"[Converter] Standardizing Mesh to {output_filename}...")
    mesh = trimesh.load(input_mesh_path)
    output_path = os.path.join(output_dir, output_filename)
    mesh.export(output_path)
    print(f"[Converter] Saved Mesh to {output_path}")
    return output_path

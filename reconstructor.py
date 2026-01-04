import os
import open3d as o3d
import trimesh
import numpy as np

def pcd_to_cad(input_pcd_path, output_filename='reconstructed_from_pcd.ply', output_dir='output'):
    """Reconstructs a mesh (CAD) from a Point Cloud using Ball Pivoting."""
    print(f"[Reconstructor] Reconstructing CAD from Point Cloud: {input_pcd_path}...")
    
    pcd = o3d.io.read_point_cloud(input_pcd_path)
    if not pcd.has_normals():
        pcd.estimate_normals()
        
    # Estimate radii for BPA
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radii = [avg_dist * k for k in [1, 2, 4]]
    
    # Run BPA
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))
    
    # Post-process
    # mesh = mesh.simplify_quadric_decimation(1000) # Optional simplification
    # mesh.compute_vertex_normals()
    
    output_path = os.path.join(output_dir, output_filename)
    o3d.io.write_triangle_mesh(output_path, mesh)
    print(f"[Reconstructor] Saved Reconstructed Mesh (PCD Source) to {output_path}")
    return output_path

def voxel_to_cad(input_voxel_path, output_filename='reconstructed_from_voxel.ply', output_dir='output', pitch=0.05):
    """Reconstructs a mesh (CAD) from a Voxel grid (approximated as boxes/lego)."""
    print(f"[Reconstructor] Reconstructing CAD from Voxel Data: {input_voxel_path}...")
    
    # Load points from the Voxel PLY
    pcd = o3d.io.read_point_cloud(input_voxel_path)
    points = np.asarray(pcd.points)
    
    # Since trimesh.voxel.creation.voxelize expects a Mesh, and we have points,
    # we will manually create a box for each voxel center.
    # This is a robust way to visualize "Voxel to Mesh" (Lego style).
    
    print(f"[Reconstructor] generating boxes for {len(points)} voxels...")
    
    # Create a unit box
    box_template = trimesh.creation.box(extents=(pitch, pitch, pitch))
    
    # We can speed this up by not creating objects but just verifying logic
    # But trimesh.util.concatenate is decent. 
    # For very large grids, we would use a VoxelGrid object, but constructing it from loose points 
    # in trimesh requires setting up the encoding and transform manually, which is error-prone.
    
    boxes = []
    for p in points:
        # Create a copy of the template
        b = box_template.copy()
        b.apply_translation(p)
        boxes.append(b)
        
    if boxes:
        mesh = trimesh.util.concatenate(boxes)
        output_path = os.path.join(output_dir, output_filename)
        mesh.export(output_path)
        print(f"[Reconstructor] Saved Reconstructed Mesh (Voxel Source) to {output_path}")
        return output_path
    else:
        print("[Reconstructor] No voxels found!")
        return None

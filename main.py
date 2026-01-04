import os
import converter
import reconstructor
import visualizer

def main():
    print("=== CAD Pipeline Started ===")
    
    # 0. Setup
    output_dir = 'output'
    converter.ensure_output_dir(output_dir)
    
    # 1. Input Generation (or Selection)
    import sys
    input_cad = sys.argv[1] if len(sys.argv) > 1 else converter.create_sample_cad('sample_torus.stl', output_dir)
    
    # Initialize variables to None to handle skipped steps safely
    pcd_path = None
    voxel_path = None
    mesh_path = None
    recon_from_pcd = None
    recon_from_voxel = None

    # 2. Forward Conversion: CAD -> PCD, Voxel, Mesh(Clean)
    print("\n--- Phase 1: Forward Conversion ---")
    
    # Always try to convert to PCD
    if os.path.exists(input_cad):
        pcd_path = converter.to_point_cloud(input_cad, 'converted_cloud.pcd', output_dir)
    
    # Optional: Voxelization (can be slow on large meshes)
    # voxel_path = converter.to_voxel(input_cad, 'converted_voxel.ply', output_dir)
    
    # Optional: Standardize Mesh
    # mesh_path = converter.to_mesh_format(input_cad, 'converted_mesh.ply', output_dir)
    
    # 3. Backward Reconstruction: PCD/Voxel -> CAD (Mesh)
    print("\n--- Phase 2: Reconstruction ---")
    if pcd_path:
        recon_from_pcd = reconstructor.pcd_to_cad(pcd_path, 'recon_from_pcd.ply', output_dir)
    
    if voxel_path:
        recon_from_voxel = reconstructor.voxel_to_cad(voxel_path, 'recon_from_voxel.ply', output_dir)
    
    # 4. Visualization
    print("\n--- Phase 3: Visualization ---")
    
    items_to_show = []
    
    # Add items if they exist
    # Use input_cad if standardized mesh_path wasn't created
    if mesh_path and os.path.exists(mesh_path):
        items_to_show.append({'path': mesh_path, 'type': 'mesh', 'title': 'Original/Converted Mesh'})
    elif input_cad and os.path.exists(input_cad):
         items_to_show.append({'path': input_cad, 'type': 'mesh', 'title': 'Original Input Mesh'})

    if pcd_path and os.path.exists(pcd_path):
        items_to_show.append({'path': pcd_path, 'type': 'pcd', 'title': 'Point Cloud Representation'})
        
    if voxel_path and os.path.exists(voxel_path):
        items_to_show.append({'path': voxel_path, 'type': 'voxel', 'title': 'Voxel Representation'})
        
    if recon_from_pcd and os.path.exists(recon_from_pcd):
        items_to_show.append({'path': recon_from_pcd, 'type': 'mesh', 'title': 'Reconstruction from PCD (BPA)'})
        
    if recon_from_voxel and os.path.exists(recon_from_voxel):
        items_to_show.append({'path': recon_from_voxel, 'type': 'mesh', 'title': 'Reconstruction from Voxel (Boxes)'})
    
    if items_to_show:
        visualizer.visualize_files(items_to_show)
    else:
        print("Nothing to visualize!")
    
    print("=== Pipeline Finished ===")

if __name__ == "__main__":
    main()

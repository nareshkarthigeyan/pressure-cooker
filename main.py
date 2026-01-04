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
    # For now, we generate a sample. In a real app, this might be a user argument.
    input_cad = converter.create_sample_cad('sample_torus.stl', output_dir)
    
    # 2. Forward Conversion: CAD -> PCD, Voxel, Mesh(Clean)
    print("\n--- Phase 1: Forward Conversion ---")
    pcd_path = converter.to_point_cloud(input_cad, 'converted_cloud.pcd', output_dir)
    voxel_path = converter.to_voxel(input_cad, 'converted_voxel.ply', output_dir)
    mesh_path = converter.to_mesh_format(input_cad, 'converted_mesh.ply', output_dir)
    
    # 3. Backward Reconstruction: PCD/Voxel -> CAD (Mesh)
    print("\n--- Phase 2: Reconstruction ---")
    recon_from_pcd = reconstructor.pcd_to_cad(pcd_path, 'recon_from_pcd.ply', output_dir)
    recon_from_voxel = reconstructor.voxel_to_cad(voxel_path, 'recon_from_voxel.ply', output_dir)
    
    # 4. Visualization
    print("\n--- Phase 3: Visualization ---")
    
    # We define what to show. 
    # Let's show: Original Mesh, Generated PCD, Generated Voxel, Recon(PCD), Recon(Voxel)
    # That's 5 windows.
    items_to_show = [
        {'path': mesh_path,       'type': 'mesh',  'title': 'Original/Converted Mesh'},
        {'path': pcd_path,        'type': 'pcd',   'title': 'Point Cloud Representation'},
        {'path': voxel_path,      'type': 'voxel', 'title': 'Voxel Representation'},
        {'path': recon_from_pcd,  'type': 'mesh',  'title': 'Reconstruction from PCD (BPA)'},
        {'path': recon_from_voxel,'type': 'mesh',  'title': 'Reconstruction from Voxel (Boxes)'}
    ]
    
    visualizer.visualize_files(items_to_show)
    
    print("=== Pipeline Finished ===")

if __name__ == "__main__":
    main()

import open3d as o3d
import multiprocessing
import os

# Top-level functions for multiprocessing compatibility

def _show_mesh_process(path, title, width, height, left, top):
    import open3d as o3d
    try:
        mesh = o3d.io.read_triangle_mesh(path)
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh], window_name=title, width=width, height=height, left=left, top=top)
    except Exception as e:
        print(f"Error visualizing mesh {path}: {e}")

def _show_pcd_process(path, title, width, height, left, top):
    import open3d as o3d
    try:
        pcd = o3d.io.read_point_cloud(path)
        o3d.visualization.draw_geometries([pcd], window_name=title, width=width, height=height, left=left, top=top)
    except Exception as e:
        print(f"Error visualizing pcd {path}: {e}")

def _show_voxel_process(path, title, width, height, left, top):
    import open3d as o3d
    try:
        # Try reading as VoxelGrid first
        voxel = o3d.io.read_voxel_grid(path)
        if not voxel.has_voxels():
             # Fallback: Read as PCD and voxelize on the fly for display
             pcd = o3d.io.read_point_cloud(path)
             voxel = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.05)
        
        o3d.visualization.draw_geometries([voxel], window_name=title, width=width, height=height, left=left, top=top)
    except Exception as e:
        print(f"Error visualizing voxel {path}: {e}")

def visualize_files(files_metadata):
    """
    Spawns multiple processes to visualize files.
    files_metadata: List of dicts {'path': str, 'type': 'mesh'|'pcd'|'voxel', 'title': str}
    """
    print("[Visualizer] Launching visualization windows...")
    
    processes = []
    
    # Layout logic: simple grid
    screen_width = 1920
    screen_height = 1080
    win_width = 500
    win_height = 500
    padding = 50
    
    current_left = padding
    current_top = padding
    
    for i, meta in enumerate(files_metadata):
        path = meta['path']
        ftype = meta['type']
        title = meta.get('title', f"Window {i}")
        
        target_func = None
        if ftype == 'mesh':
            target_func = _show_mesh_process
        elif ftype == 'pcd':
            target_func = _show_pcd_process
        elif ftype == 'voxel':
            target_func = _show_voxel_process
            
        if target_func:
            p = multiprocessing.Process(
                target=target_func, 
                args=(path, title, win_width, win_height, current_left, current_top)
            )
            processes.append(p)
            
            # Update position
            current_left += win_width + padding
            if current_left + win_width > screen_width:
                current_left = padding
                current_top += win_height + padding
                
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
    
    print("[Visualizer] All windows closed.")

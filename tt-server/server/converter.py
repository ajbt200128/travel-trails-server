import time

import open3d as o3d

import numpy as np
import matplotlib.pyplot as plt
import copy

def highlight_mesh(mesh, densities, threshold):
    vertices_to_remove = densities < np.quantile(densities, threshold)

    base_mesh = copy.deepcopy(mesh)
    base_mesh.remove_vertices_by_mask(vertices_to_remove)

    densities = np.asarray(densities)
    density_colors = plt.get_cmap('plasma')(
        (densities - densities.min()) / (densities.max() - densities.min()))
    density_colors = density_colors[:, :3]
    # reverse color map

    heatmap_mesh = o3d.geometry.TriangleMesh()
    heatmap_mesh.vertices = mesh.vertices
    heatmap_mesh.triangles = mesh.triangles
    heatmap_mesh.triangle_normals = mesh.triangle_normals
    heatmap_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
    heatmap_mesh.remove_vertices_by_mask(~vertices_to_remove)

    density_mesh = o3d.geometry.TriangleMesh()
    density_mesh += heatmap_mesh
    density_mesh += base_mesh
    return density_mesh

def convert_ply(ply_path, output_path, display=False, heatmap=0.0, visualize=False):
    print("Loading mesh from {}".format(ply_path))
    print("Converting to {}".format(output_path))
    ply_path = str(ply_path)
    output_path = str(output_path)
    if visualize:
        # Open output path
        o3d.visualization.draw_geometries([o3d.io.read_triangle_mesh(output_path)])
        return
    start_time = time.time()
    pcd = o3d.io.read_point_cloud(ply_path)
    pcd = pcd.uniform_down_sample(every_k_points=15)
    cl, _ = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=0.000001)
    pcd = cl
    pcd.estimate_normals()
    print("Downsampled point cloud with %d points." % len(pcd.points), flush=True)
    print("Time taken: %f" % (time.time() - start_time), flush=True)
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as _:
        start_time = time.time()
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=12
        )
        print("Surface reconstruction took %s seconds" % (time.time() - start_time), flush=True)

        if heatmap > 0:
            mesh = highlight_mesh(mesh, densities, heatmap)
        o3d.io.write_triangle_mesh(output_path, mesh)
        if display:
            o3d.visualization.draw_geometries([mesh])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ply_path", type=str)
    parser.add_argument("output_path", type=str)
    parser.add_argument("--heatmap", type=float, default=0.0)
    parser.add_argument("--visualize", action="store_true", default=False)
    args = parser.parse_args()

    convert_ply(args.ply_path, args.output_path, display=True, heatmap=args.heatmap, visualize=args.visualize)

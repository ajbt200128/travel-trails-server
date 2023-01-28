import time

import open3d as o3d


def convert_ply(ply_path, output_path, display=False):
    start_time = time.time()
    pcd = o3d.io.read_point_cloud(ply_path)
    pcd = pcd.uniform_down_sample(every_k_points=40)
    cl, _ = pcd.remove_statistical_outlier(nb_neighbors=300, std_ratio=0.000001)
    pcd = cl
    pcd.estimate_normals()
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as _:
        start_time = time.time()
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=12
        )
        print("Surface reconstruction took %s seconds" % (time.time() - start_time))

        o3d.io.write_triangle_mesh(output_path, mesh)
        if display:
            o3d.visualization.draw_geometries([mesh])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ply_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    convert_ply(args.ply_path, args.output_path, display=True)

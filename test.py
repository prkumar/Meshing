from meshing import mesh


off_file = "models/elephant.off"

connectivity = mesh.MeshConnectivity.load_mesh(off_file)

print("Performing edge collapse...")
connectivity.edge_collapse(0, 1)
print("Done!")

print("Saving new mesh...")
connectivity.save()
print("Done!")

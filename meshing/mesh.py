# Standard-library imports
import atexit
import collections
import itertools

# Third-party imports
import numpy as np
import pyassimp


def unique_2d(matrix):
    uniques = collections.OrderedDict()
    indices = []
    for i, vert in enumerate(matrix):
        key = tuple(vert)
        if key not in uniques:
            uniques[key] = len(uniques)
        indices.append(uniques[key])
    uniques, indices = np.asarray(uniques.keys()), np.asarray(indices)
    assert ((uniques[indices] == matrix).all())
    return uniques, indices


def _map_set(func, iterables):
    return set(itertools.chain(map(func, iterables)))


def set_true(values, size):
    new_row = np.zeros(size, dtype=bool)
    new_row[values] = True
    return new_row


class MeshConnectivity(object):
    @classmethod
    def load_mesh(cls, filename):
        print("Loading Mesh...")
        scene = pyassimp.load(filename)
        print("Done!")
        atexit.register(pyassimp.release, scene)
        return cls(scene.meshes[0])

    def __init__(self, mesh):
        self._mesh = mesh
        vertices, indices = unique_2d(mesh.vertices)
        faces = np.apply_along_axis(indices.__getitem__, 1, mesh.faces)
        num_vertices, num_faces = len(vertices), len(faces)
        print("Building adjacency matrix...")
        vertices = dict(zip(range(num_vertices), vertices))
        faces = dict(zip(range(num_faces), faces))
        vertex_to_faces = collections.defaultdict(set)
        for i, (v1, v2, v3) in faces.items():
            vertex_to_faces[v1].add(i)
            vertex_to_faces[v2].add(i)
            vertex_to_faces[v3].add(i)
        print("Done")
        self.faces = faces
        self.vertex_to_faces = vertex_to_faces
        self.vertices = vertices

    def find_adjacent_vertices_of_face(self, face):
        return self.faces[face]

    def find_adjacent_faces_of_vertex(self, vertex):
        return self.vertex_to_faces[vertex]

    def find_neighboring_faces_of_face(self, face):
        neighbors = _map_set(
            self.find_adjacent_faces_of_vertex,
            self.find_adjacent_vertices_of_face(face)
        )
        neighbors.remove(face)
        return list(sorted(neighbors))

    def find_neighboring_vertices_of_vertex(self, vertex):
        neighbors = _map_set(
            self.find_neighboring_faces_of_face,
            self.find_adjacent_faces_of_vertex(vertex)
        )
        neighbors.remove(vertex)
        return list(sorted(neighbors))

    def replace_vertices(self, new_vertex, v0, v1):
        # Swap vertex
        assert(v0 != v1 and v0 in self.vertices and v1 in self.vertices)
        print(self.vertices[v0], self.vertices[v1])
        s_i = min(v0, v1)
        other = max(v0, v1)
        s_v = self.vertices.pop(s_i)
        other_v = self.vertices.pop(other)
        self.vertices[s_i] = new_vertex

        # Handle faces
        faces_1 = set(self.find_adjacent_faces_of_vertex(s_i))
        faces_2 = set(self.find_adjacent_faces_of_vertex(other))

        # Categorize neighboring faces
        unique_faces = faces_1.symmetric_difference(faces_2)
        update_faces = unique_faces - faces_1
        overlapping_faces = faces_1.intersection(faces_2)

        self.vertex_to_faces[s_i] = unique_faces
        for face in update_faces:
            self.faces[face][self.faces[face] == other] = s_i

        # Remove overlapping (degenerate) faces.
        removed = []
        self.vertex_to_faces.pop(other)
        for face in overlapping_faces:
            print(self.faces[face], s_i)
            not_s_i = self.faces[face][self.faces[face] != s_i]
            removed.append(not_s_i[not_s_i[0] == other])
            self.faces.pop(face)
        return s_i, s_v, other, other_v, overlapping_faces, update_faces, removed

    def vertex_split(self, s_i, s_v, other, other_v, overlapping_faces, update_faces, removed):
        unique_faces = self.vertex_to_faces[s_i]
        faces_2 = overlapping_faces.union(update_faces)
        faces_1 = overlapping_faces.union(unique_faces - faces_2)
        self.vertices[s_i] = s_v
        self.vertices[other] = other_v
        self.vertex_to_faces[s_i] = faces_1
        self.vertex_to_faces[other] = faces_2
        for face in update_faces:
            self.faces[face][self.faces[face] == s_i] = other
        for face, r in zip(overlapping_faces, removed):
            self.faces[face] = np.asarray([s_i, other, r])

    def edge_collapse(self, v0, v1):
        # Find midpoint
        midpoint = (self.vertices[v0] + self.vertices[v1]) * -0.15
        return self.replace_vertices(midpoint, v0, v1)

    def save(self):
        faces = np.zeros((len(self.faces), 3), dtype=self._mesh.faces.dtype)
        vertices = []
        start = np.asarray([0, 1, 2])
        for i, face in enumerate(self.faces.values()):
            vertex_indices = start + (i * 3)
            faces[i] = vertex_indices
            print(vertex_indices)
            vertices.append(self.vertices[face[0]])
            vertices.append(self.vertices[face[1]])
            vertices.append(self.vertices[face[2]])
        self._mesh.vertices = np.asarray(vertices, dtype=self._mesh.vertices.dtype)
        self._mesh.faces = faces
        return self._mesh


def load_mesh(filename):
    scene = pyassimp.load(filename)
    mesh = scene.meshes[0]

    # Create Indexed Set
    vertices = collections.OrderedDict()
    indices = []
    for i, vert in enumerate(mesh.vertices):
        key = tuple(vert)
        if key not in vertices:
            vertices[key] = len(vertices)
        indices.append(vertices[key])
    vertices, indices = np.asarray(vertices.keys()), np.asarray(indices)
    faces = np.apply_along_axis(indices.__getitem__, 1, mesh.faces)
    vertex_face_adjacency = collections.defaultdict(set)
    for i, (v1, v2, v3) in enumerate(faces):
        vertex_face_adjacency[v1].add(i)
        vertex_face_adjacency[v2].add(i)
        vertex_face_adjacency[v3].add(i)
    print(len(vertices), len(faces))






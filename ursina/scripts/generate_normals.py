# import numpy




def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    import numpy
    
    lens = numpy.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens
    return arr


def generate_normals(vertices, triangles=None, smooth=True, inverse=False):
    import numpy

    if not triangles:
        # print('generated triangles:', triangles)
        new_tris = [(i, i+1, i+2) for i in range(0, len(vertices), 3)]
    else:
        new_tris = list()
        for t in triangles:
            if isinstance(t, int):
                new_tris.append(t)
            elif len(t) == 3:
                new_tris.extend(t)
            elif len(t) == 4:
                new_tris.extend((t[0], t[1], t[2], t[2], t[3], t[0]))

        new_tris = [(new_tris[i], new_tris[i+1], new_tris[i+2]) for i in range(0, len(new_tris), 3)]


    vertices = numpy.array(vertices)
    triangles = numpy.array(new_tris)

    normals = numpy.zeros(vertices.shape, dtype=vertices.dtype)
    #Create an indexed view into the vertex array using the array of three indices for triangles
    tris = vertices[triangles]
    #Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle
    n = numpy.cross(tris[::,1] - tris[::,0] ,tris[::,2] - tris[::,0])
    # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
    # we need to normalize these, so that our next step weights each normal equally.
    normalize_v3(n)

    # inverse it, dunno why
    if (inverse):
        n = [-e for e in n]
    else:
        n = n

    # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
    # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
    # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
    # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
    normals[triangles[:,0]] += n
    normals[triangles[:,1]] += n
    normals[triangles[:,2]] += n
    normalize_v3(normals)

    # smooth
    if smooth:
        vertices=vertices.tolist()
        bucket = list()
        for i, v in enumerate(vertices):
            if i in bucket:
                continue

            overlapping_verts_indices = list()
            for j, w in enumerate(vertices):
                if w == v:
                    overlapping_verts_indices.append(j)
                    bucket.append(j)

            average_normal = sum([normals[e] for e in overlapping_verts_indices]) / 3
            for index in overlapping_verts_indices:
                normals[index] = average_normal


    return normals

if __name__ == '__main__':
    vertices=((-0.0, -0.5, 0.0), (0.10159, -0.483975, -0.073809), (-0.038803, -0.483975, -0.119426), (0.361804, -0.22361, -0.262863), (0.304773, -0.328759, -0.221428), (0.406365, -0.25115, -0.147619), (-0.0, -0.5, 0.0), (-0.038803, -0.483975, -0.119426), (-0.125573, -0.483974, 0.0), (-0.0, -0.5, 0.0), (-0.125573, -0.483974, 0.0), (-0.038803, -0.483975, 0.119426), (-0.0, -0.5, 0.0), (-0.038803, -0.483975, 0.119426), (0.10159, -0.483975, 0.073809), (0.361804, -0.22361, -0.262863), (0.406365, -0.25115, -0.147619), (0.430349, -0.125575, -0.221429), (-0.138194, -0.22361, -0.425325), (-0.01482, -0.251151, -0.432092), (-0.077608, -0.125576, -0.477711), (-0.447213, -0.223608, 0.0), (-0.415525, -0.251149, -0.119427), (-0.478313, -0.125575, -0.073809), (-0.138194, -0.22361, 0.425325), (-0.241986, -0.251151, 0.358282), (-0.218003, -0.125576, 0.432094), (0.361804, -0.22361, 0.262863), (0.26597, -0.251151, 0.340856), (0.343579, -0.125576, 0.340858), (0.361804, -0.22361, -0.262863), (0.430349, -0.125575, -0.221429), (0.343579, -0.125576, -0.340858), (-0.138194, -0.22361, -0.425325), (-0.077608, -0.125576, -0.477711), (-0.218003, -0.125576, -0.432094), (-0.447213, -0.223608, 0.0), (-0.478313, -0.125575, -0.073809), (-0.478313, -0.125575, 0.073809), (-0.138194, -0.22361, 0.425325), (-0.218003, -0.125576, 0.432094), (-0.077608, -0.125576, 0.477711), (0.361804, -0.22361, 0.262863), (0.343579, -0.125576, 0.340858), (0.430349, -0.125575, 0.221429), (0.138194, 0.22361, -0.425325), (0.241986, 0.251151, -0.358282), (0.116411, 0.32876, -0.358282), (-0.361804, 0.22361, -0.262863), (-0.26597, 0.251151, -0.340856), (-0.304773, 0.328759, -0.221428), (-0.361804, 0.22361, 0.262863), (-0.406365, 0.25115, 0.147619), (-0.304773, 0.328759, 0.221428), (0.138194, 0.22361, 0.425325), (0.01482, 0.251151, 0.432092), (0.116411, 0.32876, 0.358282), (0.447213, 0.223608, 0.0), (0.415525, 0.251149, 0.119427), (0.376721, 0.328757, 0.0), (0.125573, 0.483974, 0.0), (0.038803, 0.483975, 0.119426), (-0.0, 0.5, 0.0), (0.262865, 0.425326, 0.0), (0.1809, 0.447215, 0.131431), (0.125573, 0.483974, 0.0), (0.376721, 0.328757, 0.0), (0.319097, 0.361805, 0.131432), (0.262865, 0.425326, 0.0), (0.125573, 0.483974, 0.0), (0.1809, 0.447215, 0.131431), (0.038803, 0.483975, 0.119426), (0.1809, 0.447215, 0.131431), (0.081228, 0.425327, 0.249998), (0.038803, 0.483975, 0.119426), (0.262865, 0.425326, 0.0), (0.319097, 0.361805, 0.131432), (0.1809, 0.447215, 0.131431), (0.319097, 0.361805, 0.131432), (0.223605, 0.361806, 0.262864), (0.1809, 0.447215, 0.131431), (0.1809, 0.447215, 0.131431), (0.223605, 0.361806, 0.262864), (0.081228, 0.425327, 0.249998), (0.223605, 0.361806, 0.262864), (0.116411, 0.32876, 0.358282), (0.081228, 0.425327, 0.249998), (0.376721, 0.328757, 0.0), (0.415525, 0.251149, 0.119427), (0.319097, 0.361805, 0.131432), (0.415525, 0.251149, 0.119427), (0.344095, 0.262868, 0.249998), (0.319097, 0.361805, 0.131432), (0.319097, 0.361805, 0.131432), (0.344095, 0.262868, 0.249998), (0.223605, 0.361806, 0.262864), (0.344095, 0.262868, 0.249998), (0.241986, 0.251151, 0.358282), (0.223605, 0.361806, 0.262864), (0.223605, 0.361806, 0.262864), (0.241986, 0.251151, 0.358282), (0.116411, 0.32876, 0.358282), (0.241986, 0.251151, 0.358282), (0.138194, 0.22361, 0.425325), (0.116411, 0.32876, 0.358282), (0.038803, 0.483975, 0.119426), (-0.10159, 0.483975, 0.073809), (-0.0, 0.5, 0.0), (0.081228, 0.425327, 0.249998), (-0.069099, 0.447215, 0.21266), (0.038803, 0.483975, 0.119426), (0.116411, 0.32876, 0.358282), (-0.026395, 0.361806, 0.344092), (0.081228, 0.425327, 0.249998), (0.038803, 0.483975, 0.119426), (-0.069099, 0.447215, 0.21266), (-0.10159, 0.483975, 0.073809), (-0.069099, 0.447215, 0.21266), (-0.212661, 0.425327, 0.154506), (-0.10159, 0.483975, 0.073809), (0.081228, 0.425327, 0.249998), (-0.026395, 0.361806, 0.344092), (-0.069099, 0.447215, 0.21266), (-0.026395, 0.361806, 0.344092), (-0.180902, 0.361806, 0.293889), (-0.069099, 0.447215, 0.21266), (-0.069099, 0.447215, 0.21266), (-0.180902, 0.361806, 0.293889), (-0.212661, 0.425327, 0.154506), (-0.180902, 0.361806, 0.293889), (-0.304773, 0.328759, 0.221428), (-0.212661, 0.425327, 0.154506), (0.116411, 0.32876, 0.358282), (0.01482, 0.251151, 0.432092), (-0.026395, 0.361806, 0.344092), (0.01482, 0.251151, 0.432092), (-0.131434, 0.262869, 0.404506), (-0.026395, 0.361806, 0.344092), (-0.026395, 0.361806, 0.344092), (-0.131434, 0.262869, 0.404506), (-0.180902, 0.361806, 0.293889), (-0.131434, 0.262869, 0.404506), (-0.26597, 0.251151, 0.340856), (-0.180902, 0.361806, 0.293889), (-0.180902, 0.361806, 0.293889), (-0.26597, 0.251151, 0.340856), (-0.304773, 0.328759, 0.221428), (-0.26597, 0.251151, 0.340856), (-0.361804, 0.22361, 0.262863), (-0.304773, 0.328759, 0.221428), (-0.10159, 0.483975, 0.073809), (-0.10159, 0.483975, -0.073809), (-0.0, 0.5, 0.0), (-0.212661, 0.425327, 0.154506), (-0.223605, 0.447215, 0.0), (-0.10159, 0.483975, 0.073809), (-0.304773, 0.328759, 0.221428), (-0.335408, 0.361805, 0.081229), (-0.212661, 0.425327, 0.154506), (-0.10159, 0.483975, 0.073809), (-0.223605, 0.447215, 0.0), (-0.10159, 0.483975, -0.073809), (-0.223605, 0.447215, 0.0), (-0.212661, 0.425327, -0.154506), (-0.10159, 0.483975, -0.073809), (-0.212661, 0.425327, 0.154506), (-0.335408, 0.361805, 0.081229), (-0.223605, 0.447215, 0.0), (-0.335408, 0.361805, 0.081229), (-0.335408, 0.361805, -0.081229), (-0.223605, 0.447215, 0.0), (-0.223605, 0.447215, 0.0), (-0.335408, 0.361805, -0.081229), (-0.212661, 0.425327, -0.154506), (-0.335408, 0.361805, -0.081229), (-0.304773, 0.328759, -0.221428), (-0.212661, 0.425327, -0.154506), (-0.304773, 0.328759, 0.221428), (-0.406365, 0.25115, 0.147619), (-0.335408, 0.361805, 0.081229), (-0.406365, 0.25115, 0.147619), (-0.425324, 0.262868, 0.0), (-0.335408, 0.361805, 0.081229), (-0.335408, 0.361805, 0.081229), (-0.425324, 0.262868, 0.0), (-0.335408, 0.361805, -0.081229), (-0.425324, 0.262868, 0.0), (-0.406365, 0.25115, -0.147619), (-0.335408, 0.361805, -0.081229), (-0.335408, 0.361805, -0.081229), (-0.406365, 0.25115, -0.147619), (-0.304773, 0.328759, -0.221428), (-0.406365, 0.25115, -0.147619), (-0.361804, 0.22361, -0.262863), (-0.304773, 0.328759, -0.221428), (-0.10159, 0.483975, -0.073809), (0.038803, 0.483975, -0.119426), (-0.0, 0.5, 0.0), (-0.212661, 0.425327, -0.154506), (-0.069099, 0.447215, -0.21266), (-0.10159, 0.483975, -0.073809), (-0.304773, 0.328759, -0.221428), (-0.180902, 0.361806, -0.293889), (-0.212661, 0.425327, -0.154506), (-0.10159, 0.483975, -0.073809), (-0.069099, 0.447215, -0.21266), (0.038803, 0.483975, -0.119426), (-0.069099, 0.447215, -0.21266), (0.081228, 0.425327, -0.249998), (0.038803, 0.483975, -0.119426), (-0.212661, 0.425327, -0.154506), (-0.180902, 0.361806, -0.293889), (-0.069099, 0.447215, -0.21266), (-0.180902, 0.361806, -0.293889), (-0.026395, 0.361806, -0.344092), (-0.069099, 0.447215, -0.21266), (-0.069099, 0.447215, -0.21266), (-0.026395, 0.361806, -0.344092), (0.081228, 0.425327, -0.249998), (-0.026395, 0.361806, -0.344092), (0.116411, 0.32876, -0.358282), (0.081228, 0.425327, -0.249998), (-0.304773, 0.328759, -0.221428), (-0.26597, 0.251151, -0.340856), (-0.180902, 0.361806, -0.293889), (-0.26597, 0.251151, -0.340856), (-0.131434, 0.262869, -0.404506), (-0.180902, 0.361806, -0.293889), (-0.180902, 0.361806, -0.293889), (-0.131434, 0.262869, -0.404506), (-0.026395, 0.361806, -0.344092), (-0.131434, 0.262869, -0.404506), (0.01482, 0.251151, -0.432092), (-0.026395, 0.361806, -0.344092), (-0.026395, 0.361806, -0.344092), (0.01482, 0.251151, -0.432092), (0.116411, 0.32876, -0.358282), (0.01482, 0.251151, -0.432092), (0.138194, 0.22361, -0.425325), (0.116411, 0.32876, -0.358282), (0.038803, 0.483975, -0.119426), (0.125573, 0.483974, 0.0), (-0.0, 0.5, 0.0), (0.081228, 0.425327, -0.249998), (0.1809, 0.447215, -0.131431), (0.038803, 0.483975, -0.119426), (0.116411, 0.32876, -0.358282), (0.223605, 0.361806, -0.262864), (0.081228, 0.425327, -0.249998), (0.038803, 0.483975, -0.119426), (0.1809, 0.447215, -0.131431), (0.125573, 0.483974, 0.0), (0.1809, 0.447215, -0.131431), (0.262865, 0.425326, 0.0), (0.125573, 0.483974, 0.0), (0.081228, 0.425327, -0.249998), (0.223605, 0.361806, -0.262864), (0.1809, 0.447215, -0.131431), (0.223605, 0.361806, -0.262864), (0.319097, 0.361805, -0.131432), (0.1809, 0.447215, -0.131431), (0.1809, 0.447215, -0.131431), (0.319097, 0.361805, -0.131432), (0.262865, 0.425326, 0.0), (0.319097, 0.361805, -0.131432), (0.376721, 0.328757, 0.0), (0.262865, 0.425326, 0.0), (0.116411, 0.32876, -0.358282), (0.241986, 0.251151, -0.358282), (0.223605, 0.361806, -0.262864), (0.241986, 0.251151, -0.358282), (0.344095, 0.262868, -0.249998), (0.223605, 0.361806, -0.262864), (0.223605, 0.361806, -0.262864), (0.344095, 0.262868, -0.249998), (0.319097, 0.361805, -0.131432), (0.344095, 0.262868, -0.249998), (0.415525, 0.251149, -0.119427), (0.319097, 0.361805, -0.131432), (0.319097, 0.361805, -0.131432), (0.415525, 0.251149, -0.119427), (0.376721, 0.328757, 0.0), (0.415525, 0.251149, -0.119427), (0.447213, 0.223608, 0.0), (0.376721, 0.328757, 0.0), (0.478313, 0.125575, 0.073809), (0.415525, 0.251149, 0.119427), (0.447213, 0.223608, 0.0), (0.475529, 0.0, 0.154506), (0.430902, 0.138198, 0.212661), (0.478313, 0.125575, 0.073809), (0.430349, -0.125575, 0.221429), (0.40451, 0.0, 0.293891), (0.475529, 0.0, 0.154506), (0.478313, 0.125575, 0.073809), (0.430902, 0.138198, 0.212661), (0.415525, 0.251149, 0.119427), (0.430902, 0.138198, 0.212661), (0.344095, 0.262868, 0.249998), (0.415525, 0.251149, 0.119427), (0.475529, 0.0, 0.154506), (0.40451, 0.0, 0.293891), (0.430902, 0.138198, 0.212661), (0.40451, 0.0, 0.293891), (0.33541, 0.138199, 0.344095), (0.430902, 0.138198, 0.212661), (0.430902, 0.138198, 0.212661), (0.33541, 0.138199, 0.344095), (0.344095, 0.262868, 0.249998), (0.33541, 0.138199, 0.344095), (0.241986, 0.251151, 0.358282), (0.344095, 0.262868, 0.249998), (0.430349, -0.125575, 0.221429), (0.343579, -0.125576, 0.340858), (0.40451, 0.0, 0.293891), (0.343579, -0.125576, 0.340858), (0.293893, -0.0, 0.404508), (0.40451, 0.0, 0.293891), (0.40451, 0.0, 0.293891), (0.293893, -0.0, 0.404508), (0.33541, 0.138199, 0.344095), (0.293893, -0.0, 0.404508), (0.218003, 0.125576, 0.432094), (0.33541, 0.138199, 0.344095), (0.33541, 0.138199, 0.344095), (0.218003, 0.125576, 0.432094), (0.241986, 0.251151, 0.358282), (0.218003, 0.125576, 0.432094), (0.138194, 0.22361, 0.425325), (0.241986, 0.251151, 0.358282), (0.077608, 0.125576, 0.477711), (0.01482, 0.251151, 0.432092), (0.138194, 0.22361, 0.425325), (-0.0, 0.0, 0.5), (-0.069099, 0.138199, 0.475528), (0.077608, 0.125576, 0.477711), (-0.077608, -0.125576, 0.477711), (-0.154508, -0.0, 0.475528), (-0.0, 0.0, 0.5), (0.077608, 0.125576, 0.477711), (-0.069099, 0.138199, 0.475528), (0.01482, 0.251151, 0.432092), (-0.069099, 0.138199, 0.475528), (-0.131434, 0.262869, 0.404506), (0.01482, 0.251151, 0.432092), (-0.0, 0.0, 0.5), (-0.154508, -0.0, 0.475528), (-0.069099, 0.138199, 0.475528), (-0.154508, -0.0, 0.475528), (-0.223608, 0.138199, 0.425324), (-0.069099, 0.138199, 0.475528), (-0.069099, 0.138199, 0.475528), (-0.223608, 0.138199, 0.425324), (-0.131434, 0.262869, 0.404506), (-0.223608, 0.138199, 0.425324), (-0.26597, 0.251151, 0.340856), (-0.131434, 0.262869, 0.404506), (-0.077608, -0.125576, 0.477711), (-0.218003, -0.125576, 0.432094), (-0.154508, -0.0, 0.475528), (-0.218003, -0.125576, 0.432094), (-0.293893, -0.0, 0.404508), (-0.154508, -0.0, 0.475528), (-0.154508, -0.0, 0.475528), (-0.293893, -0.0, 0.404508), (-0.223608, 0.138199, 0.425324), (-0.293893, -0.0, 0.404508), (-0.343579, 0.125576, 0.340858), (-0.223608, 0.138199, 0.425324), (-0.223608, 0.138199, 0.425324), (-0.343579, 0.125576, 0.340858), (-0.26597, 0.251151, 0.340856), (-0.343579, 0.125576, 0.340858), (-0.361804, 0.22361, 0.262863), (-0.26597, 0.251151, 0.340856), (-0.430349, 0.125575, 0.221429), (-0.406365, 0.25115, 0.147619), (-0.361804, 0.22361, 0.262863), (-0.475529, 0.0, 0.154506), (-0.473607, 0.138198, 0.081229), (-0.430349, 0.125575, 0.221429), (-0.478313, -0.125575, 0.073809), (-0.5, 0.0, -0.0), (-0.475529, 0.0, 0.154506), (-0.430349, 0.125575, 0.221429), (-0.473607, 0.138198, 0.081229), (-0.406365, 0.25115, 0.147619), (-0.473607, 0.138198, 0.081229), (-0.425324, 0.262868, 0.0), (-0.406365, 0.25115, 0.147619), (-0.475529, 0.0, 0.154506), (-0.5, 0.0, -0.0), (-0.473607, 0.138198, 0.081229), (-0.5, 0.0, -0.0), (-0.473606, 0.138198, -0.081229), (-0.473607, 0.138198, 0.081229), (-0.473607, 0.138198, 0.081229), (-0.473606, 0.138198, -0.081229), (-0.425324, 0.262868, 0.0), (-0.473606, 0.138198, -0.081229), (-0.406365, 0.25115, -0.147619), (-0.425324, 0.262868, 0.0), (-0.478313, -0.125575, 0.073809), (-0.478313, -0.125575, -0.073809), (-0.5, 0.0, -0.0), (-0.478313, -0.125575, -0.073809), (-0.475529, -0.0, -0.154506), (-0.5, 0.0, -0.0), (-0.5, 0.0, -0.0), (-0.475529, -0.0, -0.154506), (-0.473606, 0.138198, -0.081229), (-0.475529, -0.0, -0.154506), (-0.430349, 0.125575, -0.221429), (-0.473606, 0.138198, -0.081229), (-0.473606, 0.138198, -0.081229), (-0.430349, 0.125575, -0.221429), (-0.406365, 0.25115, -0.147619), (-0.430349, 0.125575, -0.221429), (-0.361804, 0.22361, -0.262863), (-0.406365, 0.25115, -0.147619), (-0.343579, 0.125576, -0.340858), (-0.26597, 0.251151, -0.340856), (-0.361804, 0.22361, -0.262863), (-0.293893, 0.0, -0.404508), (-0.223608, 0.138198, -0.425324), (-0.343579, 0.125576, -0.340858), (-0.218003, -0.125576, -0.432094), (-0.154509, -0.0, -0.475528), (-0.293893, 0.0, -0.404508), (-0.343579, 0.125576, -0.340858), (-0.223608, 0.138198, -0.425324), (-0.26597, 0.251151, -0.340856), (-0.223608, 0.138198, -0.425324), (-0.131434, 0.262869, -0.404506), (-0.26597, 0.251151, -0.340856), (-0.293893, 0.0, -0.404508), (-0.154509, -0.0, -0.475528), (-0.223608, 0.138198, -0.425324), (-0.154509, -0.0, -0.475528), (-0.0691, 0.138198, -0.475528), (-0.223608, 0.138198, -0.425324), (-0.223608, 0.138198, -0.425324), (-0.0691, 0.138198, -0.475528), (-0.131434, 0.262869, -0.404506), (-0.0691, 0.138198, -0.475528), (0.01482, 0.251151, -0.432092), (-0.131434, 0.262869, -0.404506), (-0.218003, -0.125576, -0.432094), (-0.077608, -0.125576, -0.477711), (-0.154509, -0.0, -0.475528), (-0.077608, -0.125576, -0.477711), (-0.0, -0.0, -0.5), (-0.154509, -0.0, -0.475528), (-0.154509, -0.0, -0.475528), (-0.0, -0.0, -0.5), (-0.0691, 0.138198, -0.475528), (-0.0, -0.0, -0.5), (0.077608, 0.125576, -0.477711), (-0.0691, 0.138198, -0.475528), (-0.0691, 0.138198, -0.475528), (0.077608, 0.125576, -0.477711), (0.01482, 0.251151, -0.432092), (0.077608, 0.125576, -0.477711), (0.138194, 0.22361, -0.425325), (0.01482, 0.251151, -0.432092), (0.218003, 0.125576, -0.432094), (0.241986, 0.251151, -0.358282), (0.138194, 0.22361, -0.425325), (0.293893, 0.0, -0.404508), (0.33541, 0.138198, -0.344095), (0.218003, 0.125576, -0.432094), (0.343579, -0.125576, -0.340858), (0.404509, -1e-06, -0.293891), (0.293893, 0.0, -0.404508), (0.218003, 0.125576, -0.432094), (0.33541, 0.138198, -0.344095), (0.241986, 0.251151, -0.358282), (0.33541, 0.138198, -0.344095), (0.344095, 0.262868, -0.249998), (0.241986, 0.251151, -0.358282), (0.293893, 0.0, -0.404508), (0.404509, -1e-06, -0.293891), (0.33541, 0.138198, -0.344095), (0.404509, -1e-06, -0.293891), (0.430902, 0.138197, -0.212662), (0.33541, 0.138198, -0.344095), (0.33541, 0.138198, -0.344095), (0.430902, 0.138197, -0.212662), (0.344095, 0.262868, -0.249998), (0.430902, 0.138197, -0.212662), (0.415525, 0.251149, -0.119427), (0.344095, 0.262868, -0.249998), (0.343579, -0.125576, -0.340858), (0.430349, -0.125575, -0.221429), (0.404509, -1e-06, -0.293891), (0.430349, -0.125575, -0.221429), (0.475529, -0.0, -0.154506), (0.404509, -1e-06, -0.293891), (0.404509, -1e-06, -0.293891), (0.475529, -0.0, -0.154506), (0.430902, 0.138197, -0.212662), (0.475529, -0.0, -0.154506), (0.478313, 0.125575, -0.073809), (0.430902, 0.138197, -0.212662), (0.430902, 0.138197, -0.212662), (0.478313, 0.125575, -0.073809), (0.415525, 0.251149, -0.119427), (0.478313, 0.125575, -0.073809), (0.447213, 0.223608, 0.0), (0.415525, 0.251149, -0.119427), (0.218003, 0.125576, 0.432094), (0.077608, 0.125576, 0.477711), (0.138194, 0.22361, 0.425325), (0.293893, -0.0, 0.404508), (0.154509, -0.0, 0.475528), (0.218003, 0.125576, 0.432094), (0.343579, -0.125576, 0.340858), (0.223608, -0.138199, 0.425324), (0.293893, -0.0, 0.404508), (0.218003, 0.125576, 0.432094), (0.154509, -0.0, 0.475528), (0.077608, 0.125576, 0.477711), (0.154509, -0.0, 0.475528), (-0.0, 0.0, 0.5), (0.077608, 0.125576, 0.477711), (0.293893, -0.0, 0.404508), (0.223608, -0.138199, 0.425324), (0.154509, -0.0, 0.475528), (0.223608, -0.138199, 0.425324), (0.0691, -0.138199, 0.475527), (0.154509, -0.0, 0.475528), (0.154509, -0.0, 0.475528), (0.0691, -0.138199, 0.475527), (-0.0, 0.0, 0.5), (0.0691, -0.138199, 0.475527), (-0.077608, -0.125576, 0.477711), (-0.0, 0.0, 0.5), (0.343579, -0.125576, 0.340858), (0.26597, -0.251151, 0.340856), (0.223608, -0.138199, 0.425324), (0.26597, -0.251151, 0.340856), (0.131434, -0.262869, 0.404506), (0.223608, -0.138199, 0.425324), (0.223608, -0.138199, 0.425324), (0.131434, -0.262869, 0.404506), (0.0691, -0.138199, 0.475527), (0.131434, -0.262869, 0.404506), (-0.01482, -0.251151, 0.432092), (0.0691, -0.138199, 0.475527), (0.0691, -0.138199, 0.475527), (-0.01482, -0.251151, 0.432092), (-0.077608, -0.125576, 0.477711), (-0.01482, -0.251151, 0.432092), (-0.138194, -0.22361, 0.425325), (-0.077608, -0.125576, 0.477711), (-0.343579, 0.125576, 0.340858), (-0.430349, 0.125575, 0.221429), (-0.361804, 0.22361, 0.262863), (-0.293893, -0.0, 0.404508), (-0.404509, -0.0, 0.293892), (-0.343579, 0.125576, 0.340858), (-0.218003, -0.125576, 0.432094), (-0.335409, -0.138199, 0.344095), (-0.293893, -0.0, 0.404508), (-0.343579, 0.125576, 0.340858), (-0.404509, -0.0, 0.293892), (-0.430349, 0.125575, 0.221429), (-0.404509, -0.0, 0.293892), (-0.475529, 0.0, 0.154506), (-0.430349, 0.125575, 0.221429), (-0.293893, -0.0, 0.404508), (-0.335409, -0.138199, 0.344095), (-0.404509, -0.0, 0.293892), (-0.335409, -0.138199, 0.344095), (-0.430902, -0.138198, 0.212662), (-0.404509, -0.0, 0.293892), (-0.404509, -0.0, 0.293892), (-0.430902, -0.138198, 0.212662), (-0.475529, 0.0, 0.154506), (-0.430902, -0.138198, 0.212662), (-0.478313, -0.125575, 0.073809), (-0.475529, 0.0, 0.154506), (-0.218003, -0.125576, 0.432094), (-0.241986, -0.251151, 0.358282), (-0.335409, -0.138199, 0.344095), (-0.241986, -0.251151, 0.358282), (-0.344095, -0.262868, 0.249998), (-0.335409, -0.138199, 0.344095), (-0.335409, -0.138199, 0.344095), (-0.344095, -0.262868, 0.249998), (-0.430902, -0.138198, 0.212662), (-0.344095, -0.262868, 0.249998), (-0.415525, -0.251149, 0.119427), (-0.430902, -0.138198, 0.212662), (-0.430902, -0.138198, 0.212662), (-0.415525, -0.251149, 0.119427), (-0.478313, -0.125575, 0.073809), (-0.415525, -0.251149, 0.119427), (-0.447213, -0.223608, 0.0), (-0.478313, -0.125575, 0.073809), (-0.430349, 0.125575, -0.221429), (-0.343579, 0.125576, -0.340858), (-0.361804, 0.22361, -0.262863), (-0.475529, -0.0, -0.154506), (-0.404509, 0.0, -0.293892), (-0.430349, 0.125575, -0.221429), (-0.478313, -0.125575, -0.073809), (-0.430902, -0.138198, -0.212662), (-0.475529, -0.0, -0.154506), (-0.430349, 0.125575, -0.221429), (-0.404509, 0.0, -0.293892), (-0.343579, 0.125576, -0.340858), (-0.404509, 0.0, -0.293892), (-0.293893, 0.0, -0.404508), (-0.343579, 0.125576, -0.340858), (-0.475529, -0.0, -0.154506), (-0.430902, -0.138198, -0.212662), (-0.404509, 0.0, -0.293892), (-0.430902, -0.138198, -0.212662), (-0.33541, -0.138199, -0.344095), (-0.404509, 0.0, -0.293892), (-0.404509, 0.0, -0.293892), (-0.33541, -0.138199, -0.344095), (-0.293893, 0.0, -0.404508), (-0.33541, -0.138199, -0.344095), (-0.218003, -0.125576, -0.432094), (-0.293893, 0.0, -0.404508), (-0.478313, -0.125575, -0.073809), (-0.415525, -0.251149, -0.119427), (-0.430902, -0.138198, -0.212662), (-0.415525, -0.251149, -0.119427), (-0.344095, -0.262868, -0.249998), (-0.430902, -0.138198, -0.212662), (-0.430902, -0.138198, -0.212662), (-0.344095, -0.262868, -0.249998), (-0.33541, -0.138199, -0.344095), (-0.344095, -0.262868, -0.249998), (-0.241986, -0.251151, -0.358282), (-0.33541, -0.138199, -0.344095), (-0.33541, -0.138199, -0.344095), (-0.241986, -0.251151, -0.358282), (-0.218003, -0.125576, -0.432094), (-0.241986, -0.251151, -0.358282), (-0.138194, -0.22361, -0.425325), (-0.218003, -0.125576, -0.432094), (0.077608, 0.125576, -0.477711), (0.218003, 0.125576, -0.432094), (0.138194, 0.22361, -0.425325), (-0.0, -0.0, -0.5), (0.154509, 0.0, -0.475528), (0.077608, 0.125576, -0.477711), (-0.077608, -0.125576, -0.477711), (0.0691, -0.138199, -0.475527), (-0.0, -0.0, -0.5), (0.077608, 0.125576, -0.477711), (0.154509, 0.0, -0.475528), (0.218003, 0.125576, -0.432094), (0.154509, 0.0, -0.475528), (0.293893, 0.0, -0.404508), (0.218003, 0.125576, -0.432094), (-0.0, -0.0, -0.5), (0.0691, -0.138199, -0.475527), (0.154509, 0.0, -0.475528), (0.0691, -0.138199, -0.475527), (0.223608, -0.138199, -0.425324), (0.154509, 0.0, -0.475528), (0.154509, 0.0, -0.475528), (0.223608, -0.138199, -0.425324), (0.293893, 0.0, -0.404508), (0.223608, -0.138199, -0.425324), (0.343579, -0.125576, -0.340858), (0.293893, 0.0, -0.404508), (-0.077608, -0.125576, -0.477711), (-0.01482, -0.251151, -0.432092), (0.0691, -0.138199, -0.475527), (-0.01482, -0.251151, -0.432092), (0.131434, -0.262869, -0.404506), (0.0691, -0.138199, -0.475527), (0.0691, -0.138199, -0.475527), (0.131434, -0.262869, -0.404506), (0.223608, -0.138199, -0.425324), (0.131434, -0.262869, -0.404506), (0.26597, -0.251151, -0.340856), (0.223608, -0.138199, -0.425324), (0.223608, -0.138199, -0.425324), (0.26597, -0.251151, -0.340856), (0.343579, -0.125576, -0.340858), (0.26597, -0.251151, -0.340856), (0.361804, -0.22361, -0.262863), (0.343579, -0.125576, -0.340858), (0.478313, 0.125575, -0.073809), (0.478313, 0.125575, 0.073809), (0.447213, 0.223608, 0.0), (0.475529, -0.0, -0.154506), (0.5, 0.0, 0.0), (0.478313, 0.125575, -0.073809), (0.430349, -0.125575, -0.221429), (0.473607, -0.138198, -0.081229), (0.475529, -0.0, -0.154506), (0.478313, 0.125575, -0.073809), (0.5, 0.0, 0.0), (0.478313, 0.125575, 0.073809), (0.5, 0.0, 0.0), (0.475529, 0.0, 0.154506), (0.478313, 0.125575, 0.073809), (0.475529, -0.0, -0.154506), (0.473607, -0.138198, -0.081229), (0.5, 0.0, 0.0), (0.473607, -0.138198, -0.081229), (0.473607, -0.138198, 0.081229), (0.5, 0.0, 0.0), (0.5, 0.0, 0.0), (0.473607, -0.138198, 0.081229), (0.475529, 0.0, 0.154506), (0.473607, -0.138198, 0.081229), (0.430349, -0.125575, 0.221429), (0.475529, 0.0, 0.154506), (0.430349, -0.125575, -0.221429), (0.406365, -0.25115, -0.147619), (0.473607, -0.138198, -0.081229), (0.406365, -0.25115, -0.147619), (0.425324, -0.262868, 0.0), (0.473607, -0.138198, -0.081229), (0.473607, -0.138198, -0.081229), (0.425324, -0.262868, 0.0), (0.473607, -0.138198, 0.081229), (0.425324, -0.262868, 0.0), (0.406365, -0.25115, 0.147619), (0.473607, -0.138198, 0.081229), (0.473607, -0.138198, 0.081229), (0.406365, -0.25115, 0.147619), (0.430349, -0.125575, 0.221429), (0.406365, -0.25115, 0.147619), (0.361804, -0.22361, 0.262863), (0.430349, -0.125575, 0.221429), (0.304773, -0.328759, 0.221428), (0.26597, -0.251151, 0.340856), (0.361804, -0.22361, 0.262863), (0.212661, -0.425327, 0.154506), (0.180902, -0.361806, 0.29389), (0.304773, -0.328759, 0.221428), (0.10159, -0.483975, 0.073809), (0.069098, -0.447215, 0.212661), (0.212661, -0.425327, 0.154506), (0.304773, -0.328759, 0.221428), (0.180902, -0.361806, 0.29389), (0.26597, -0.251151, 0.340856), (0.180902, -0.361806, 0.29389), (0.131434, -0.262869, 0.404506), (0.26597, -0.251151, 0.340856), (0.212661, -0.425327, 0.154506), (0.069098, -0.447215, 0.212661), (0.180902, -0.361806, 0.29389), (0.069098, -0.447215, 0.212661), (0.026395, -0.361805, 0.344093), (0.180902, -0.361806, 0.29389), (0.180902, -0.361806, 0.29389), (0.026395, -0.361805, 0.344093), (0.131434, -0.262869, 0.404506), (0.026395, -0.361805, 0.344093), (-0.01482, -0.251151, 0.432092), (0.131434, -0.262869, 0.404506), (0.10159, -0.483975, 0.073809), (-0.038803, -0.483975, 0.119426), (0.069098, -0.447215, 0.212661), (-0.038803, -0.483975, 0.119426), (-0.081228, -0.425327, 0.249998), (0.069098, -0.447215, 0.212661), (0.069098, -0.447215, 0.212661), (-0.081228, -0.425327, 0.249998), (0.026395, -0.361805, 0.344093), (-0.081228, -0.425327, 0.249998), (-0.116411, -0.32876, 0.358282), (0.026395, -0.361805, 0.344093), (0.026395, -0.361805, 0.344093), (-0.116411, -0.32876, 0.358282), (-0.01482, -0.251151, 0.432092), (-0.116411, -0.32876, 0.358282), (-0.138194, -0.22361, 0.425325), (-0.01482, -0.251151, 0.432092), (-0.116411, -0.32876, 0.358282), (-0.241986, -0.251151, 0.358282), (-0.138194, -0.22361, 0.425325), (-0.081228, -0.425327, 0.249998), (-0.223605, -0.361806, 0.262864), (-0.116411, -0.32876, 0.358282), (-0.038803, -0.483975, 0.119426), (-0.180901, -0.447214, 0.131431), (-0.081228, -0.425327, 0.249998), (-0.116411, -0.32876, 0.358282), (-0.223605, -0.361806, 0.262864), (-0.241986, -0.251151, 0.358282), (-0.223605, -0.361806, 0.262864), (-0.344095, -0.262868, 0.249998), (-0.241986, -0.251151, 0.358282), (-0.081228, -0.425327, 0.249998), (-0.180901, -0.447214, 0.131431), (-0.223605, -0.361806, 0.262864), (-0.180901, -0.447214, 0.131431), (-0.319097, -0.361805, 0.131431), (-0.223605, -0.361806, 0.262864), (-0.223605, -0.361806, 0.262864), (-0.319097, -0.361805, 0.131431), (-0.344095, -0.262868, 0.249998), (-0.319097, -0.361805, 0.131431), (-0.415525, -0.251149, 0.119427), (-0.344095, -0.262868, 0.249998), (-0.038803, -0.483975, 0.119426), (-0.125573, -0.483974, 0.0), (-0.180901, -0.447214, 0.131431), (-0.125573, -0.483974, 0.0), (-0.262865, -0.425326, 0.0), (-0.180901, -0.447214, 0.131431), (-0.180901, -0.447214, 0.131431), (-0.262865, -0.425326, 0.0), (-0.319097, -0.361805, 0.131431), (-0.262865, -0.425326, 0.0), (-0.376721, -0.328757, 0.0), (-0.319097, -0.361805, 0.131431), (-0.319097, -0.361805, 0.131431), (-0.376721, -0.328757, 0.0), (-0.415525, -0.251149, 0.119427), (-0.376721, -0.328757, 0.0), (-0.447213, -0.223608, 0.0), (-0.415525, -0.251149, 0.119427), (-0.376721, -0.328757, 0.0), (-0.415525, -0.251149, -0.119427), (-0.447213, -0.223608, 0.0), (-0.262865, -0.425326, 0.0), (-0.319097, -0.361805, -0.131432), (-0.376721, -0.328757, 0.0), (-0.125573, -0.483974, 0.0), (-0.180901, -0.447214, -0.131432), (-0.262865, -0.425326, 0.0), (-0.376721, -0.328757, 0.0), (-0.319097, -0.361805, -0.131432), (-0.415525, -0.251149, -0.119427), (-0.319097, -0.361805, -0.131432), (-0.344095, -0.262868, -0.249998), (-0.415525, -0.251149, -0.119427), (-0.262865, -0.425326, 0.0), (-0.180901, -0.447214, -0.131432), (-0.319097, -0.361805, -0.131432), (-0.180901, -0.447214, -0.131432), (-0.223605, -0.361805, -0.262864), (-0.319097, -0.361805, -0.131432), (-0.319097, -0.361805, -0.131432), (-0.223605, -0.361805, -0.262864), (-0.344095, -0.262868, -0.249998), (-0.223605, -0.361805, -0.262864), (-0.241986, -0.251151, -0.358282), (-0.344095, -0.262868, -0.249998), (-0.125573, -0.483974, 0.0), (-0.038803, -0.483975, -0.119426), (-0.180901, -0.447214, -0.131432), (-0.038803, -0.483975, -0.119426), (-0.081228, -0.425327, -0.249998), (-0.180901, -0.447214, -0.131432), (-0.180901, -0.447214, -0.131432), (-0.081228, -0.425327, -0.249998), (-0.223605, -0.361805, -0.262864), (-0.081228, -0.425327, -0.249998), (-0.116411, -0.32876, -0.358282), (-0.223605, -0.361805, -0.262864), (-0.223605, -0.361805, -0.262864), (-0.116411, -0.32876, -0.358282), (-0.241986, -0.251151, -0.358282), (-0.116411, -0.32876, -0.358282), (-0.138194, -0.22361, -0.425325), (-0.241986, -0.251151, -0.358282), (0.406365, -0.25115, 0.147619), (0.304773, -0.328759, 0.221428), (0.361804, -0.22361, 0.262863), (0.425324, -0.262868, 0.0), (0.335409, -0.361805, 0.081228), (0.406365, -0.25115, 0.147619), (0.406365, -0.25115, -0.147619), (0.335409, -0.361805, -0.081229), (0.425324, -0.262868, 0.0), (0.406365, -0.25115, 0.147619), (0.335409, -0.361805, 0.081228), (0.304773, -0.328759, 0.221428), (0.335409, -0.361805, 0.081228), (0.212661, -0.425327, 0.154506), (0.304773, -0.328759, 0.221428), (0.425324, -0.262868, 0.0), (0.335409, -0.361805, -0.081229), (0.335409, -0.361805, 0.081228), (0.335409, -0.361805, -0.081229), (0.223605, -0.447214, -0.0), (0.335409, -0.361805, 0.081228), (0.335409, -0.361805, 0.081228), (0.223605, -0.447214, -0.0), (0.212661, -0.425327, 0.154506), (0.223605, -0.447214, -0.0), (0.10159, -0.483975, 0.073809), (0.212661, -0.425327, 0.154506), (0.406365, -0.25115, -0.147619), (0.304773, -0.328759, -0.221428), (0.335409, -0.361805, -0.081229), (0.304773, -0.328759, -0.221428), (0.212661, -0.425327, -0.154506), (0.335409, -0.361805, -0.081229), (0.335409, -0.361805, -0.081229), (0.212661, -0.425327, -0.154506), (0.223605, -0.447214, -0.0), (0.212661, -0.425327, -0.154506), (0.10159, -0.483975, -0.073809), (0.223605, -0.447214, -0.0), (0.223605, -0.447214, -0.0), (0.10159, -0.483975, -0.073809), (0.10159, -0.483975, 0.073809), (0.10159, -0.483975, -0.073809), (-0.0, -0.5, 0.0), (0.10159, -0.483975, 0.073809), (-0.116411, -0.32876, -0.358282), (-0.01482, -0.251151, -0.432092), (-0.138194, -0.22361, -0.425325), (-0.081228, -0.425327, -0.249998), (0.026395, -0.361806, -0.344093), (-0.116411, -0.32876, -0.358282), (-0.038803, -0.483975, -0.119426), (0.069099, -0.447215, -0.21266), (-0.081228, -0.425327, -0.249998), (-0.116411, -0.32876, -0.358282), (0.026395, -0.361806, -0.344093), (-0.01482, -0.251151, -0.432092), (0.026395, -0.361806, -0.344093), (0.131434, -0.262869, -0.404506), (-0.01482, -0.251151, -0.432092), (-0.081228, -0.425327, -0.249998), (0.069099, -0.447215, -0.21266), (0.026395, -0.361806, -0.344093), (0.069099, -0.447215, -0.21266), (0.180902, -0.361805, -0.29389), (0.026395, -0.361806, -0.344093), (0.026395, -0.361806, -0.344093), (0.180902, -0.361805, -0.29389), (0.131434, -0.262869, -0.404506), (0.180902, -0.361805, -0.29389), (0.26597, -0.251151, -0.340856), (0.131434, -0.262869, -0.404506), (-0.038803, -0.483975, -0.119426), (0.10159, -0.483975, -0.073809), (0.069099, -0.447215, -0.21266), (0.10159, -0.483975, -0.073809), (0.212661, -0.425327, -0.154506), (0.069099, -0.447215, -0.21266), (0.069099, -0.447215, -0.21266), (0.212661, -0.425327, -0.154506), (0.180902, -0.361805, -0.29389), (0.212661, -0.425327, -0.154506), (0.304773, -0.328759, -0.221428), (0.180902, -0.361805, -0.29389), (0.180902, -0.361805, -0.29389), (0.304773, -0.328759, -0.221428), (0.26597, -0.251151, -0.340856), (0.304773, -0.328759, -0.221428), (0.361804, -0.22361, -0.262863), (0.26597, -0.251151, -0.340856))
    # vertices = (
    #     (0,0,0), (1,1,0), (0,1,0)
    # )
    norms = generate_normals(vertices)
    # print(norms)
    # from ursina import *
    # app = Ursina()
    # m = Mesh(vertices=vertices)
    # m.generate_normals()
    # e = Entity(model=m)
    # # print(e.normals)
    # if e.normals:
    #     verts = list()
    #     for i in range(len(e.vertices)):
    #         verts.append(e.vertices[i])
    #         verts.append(Vec3(e.vertices[i][0], e.vertices[i][1], e.vertices[i][2])
    #             + Vec3(e.normals[i][0], e.normals[i][1], e.normals[i][2])*2)
    #
    #     lines=Entity(model=Mesh(verts, mode='line'))
    # # e.shader = 'shader_normals'
    # EditorCamera()
    # app.run()

import numpy as np
from scipy.spatial import cKDTree


def deduplicate_particleblock(particle_block, exclusion_radius=1):
    kdt = cKDTree(particle_block.positions.data)
    clusters = kdt.query_ball_point(particle_block.positions.data, exclusion_radius, workers=-1)
    clusters_sorted = sorted(clusters, key=len, reverse=True)

    duplicates = []
    visited = []
    for cluster in clusters_sorted:
        if len(cluster) == 1:
            break
        duplicates_in_cluster = [el for el in cluster[1:] if el not in visited]
        duplicates.extend(duplicates_in_cluster)
        visited.append(cluster[0])

    duplicates = np.array(sorted(list(set(duplicates)))).astype(int)
    mask = np.ones(particle_block.n, dtype=bool)
    mask[duplicates] = False

    return particle_block[mask].copy()


def deduplicate_peeper(peeper, exclusion_radius=1):
    from ..peeper import Peeper
    p = Peeper()
    for pb in peeper.particles:
        p.append(deduplicate_particleblock(pb, exclusion_radius))
    return p

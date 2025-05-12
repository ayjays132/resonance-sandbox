# resonance_sandbox/energy.py

import numpy as np
from typing import Union, Dict

# Try to import NetworkX for graph‐based metrics; optional dependency
try:
    import networkx as nx
    _HAS_NETWORKX = True
except ImportError:
    _HAS_NETWORKX = False

from .manifold import ContextualManifold

def compute_energy(
    manifold: ContextualManifold,
    full: bool = False
) -> Union[float, Dict[str, float]]:
    """
    Compute the “energy” of a ContextualManifold, plus optional advanced diagnostics.

    Parameters
    ----------
    manifold : ContextualManifold
        The manifold whose adjacency matrix encodes semantic–physical resonance.
    full : bool, default False
        If False, returns only the Frobenius norm (classical energy).
        If True, returns a dict with detailed metrics.

    Returns
    -------
    float or dict
        If full=False: returns Frobenius norm of the adjacency matrix.
        If full=True: returns a dict with keys:
          - frobenius_norm: float
          - spectral_radius: float                # largest absolute eigenvalue
          - avg_edge_weight: float                # mean of upper‐triangle weights
          - var_edge_weight: float                # variance of upper‐triangle weights
          - node_count: int                       # number of nodes
          - edge_count: int                       # number of edges
    """
    # Convert adjacency to NumPy array
    W = np.array(manifold.adj, dtype=float)

    # Core energy: Frobenius norm
    fro_norm = float(np.linalg.norm(W))

    if not full:
        return fro_norm

    # Prepare detailed diagnostics
    metrics: Dict[str, float] = {'frobenius_norm': fro_norm}

    # Spectral radius (largest absolute eigenvalue)
    try:
        eigs = np.linalg.eigvals(W)
        metrics['spectral_radius'] = float(np.max(np.abs(eigs)))
    except Exception:
        metrics['spectral_radius'] = float('nan')

    # Upper‐triangle edge weights (excludes diagonal)
    triu_i, triu_j = np.triu_indices_from(W, k=1)
    edge_weights = W[triu_i, triu_j]
    if edge_weights.size > 0:
        metrics['avg_edge_weight'] = float(np.mean(edge_weights))
        metrics['var_edge_weight'] = float(np.var(edge_weights))
    else:
        metrics['avg_edge_weight'] = 0.0
        metrics['var_edge_weight'] = 0.0

    # Graph‐based metrics if NetworkX is installed
    if _HAS_NETWORKX:
        try:
            G = nx.from_numpy_array(W)
            metrics['node_count'] = G.number_of_nodes()
            metrics['edge_count'] = G.number_of_edges()
        except Exception:
            metrics['node_count'] = 0
            metrics['edge_count'] = 0
    else:
        # Fallback counts from raw matrix
        n = W.shape[0]
        metrics['node_count'] = n
        # count nonzero off-diagonal entries as edges
        metrics['edge_count'] = int(np.count_nonzero(edge_weights))

    return metrics

import numpy as np
import networkx as nx
import json
from typing import List, Optional, Union, Dict, Any

class ContextualManifold:
    """
    Represents a dynamic contextual manifold as an adjacency matrix.
    Nodes correspond to dimension indices; edges encode relational intensity.
    Supports deformations, energy computations, spectral analysis, and serialization.
    """

    def __init__(
        self,
        size: int,
        adj: Optional[Union[List[List[float]], np.ndarray]] = None
    ):
        """
        Initialize the manifold.

        Args:
            size: Number of nodes (dimensions).
            adj: Optional adjacency matrix (list-of-lists or numpy array).
        """
        if adj is None:
            # Zero-initialize adjacency
            self.adj: List[List[float]] = [[0.0] * size for _ in range(size)]
        else:
            arr = np.array(adj, dtype=float)
            if arr.shape != (size, size):
                raise ValueError(f"Adjacency must be {size}x{size}, got {arr.shape}")
            self.adj = arr.tolist()

    def apply_deformation(
        self,
        delta_matrix: Union[List[List[float]], np.ndarray]
    ) -> None:
        """
        Apply a symmetric deformation to the adjacency matrix.

        Args:
            delta_matrix: Deformation matrix; only symmetric component is applied.
        """
        mat = np.array(delta_matrix, dtype=float)
        size = len(self.adj)
        if mat.shape != (size, size):
            raise ValueError(f"Delta must be {size}x{size}, got {mat.shape}")
        # Symmetrically apply
        for i in range(size):
            for j in range(size):
                sym = (mat[i, j] + mat[j, i]) / 2.0
                self.adj[i][j] += sym

    def energy(self) -> float:
        """
        Compute the Frobenius energy of the adjacency matrix.
        Returns the sum of squares of all entries.
        """
        arr = np.array(self.adj, dtype=float)
        return float(np.sum(arr * arr))

    def spectral_diagnostics(self) -> Dict[str, Any]:
        """
        Compute advanced diagnostics including spectral radius,
        node/edge counts, and average degree.
        """
        arr = np.array(self.adj, dtype=float)
        energy = float(np.sum(arr * arr))
        eigs = np.linalg.eigvals(arr)
        radius = float(np.max(np.abs(eigs)))
        G = nx.from_numpy_array(arr)
        node_count = G.number_of_nodes()
        edge_count = G.number_of_edges()
        avg_degree = float(sum(dict(G.degree()).values()) / node_count) if node_count else 0.0
        return {
            "energy": energy,
            "spectral_radius": radius,
            "node_count": node_count,
            "edge_count": edge_count,
            "avg_degree": avg_degree
        }

    def to_json(self) -> str:
        """
        Serialize the manifold to a JSON string.
        """
        return json.dumps({
            "size": len(self.adj),
            "adj": self.adj
        })

    @classmethod
    def from_json(
        cls,
        data: Union[str, Dict[str, Any]]
    ) -> 'ContextualManifold':
        """
        Deserialize from JSON string or dict.
        """
        obj = json.loads(data) if isinstance(data, str) else data
        return cls(obj["size"], adj=obj["adj"])

    def __repr__(self) -> str:
        size = len(self.adj)
        return f"ContextualManifold(size={size}, energy={self.energy():.4f})"

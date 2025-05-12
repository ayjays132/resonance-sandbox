import numpy as np
import json
from typing import Optional, Union, List, Dict, Any

class RelationalFlux:
    """
    Represents an abstract semantic 'flux' vector in high-dimensional space.
    Core methods:
      - perturb: return new flux with Gaussian noise
      - normalize: unit-length flux
      - magnitude: L2 norm
      - scale: scalar multiplication
      - add: vector addition
      - to_json/from_json: serialization
      - random: various random-generation distributions
    """

    def __init__(
        self,
        dim: int,
        vector: Optional[Union[List[float], np.ndarray]] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize a RelationalFlux.

        Args:
            dim: dimensionality of the flux vector.
            vector: initial values (list or ndarray). If None, sampled standard normal.
            seed: random seed for reproducibility.
        """
        self.dim = dim
        self._rng = np.random.default_rng(seed)
        if vector is None:
            self.vector = self._rng.standard_normal(dim)
        else:
            arr = np.array(vector, dtype=float)
            if arr.shape != (dim,):
                raise ValueError(f"Vector shape must be ({dim},), got {arr.shape}")
            self.vector = arr.copy()

    def perturb(self, noise_scale: float = 1e-3, seed: Optional[int] = None) -> 'RelationalFlux':
        """
        Return a new RelationalFlux with added Gaussian noise.

        Args:
            noise_scale: standard deviation of noise.
            seed: optional seed for noise generator.
        """
        rng = np.random.default_rng(seed) if seed is not None else self._rng
        noise = rng.standard_normal(self.dim) * noise_scale
        return RelationalFlux(self.dim, self.vector + noise)

    def magnitude(self) -> float:
        """Return the L2 norm of the flux."""
        return float(np.linalg.norm(self.vector))

    def normalize(self) -> 'RelationalFlux':
        """Return a unit‐length version of this flux."""
        mag = self.magnitude()
        if mag == 0:
            return RelationalFlux(self.dim, np.zeros(self.dim))
        return RelationalFlux(self.dim, self.vector / mag)

    def scale(self, factor: float) -> 'RelationalFlux':
        """Return a new flux scaled by the given factor."""
        return RelationalFlux(self.dim, self.vector * factor)

    def add(self, other: 'RelationalFlux') -> 'RelationalFlux':
        """Elementwise addition with another flux (must match dims)."""
        if not isinstance(other, RelationalFlux) or other.dim != self.dim:
            raise ValueError("Can only add RelationalFlux of same dimension")
        return RelationalFlux(self.dim, self.vector + other.vector)

    def to_json(self) -> str:
        """Serialize this flux to a JSON string."""
        data: Dict[str, Any] = {"dim": self.dim, "vector": self.vector.tolist()}
        return json.dumps(data)

    @classmethod
    def from_json(cls, data: Union[str, Dict[str, Any]]) -> 'RelationalFlux':
        """
        Deserialize from JSON.
        Accepts either a JSON string or a loaded dict.
        """
        obj = json.loads(data) if isinstance(data, str) else data
        return cls(obj["dim"], obj.get("vector"))

    @classmethod
    def random(
        cls,
        dim: int,
        distribution: str = "normal",
        **kwargs: Any
    ) -> 'RelationalFlux':
        """
        Generate a random flux.

        Args:
            dim: dimensionality.
            distribution: "normal" | "uniform" | "bernoulli".
            kwargs: extra params (seed, p for bernoulli).
        """
        seed = kwargs.get("seed", None)
        rng = np.random.default_rng(seed)
        if distribution == "normal":
            vec = rng.standard_normal(dim)
        elif distribution == "uniform":
            vec = rng.uniform(-1, 1, size=dim)
        elif distribution == "bernoulli":
            p = kwargs.get("p", 0.5)
            vec = rng.binomial(1, p, size=dim).astype(float)
        else:
            raise ValueError(f"Unsupported distribution: {distribution}")
        return cls(dim, vec, seed=seed)

    def __repr__(self):
        return f"RelationalFlux(dim={self.dim}, magnitude={self.magnitude():.4f})"

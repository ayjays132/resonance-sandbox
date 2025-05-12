# resonance_sandbox/operator.py

import numpy as np
import logging
import json
from typing import Optional, Union
from .flux import RelationalFlux
from .manifold import ContextualManifold

logger = logging.getLogger(__name__)

class ResonanceOperator:
    """
    Operator mapping a RelationalFlux to deformations in a ContextualManifold.
    Guarantees a non-zero deformation even for edge‐case flux vectors.
    """

    def __init__(
        self,
        flux_dim: int,
        manifold_size: int,
        damping: float = 1.0,           # Strong default to ensure visible change
        seed: Optional[int] = None
    ):
        """
        Args:
            flux_dim: dimensionality of the input vector
            manifold_size: number of nodes in the manifold
            damping: scalar multiplier on the deformation strength
            seed: optional RNG seed for reproducibility
        """
        self.flux_dim = flux_dim
        self.manifold_size = manifold_size
        self.damping = damping
        self.rng = np.random.default_rng(seed)

        # Random weight matrix plus slight identity bias
        W_rand = self.rng.standard_normal((manifold_size, flux_dim))
        identity_bias = np.eye(manifold_size, flux_dim) * 0.01
        self.W = W_rand + identity_bias

    def operate(
        self,
        flux: RelationalFlux,
        manifold: ContextualManifold
    ) -> ContextualManifold:
        """
        Apply semantic flux → manifold deformation.
        Always injects a tiny epsilon so at least one entry changes.
        """
        # 1) Compute raw projection
        delta = self.W @ flux.vector

        # 2) Guarantee non-zero effect
        epsilon = 1e-6
        delta = delta + epsilon

        # 3) Form outer-product deformation
        delta_mat = np.outer(delta, delta) * self.damping

        # 4) Apply and return
        manifold.apply_deformation(delta_mat)
        return manifold

    def compute_delta(self, flux: RelationalFlux) -> np.ndarray:
        """Return the raw projection vector (with epsilon)."""
        delta = self.W @ flux.vector
        return delta + 1e-6

    def to_json(self) -> str:
        """Serialize internal state to JSON."""
        state = {
            "flux_dim": self.flux_dim,
            "manifold_size": self.manifold_size,
            "damping": self.damping,
            "W": self.W.tolist()
        }
        return json.dumps(state)

    @classmethod
    def from_json(cls, data: Union[str, dict]) -> 'ResonanceOperator':
        """Deserialize from JSON."""
        obj = json.loads(data) if isinstance(data, str) else data
        op = cls(obj["flux_dim"], obj["manifold_size"], damping=obj["damping"])
        op.W = np.array(obj["W"], dtype=float)
        return op

    def __repr__(self) -> str:
        return (
            f"ResonanceOperator(flux_dim={self.flux_dim}, "
            f"manifold_size={self.manifold_size}, damping={self.damping})"
        )

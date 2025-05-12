# resonance_sandbox/meta_learning.py

import numpy as np
import logging
from typing import Optional, Tuple, List, Dict, Any

from .flux import RelationalFlux
from .manifold import ContextualManifold
from .operator import ResonanceOperator
from .energy import compute_energy

logger = logging.getLogger(__name__)


def random_search(
    flux_dim: int,
    manifold_size: int,
    base_operator: Optional[ResonanceOperator] = None,
    iterations: int = 50,
    pop_size: int = 20,
    noise_scale: float = 0.1,
    null_penalty: float = 10.0,
    return_history: bool = False
) -> Tuple[ResonanceOperator, float, List[Dict[str, Any]]]:
    """
    Perform a random search over ResonanceOperator weights to optimize semantic–
    physical coupling while minimizing null‐flux violations.

    Parameters
    ----------
    flux_dim : int
        Dimensionality of the RelationalFlux vectors.
    manifold_size : int
        Number of nodes (size of adjacency matrix).
    base_operator : Optional[ResonanceOperator]
        Starting operator. If None, a new one is created.
    iterations : int
        Number of optimization generations.
    pop_size : int
        Number of candidate operators per generation.
    noise_scale : float
        Standard deviation for Gaussian weight perturbations.
    null_penalty : float
        Penalty multiplier for null‐flux violations.
    return_history : bool
        If True, returns a history of generation metrics.

    Returns
    -------
    best_operator : ResonanceOperator
        The operator instance achieving the highest fitness.
    best_fitness : float
        The corresponding fitness score.
    history : List[Dict[str, Any]]
        If return_history, list of dicts with per-generation metrics.
    """
    # Initialize operator
    op = base_operator or ResonanceOperator(flux_dim, manifold_size)
    best_op = op
    best_fitness = float('-inf')
    history: List[Dict[str, Any]] = []

    for gen in range(1, iterations + 1):
        gen_best: Dict[str, Any] = {
            "generation": gen,
            "fitness": float('-inf'),
            "positive": 0.0,
            "null": float('inf'),
            "energy": 0.0
        }

        for _ in range(pop_size):
            # Create a candidate by perturbing weights
            candidate = ResonanceOperator(flux_dim, manifold_size, damping=op.damping)
            candidate.W = op.W + np.random.randn(manifold_size, flux_dim) * noise_scale

            # Null-flux test: expect zero deformation
            zero_flux = RelationalFlux(flux_dim, vector=[0.0] * flux_dim)
            m_null = ContextualManifold(manifold_size)
            candidate.operate(zero_flux, m_null)
            null_violation = sum(abs(v) for row in m_null.adj for v in row)

            # Positive-flux test: expect substantial deformation
            flux = RelationalFlux.random(flux_dim, distribution="normal")
            m_pos = ContextualManifold(manifold_size)
            candidate.operate(flux, m_pos)
            positive_delta = sum(abs(m_pos.adj[i][j]) 
                                 for i in range(manifold_size) 
                                 for j in range(manifold_size))

            # Compute energy impact
            energy = compute_energy(m_pos)

            # Fitness: reward positive effect, penalize null violations
            fitness = positive_delta - null_penalty * null_violation

            # Update generation best
            if fitness > gen_best["fitness"]:
                gen_best.update({
                    "fitness": fitness,
                    "positive": positive_delta,
                    "null": null_violation,
                    "energy": energy,
                    "operator": candidate
                })

        # Promote to global best if improved
        if gen_best["fitness"] > best_fitness:
            best_fitness = gen_best["fitness"]
            best_op = gen_best["operator"]

        logger.info(
            f"Gen {gen}/{iterations} | fitness={gen_best['fitness']:.4f} "
            f"(+Δ={gen_best['positive']:.4f}, null={gen_best['null']:.4f}, energy={gen_best['energy']:.4f})"
        )

        if return_history:
            history.append({
                "generation": gen,
                "fitness": gen_best["fitness"],
                "positive": gen_best["positive"],
                "null": gen_best["null"],
                "energy": gen_best["energy"]
            })

    # Return history if requested
    if return_history:
        return best_op, best_fitness, history
    return best_op, best_fitness, []

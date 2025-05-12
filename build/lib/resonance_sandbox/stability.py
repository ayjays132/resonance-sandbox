# resonance_sandbox/stability.py

from typing import Dict, Any, List, Optional, Tuple
from .flux import RelationalFlux
from .manifold import ContextualManifold
from .operator import ResonanceOperator

def stability_test(
    flux_dim: int = 16,
    manifold_size: int = 8,
    scales: Optional[List[float]] = None,
    full_metrics: bool = False
) -> Dict[float, Any]:
    """
    If full_metrics=False (default), returns:
        { scale: (E_before, E_after) }
    matching the original tests’ expectations.

    If full_metrics=True, returns:
        { scale: {
            "E_before": float,
            "E_after": float,
            "delta": float,
            "stable": bool
          } }
    for richer diagnostics.
    """
    if scales is None:
        scales = [1e-4, 1e-3, 1e-2]

    results: Dict[float, Any] = {}
    op = ResonanceOperator(flux_dim, manifold_size)

    for scale in scales:
        # Baseline manifold with zero flux
        base = ContextualManifold(manifold_size)
        E0 = base.energy()

        # Perturb with a small random flux
        flux = RelationalFlux(flux_dim)
        perturbed = op.operate(flux.perturb(scale), base)
        E1 = perturbed.energy()

        if not full_metrics:
            # classic tuple form for test_stability
            results[scale] = (E0, E1)
        else:
            # richer form if requested
            results[scale] = {
                "E_before": E0,
                "E_after": E1,
                "delta": E1 - E0,
                "stable": (E1 >= E0)
            }

    return results

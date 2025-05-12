# resonance_sandbox/human_interface.py

import logging
from typing import Any, Dict, List, Optional, Union

import numpy as np

from .flux import RelationalFlux
from .manifold import ContextualManifold
from .operator import ResonanceOperator
from .energy import compute_energy

# configure module‐level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def text_to_flux(
    text: str,
    dim: int,
    normalize: bool = True,
    distribution: str = "uniform",
    **dist_kwargs: Any
) -> RelationalFlux:
    """
    Convert an input string into a RelationalFlux vector.

    Each character is hashed into one of `dim` buckets, then optionally
    normalized or resampled from a distribution.

    Args:
        text: The input text to encode.
        dim: Dimensionality of the resulting flux.
        normalize: If True, returns unit‐length flux.
        distribution: If specified, resample flux via RelationalFlux.random().
        dist_kwargs: Passed to RelationalFlux.random (e.g., seed, p).

    Returns:
        A RelationalFlux instance representing the text.
    """
    vec = np.zeros(dim, dtype=float)
    for i, c in enumerate(text):
        idx = ord(c) % dim
        vec[idx] += 1.0

    flux = RelationalFlux(dim, vector=vec)
    logger.debug(f"Raw text flux (pre‐normalize): magnitude={flux.magnitude():.4f}")

    if normalize:
        flux = flux.normalize()
        logger.debug(f"Normalized flux: magnitude={flux.magnitude():.4f}")

    if distribution:
        # blend original with random noise from chosen distribution
        random_flux = RelationalFlux.random(dim, distribution, **dist_kwargs)
        flux = flux.add(random_flux.scale(0.1)).normalize()
        logger.debug(f"Blended with {distribution} noise, new magnitude={flux.magnitude():.4f}")

    return flux


def human_test(
    text: str,
    flux_dim: int = 16,
    manifold_size: int = 8,
    damping: float = 1e-3,
    snippet_size: int = 3,
    include_metrics: bool = False
) -> Dict[str, Any]:
    """
    Run a single human‐oriented test: convert text to flux, operate the resonance,
    and return a small adjacency snippet plus optional energy metrics.

    Args:
        text: Input text prompt.
        flux_dim: Dimensionality for RelationalFlux.
        manifold_size: Size of the ContextualManifold (number of nodes).
        damping: Damping factor for ResonanceOperator.
        snippet_size: Number of top‐left rows/cols to include in snippet.
        include_metrics: If True, include full energy diagnostics.

    Returns:
        A dict with keys:
          - "snippet": List[List[float]] 3×3 block of the resulting adjacency.
          - "flux": List[float] full flux vector.
          - "metrics": Dict[str, float] if include_metrics, else None.
    """
    logger.info(f"Human test on text: '{text}'")
    # 1) Encode text → flux
    flux = text_to_flux(text, flux_dim)
    logger.info(f"Flux vector magnitude: {flux.magnitude():.4f}")

    # 2) Initialize operator & manifold
    op = ResonanceOperator(flux_dim, manifold_size, damping=damping)
    manifold = ContextualManifold(manifold_size)

    # 3) Apply resonance
    op.operate(flux, manifold)
    logger.info("Applied ResonanceOperator to manifold.")

    # 4) Capture adjacency snippet
    snippet = [
        [round(manifold.adj[i][j], 6) for j in range(snippet_size)]
        for i in range(snippet_size)
    ]

    result: Dict[str, Any] = {
        "snippet": snippet,
        "flux": flux.vector.tolist(),
        "metrics": None
    }

    # 5) Optionally compute full energy metrics
    if include_metrics:
        energy_info = compute_energy(manifold, full=True)
        result["metrics"] = energy_info
        logger.info(f"Computed full energy metrics: {energy_info}")

    return result


import pytest
from resonance_sandbox.stability import stability_test
from resonance_sandbox.energy import compute_energy
from resonance_sandbox.operator import ResonanceOperator
from resonance_sandbox.flux import RelationalFlux
from resonance_sandbox.manifold import ContextualManifold

def test_stability():
    results = stability_test(flux_dim=4, manifold_size=4, scales=[1e-4,1e-3])
    for E0,E1 in results.values():
        assert E1 >= E0

def test_energy():
    m = ContextualManifold(3)
    op = ResonanceOperator(3,3)
    flux = RelationalFlux(3)
    before = compute_energy(m)
    op.operate(flux, m)
    after = compute_energy(m)
    assert after >= before

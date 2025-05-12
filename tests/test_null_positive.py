
import pytest
from resonance_sandbox.flux import RelationalFlux
from resonance_sandbox.manifold import ContextualManifold
from resonance_sandbox.operator import ResonanceOperator

def test_null():
    op = ResonanceOperator(4,4)
    zero = RelationalFlux(4, vector=[0.0]*4)
    m = ContextualManifold(4)
    before = [row[:] for row in m.adj]
    op.operate(zero, m)
    assert all(abs(m.adj[i][j] - before[i][j]) < 1e-8 for i in range(4) for j in range(4))

def test_positive():
    op = ResonanceOperator(4,4)
    flux = RelationalFlux(4)
    m = ContextualManifold(4)
    before = [row[:] for row in m.adj]
    op.operate(flux, m)
    assert any(abs(m.adj[i][j] - before[i][j]) > 0 for i in range(4) for j in range(4))

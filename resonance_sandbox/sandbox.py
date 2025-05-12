#!/usr/bin/env python3
"""
resonance_sandbox/sandbox.py

Command-line interface for the Resonance Sandbox package.
Supports null-test, positive-test, stability-test, energy-monitor, and meta-learn commands.
"""
import argparse
import yaml
from .flux import RelationalFlux
from .manifold import ContextualManifold
from .operator import ResonanceOperator
from .stability import stability_test
from .energy import compute_energy
from .meta_learning import random_search
from .human_interface import human_test
import sys

def null_test(op, flux_dim, manifold_size):
    zero_flux = RelationalFlux(flux_dim, vector=[0.0]*flux_dim)
    m = ContextualManifold(manifold_size)
    before = [row[:] for row in m.adj]
    op.operate(zero_flux, m)
    max_delta = max(abs(m.adj[i][j] - before[i][j]) for i in range(manifold_size) for j in range(manifold_size))
    print("Null Test Δ-max:", max_delta)


def positive_test(op, flux_dim, manifold_size):
    flux = RelationalFlux(flux_dim)
    m = ContextualManifold(manifold_size)
    before = [row[:] for row in m.adj]
    op.operate(flux, m)
    max_delta = max(abs(m.adj[i][j] - before[i][j]) for i in range(manifold_size) for j in range(manifold_size))
    print("Positive Test Δ-max:", max_delta)


def stability_cmd(op, flux_dim, manifold_size):
    results = stability_test(flux_dim, manifold_size)
    for scale, (E0, E1) in results.items():
        print(f"Noise {scale}: E0={E0}, E1={E1}")


def energy_monitor(op, flux_dim, manifold_size):
    flux = RelationalFlux(flux_dim)
    m = ContextualManifold(manifold_size)
    op.operate(flux, m)
    e = compute_energy(m)
    print("Energy:", e)


def meta_learn_cmd(flux_dim, manifold_size):
    op = ResonanceOperator(flux_dim, manifold_size)
    best_op, best_score, _ = random_search(flux_dim, manifold_size, base_operator=op)
    print("Meta-learned best fitness:", best_score)


def human_cmd(op, text, flux_dim, manifold_size):
    result = human_test(text, flux_dim, manifold_size, include_metrics=True)
    print("Human Test snippet:", result['snippet'])
    print("Metrics:", result['metrics'])


def main():
    parser = argparse.ArgumentParser(description="Resonance Sandbox CLI v0.2.0")
    parser.add_argument("--config", "-c", default="config/config.yaml", help="Path to config file.")
    parser.add_argument("--null-test", action="store_true")
    parser.add_argument("--positive-test", action="store_true")
    parser.add_argument("--stability-test", action="store_true")
    parser.add_argument("--energy-monitor", action="store_true")
    parser.add_argument("--meta-learn", action="store_true")
    parser.add_argument("--human-test", type=str, metavar="TEXT")
    args = parser.parse_args()

    try:
        cfg = yaml.safe_load(open(args.config))
    except Exception as e:
        print("Failed to load config:", e, file=sys.stderr)
        sys.exit(1)

    flux_dim = cfg.get('flux_dim', 16)
    manifold_size = cfg.get('manifold_size', 8)
    damping = cfg.get('damping', 1.0)
    op = ResonanceOperator(flux_dim, manifold_size, damping=damping)

    if args.null_test:
        null_test(op, flux_dim, manifold_size)
    if args.positive_test:
        positive_test(op, flux_dim, manifold_size)
    if args.stability_test:
        stability_cmd(op, flux_dim, manifold_size)
    if args.energy_monitor:
        energy_monitor(op, flux_dim, manifold_size)
    if args.meta_learn:
        meta_learn_cmd(flux_dim, manifold_size)
    if args.human_test:
        human_cmd(op, args.human_test, flux_dim, manifold_size)

if __name__ == "__main__":
    main()

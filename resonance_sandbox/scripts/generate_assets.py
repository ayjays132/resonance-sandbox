#!/usr/bin/env python3
"""
generate_assets.py

Advanced asset generation for Resonance Sandbox:
- Reads a YAML config file for parameters.
- Generates semantic–physical "resonance" samples.
- Outputs adjacency matrices (CSV), graph visualizations (PNG), and metadata (JSON).
- Supports CLI overrides and progress reporting.
"""

import os
import sys
import json
import yaml
import argparse
import logging
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

from resonance_sandbox.flux import RelationalFlux
from resonance_sandbox.manifold import ContextualManifold
from resonance_sandbox.operator import ResonanceOperator

def setup_logger(log_file=None):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def save_metadata(meta, out_path):
    with open(out_path, 'w') as f:
        json.dump(meta, f, indent=2)

def generate_assets(cfg_path, logger):
    cfg = load_config(cfg_path)
    flux_dim      = cfg['flux_dim']
    manifold_size = cfg['manifold_size']
    damping       = cfg['damping']
    count         = cfg['generate_assets']['count']
    out_dir       = cfg['generate_assets']['output_dir']
    os.makedirs(out_dir, exist_ok=True)

    logger.info(f"Generating {count} assets to '{out_dir}'…")
    metadata_list = []

    for i in tqdm(range(count), desc="Assets"):
        flux     = RelationalFlux(flux_dim)
        manifold = ContextualManifold(manifold_size)
        op       = ResonanceOperator(flux_dim, manifold_size, damping=damping)
        op.operate(flux, manifold)
        adj = np.array(manifold.adj)

        # 1) Save adjacency CSV
        csv_path = os.path.join(out_dir, f"adj_{i:03d}.csv")
        np.savetxt(csv_path, adj, delimiter=",")
        logger.debug(f"Saved CSV: {csv_path}")

        # 2) Build and save graph PNG
        G = nx.from_numpy_array(adj)
        plt.figure(figsize=(6,6))
        pos = nx.circular_layout(G)
        weights = [abs(G[u][v]['weight']) for u,v in G.edges()]
        nx.draw(
            G, pos,
            with_labels=True,
            node_size=300,
            edge_color=weights,
            edge_cmap=plt.cm.viridis,
            width=[max(0.5, w*5) for w in weights]
        )
        plt.title(f"Resonance Graph #{i:03d}")
        png_path = os.path.join(out_dir, f"graph_{i:03d}.png")
        plt.savefig(png_path, bbox_inches='tight')
        plt.close()
        logger.debug(f"Saved PNG: {png_path}")

        # 3) Collect per‐asset metadata
        metadata_list.append({
            "index": i,
            "flux_vector": flux.vector.tolist(),
            "damping": damping,
            "max_edge_weight": float(adj.max()),
            "min_edge_weight": float(adj.min()),
            "csv_path": csv_path,
            "png_path": png_path
        })

    # Save metadata JSON
    meta_path = os.path.join(out_dir, "metadata.json")
    save_metadata(metadata_list, meta_path)
    logger.info(f"Saved metadata JSON: {meta_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate Resonance Sandbox assets (CSV + PNG + JSON)."
    )
    parser.add_argument(
        "--config", "-c", default="config/config.yaml",
        help="Path to YAML config file."
    )
    parser.add_argument(
        "--log", "-l", default=None,
        help="Optional logfile to record debug messages."
    )
    args = parser.parse_args()

    logger = setup_logger(args.log)
    try:
        generate_assets(args.config, logger)
        logger.info("Asset generation completed successfully.")
    except Exception as e:
        logger.error(f"Asset generation failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

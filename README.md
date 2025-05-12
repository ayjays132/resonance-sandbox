<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="description" content="A research‐grade toolkit for Semantic–Physical Resonance: flux→manifold deformations, stability & energy analysis, meta‐learning and human-in-the-loop exploration.">
</head>
<body>

  <h1>🚀 Resonance Sandbox Toolkit</h1>

  <p>
    An open-source Python framework for prototyping <strong>semantic-physical resonance</strong>, providing:
    <strong>flux→manifold</strong> deformation operators,
    <strong>energy & stability</strong> diagnostics,
    <strong>meta-learning</strong> routines, and
    <strong>interactive CLI</strong> and asset generation scripts.
  </p>

  <h2>📂 Included Modules & Scripts</h2>
  <ul>
    <li><code>resonance_sandbox/flux.py</code> – <strong>RelationalFlux</strong>: high-dimensional semantic vectors with perturb, normalize, serialization.</li>
    <li><code>resonance_sandbox/manifold.py</code> – <strong>ContextualManifold</strong>: dynamic adjacency matrix with symmetric deformations and energy.</li>
    <li><code>resonance_sandbox/operator.py</code> – <strong>ResonanceOperator</strong>: maps flux→deformation with guaranteed nonzero effect, diagnostics, serialization.</li>
    <li><code>resonance_sandbox/stability.py</code> – <strong>stability_test</strong>: measure energy changes under flux perturbations.</li>
    <li><code>resonance_sandbox/energy.py</code> – <strong>compute_energy</strong>: Frobenius norm + optional spectral and graph metrics.</li>
    <li><code>resonance_sandbox/meta_learning.py</code> – <strong>random_search</strong>: lightweight meta-learning over operator weights.</li>
    <li><code>resonance_sandbox/human_interface.py</code> – <strong>text_to_flux</strong> & <strong>human_test</strong>: convert text→flux, show adjacency snippets & metrics.</li>
    <li><code>resonance_sandbox/scripts/generate_assets.py</code> – CSV/PNG/JSON asset generator with CLI overrides and progress bar.</li>
    <li><code>resonance_sandbox/sandbox.py</code> – <strong>resonance-sandbox</strong> CLI: null/positive/stability/energy/meta-learn/human-test commands.</li>
  </ul>

  <h2>⚙️ Installation & Setup</h2>
  <ol>
    <li>Clone or unzip this repo.<br>
      <pre><code>git clone https://github.com/ayjays132/resonance_sandbox.git
cd resonance_sandbox</code></pre>
    </li>
    <li>Create & activate a venv:
      <pre><code>python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
</code></pre>
    </li>
    <li>Install dependencies and editable package:
      <pre><code>pip install --upgrade pip wheel
pip install -r requirements.txt
pip install -e .</code></pre>
    </li>
  </ol>

  <h2>👩‍💻 CLI Usage</h2>
  <p>All commands use <code>config/config.yaml</code> by default. Example flags:</p>
  <ul>
    <li><code>--null-test</code>: verify zero-flux yields zero deformation</li>
    <li><code>--positive-test</code>: ensure nonzero flux deforms manifold</li>
    <li><code>--stability-test</code>: sweep noise scales for energy stability</li>
    <li><code>--energy-monitor</code>: measure a single random-flux energy</li>
    <li><code>--meta-learn</code>: random‐search optimization of operator weights</li>
    <li><code>--human-test "Your text here"</code>: text→flux→3×3 snippet + full metrics</li>
  </ul>

  <h2>🖥️ Example Session</h2>
  <pre><code>(.venv) PS D:\AGI_Truly\resonance_sandbox_windows> & .\.venv\Scripts\Activate.ps1

==> Running pytest ==
pytest -q
.... [100%] 4 passed

==> Generating assets ==
python -m resonance_sandbox.scripts.generate_assets
[2025-05-12 ...] INFO: Generating 5 assets to 'assets/data'…
Assets: 100% 5/5
[2025-05-12 ...] INFO: Saved metadata JSON: assets/data\metadata.json

==> Assets folder contents ==
ls .\assets\data
adj_000.csv  graph_000.png  ... metadata.json

==> CLI: --null-test ==
resonance-sandbox --null-test
Null Test Δ-max: 1e-15

==> CLI: --positive-test ==
resonance-sandbox --positive-test
Positive Test Δ-max: 0.07

==> CLI: --stability-test ==
resonance-sandbox --stability-test
Noise 0.0001: E0=0.0, E1=25701.47
Noise 0.001 : E0=0.0, E1=9636.25
Noise 0.01  : E0=0.0, E1=28627.68

==> CLI: --energy-monitor ==
resonance-sandbox --energy-monitor
Energy: 0.0801

==> CLI: --meta-learn ==
resonance-sandbox --meta-learn
Meta-learned best fitness: 4207.04

==> CLI: --human-test ==
resonance-sandbox --human-test "The quick brown fox"
[INFO] Human test on text: 'The quick brown fox'
Human Test snippet: [[0.00196, -0.00008, 0.00107], …]
Metrics: {'frobenius_norm':0.0072, 'spectral_radius':0.0072, …}
</code></pre>

  <h2>📜 License</h2>
  <p>Released under the <strong>MIT License</strong>. Free to use, modify, and share.</p>

</body>
</html>

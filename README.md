# Resonance Sandbox (v0.2.0)

An advanced Python framework to prototype, validate, and meta-learn the **Geometry of Semantic–Physical Resonance**.

## Features

- Core primitives: RelationalFlux, ContextualManifold, ResonanceOperator
- Energy computations and stability auditing
- Simple meta-learning (random search) to tune the operator
- Human-in-the-loop interface for semantic perturbations
- Asset generation scripts producing CSV adjacency matrices and graph images
- CLI commands: --null-test, --positive-test, --stability-test, --energy-monitor, --meta-learn, --human-test

---

## Windows PowerShell Usage

```powershell
# Unzip the archive
Expand-Archive resonance_sandbox_windows.zip -DestinationPath resonance_sandbox_windows
cd resonance_sandbox_windows

# Run setup script to create virtual environment and install dependencies
.\setup.ps1

# Run all tests
.	est.ps1

# Generate assets (CSV and PNG)
.\generate_assets.ps1

# Run CLI examples
.un_cli.ps1

# Build distribution packages
.uild.ps1
```

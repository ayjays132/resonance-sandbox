# tests/conftest.py
import sys, os
# Prepend project root (one level up) to PYTHONPATH so tests can import resonance_sandbox
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

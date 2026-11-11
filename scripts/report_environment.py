#!/usr/bin/env python3
"""Report local package versions without contacting the network."""
from importlib import metadata
import json
import platform
import sys
from pathlib import Path

PKGS = [
    'numpy', 'pandas', 'scipy', 'scikit-learn', 'matplotlib', 'seaborn',
    'openpyxl', 'lxml', 'folium', 'xgboost', 'lightgbm', 'catboost',
    'torch', 'pytabkit', 'statsmodels', 'linearmodels', 'shap',
    'pytorch-tabnet', 'tabpfn', 'tabicl', 'causilo', 'interpret'
]
versions = {}
for package in PKGS:
    try:
        versions[package] = metadata.version(package)
    except metadata.PackageNotFoundError:
        versions[package] = None
report = {
    'python': sys.version,
    'platform': platform.platform(),
    'packages': versions,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
print('\nSave this report with run date, seed, source checksums and hardware details.')

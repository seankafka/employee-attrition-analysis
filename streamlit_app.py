import sys
from pathlib import Path

# Add deployment to path
sys.path.insert(0, str(Path(__file__).parent / "deployment"))

# Run the actual app from deployment
exec(open(Path(__file__).parent / "deployment" / "app.py").read())

import sys, os

# Garante que o Python ache seu app
sys.path.insert(0, os.path.dirname(__file__))

# Importa o Flask app
from app import app as application

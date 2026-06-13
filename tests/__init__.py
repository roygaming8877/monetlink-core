"""
MonetLink Enterprise Automated Testing Suite
Initialization Module
"""
import os

# Force environment to testing so it never overwrites the production database
os.environ["ENVIRONMENT"] = "testing"

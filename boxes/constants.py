"""
Box Selection System - Constants

Centralized configuration for magic numbers and default values.
"""

# Packing algorithm tolerance for floating-point comparisons
PACKING_TOLERANCE = 0.01

# Default pagination settings
DEFAULT_PAGE_SIZE = 50

# API rate limiting
RATE_LIMIT_ANONYMOUS = "100/hour"
RATE_LIMIT_USER = "1000/hour"

# Weight and dimension units
WEIGHT_UNIT = "kg"
DIMENSION_UNIT = "cm"

# Box recommendation priorities
PRIORITY_WEIGHT = "weight"
PRIORITY_COST = "cost"
PRIORITY_VOLUME = "volume"
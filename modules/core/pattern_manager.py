import os
import random
import logging

from state import state
from utils import parse_theta_rho_file

logger = logging.getLogger(__name__)


def is_clear_pattern(file_path):
    """Check if a file path is a clear pattern file."""
    clear_patterns = []
    for table_type in ['dune_weaver', 'dune_weaver_mini', 'dune_weaver_pro']:
        suffix = f'_{table_type.split("_")[-1]}' if table_type != 'dune_weaver' else ''
        clear_patterns.extend([
            f'./patterns/clear_from_out{suffix}.thr',
            f'./patterns/clear_from_in{suffix}.thr'
        ])

    normalized_path = os.path.normpath(file_path)
    normalized_clear_patterns = [os.path.normpath(p) for p in clear_patterns]

    return normalized_path in normalized_clear_patterns


def get_clear_pattern_file(clear_pattern_mode, path=None):
    """Return a .thr file path based on pattern_name and table type."""
    if not clear_pattern_mode or clear_pattern_mode == 'none':
        return

    clear_patterns = {
        'dune_weaver': {
            'clear_from_out': './patterns/clear_from_out.thr',
            'clear_from_in': './patterns/clear_from_in.thr'
        },
        'dune_weaver_mini': {
            'clear_from_out': './patterns/clear_from_out_mini.thr',
            'clear_from_in': './patterns/clear_from_in_mini.thr'
        },
        'dune_weaver_pro': {
            'clear_from_out': './patterns/clear_from_out_pro.thr',
            'clear_from_in': './patterns/clear_from_in_pro.thr'
        }
    }

    table_patterns = clear_patterns.get(state.table_type, clear_patterns['dune_weaver'])

    logger.debug(f"Clear pattern mode: {clear_pattern_mode} for table type: {state.table_type}")

    if clear_pattern_mode == "random":
        return random.choice(list(table_patterns.values()))

    if clear_pattern_mode == 'adaptive':
        if not path:
            logger.warning("No path provided for adaptive clear pattern")
            return random.choice(list(table_patterns.values()))

        coordinates = parse_theta_rho_file(path)
        if not coordinates:
            logger.warning("No valid coordinates found in file for adaptive clear pattern")
            return random.choice(list(table_patterns.values()))

        first_rho = coordinates[0][1]
        return table_patterns['clear_from_out'] if first_rho < 0.5 else table_patterns['clear_from_in']

    if clear_pattern_mode not in table_patterns:
        return False

    return table_patterns[clear_pattern_mode]

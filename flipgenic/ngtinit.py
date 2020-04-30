import logging
import os.path

import ngtpy

from axyn.datastore import get_path

logger = logging.getLogger(__name__)


def get_ngt(name):
    path = get_path(name)
    # Create index if it doesn't exist
    if not os.path.exists(path):
        logger.info('Creating NGT index "%s"', name)
        ngtpy.create(path, dimension=300)

    logger.info('Loading NGT index "%s"', name)
    return ngtpy.Index(path)


statements_index = get_ngt("ngt_statements")
reactions_index = get_ngt("ngt_reactions")

""" Moduel to calculate kde """

import logging
from http import HTTPStatus
from scipy import stats
import numpy as np

LOGGER = logging.getLogger(__name__)


def calculate_kde(lat, lng):
    """ Calculate kde
    lat (float): latitude coordinate
    lng (float): longitude coordinate
    return kde if no errors or response to api if errors
    """
    try:
        values = np.vstack([lat, lng])
        return stats.gaussian_kde(values)
    except BaseException as err:
        LOGGER.error(err)
        return {"code": HTTPStatus.INTERNAL_SERVER_ERROR, "message": err}

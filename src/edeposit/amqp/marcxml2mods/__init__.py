#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml2mods import marcxml2mods

from structures.requests import ConversionRequest
from structures.responses import ConversionResponse


# Functions & classes =========================================================
def _instanceof(instance, cls):
    """
    Check type of `instance` by matching ``.__name__`` with `cls.__name__`.
    """
    return type(instance).__name__ == cls.__name__


# Main function ===============================================================
def reactToAMQPMessage(message, send_back):
    """
    React to given (AMQP) message. `message` is expected to be
    :py:func:`collections.namedtuple` structure from :mod:`.structures` filled
    with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`.structures`.
        send_back (fn reference): Reference to function for responding. This is
                  useful for progress monitoring for example. Function takes
                  one parameter, which may be response structure/namedtuple, or
                  string or whatever would be normally returned.

    Returns:
        object: Response class from :mod:`structures`.

    Raises:
        ValueError: if bad type of `message` structure is given.
    """
    if _instanceof(message, ConversionRequest):
        return ConversionResponse(
            marcxml2mods(
                marc_xml=message.marc_xml,
                uuid=message.uuid,
                url=message.url
            )
        )

    raise ValueError("'%s' is unknown type of request!" % str(type(message)))

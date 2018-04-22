from .exceptions import MissingArgumentError, InvalidTypeArgumentError, \
    NodeAttributeError, ApiActionError, InvalidUssageError, GraphFailed
from .constants import _BlockRunningStatus, _GraphRunningStatus, \
    _GraphPostAction, _GraphPostStatus, _ValidationCode
from .api import _get_obj, _save_graph, _get_access_token
from .base_node import NodeProps, Inputs, OutputItem, Outputs, Params, BaseNode
from .block import Block
from .client import Client
from .file import File
from .graph import Graph
import logging


def set_logging_level(verbose):
    LOG_LEVELS = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG
    }
    logging.basicConfig(level=LOG_LEVELS.get(verbose, 4))

set_logging_level(3)

__all__ = [
    ApiActionError,
    BaseNode,
    Block,
    Client,
    File,
    Graph,
    GraphFailed,
    Inputs,
    InvalidTypeArgumentError,
    InvalidUssageError,
    MissingArgumentError,
    NodeAttributeError,
    NodeProps,
    OutputItem,
    Outputs,
    Params,
    _BlockRunningStatus,
    _GraphPostAction,
    _GraphPostStatus,
    _GraphRunningStatus,
    _ValidationCode,
    _get_access_token,
    _get_obj,
    _save_graph,
    set_logging_level,
]

from robot.api.logger import error
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from .dict import DictKeywords
from .functional import FunctionalKeywords
from .list import ListKeywords
from .set import SetKeywords


@library(scope="GLOBAL", version="0.0.1", doc_format="reST", auto_keywords=True)
class CollectionExtensions(DictKeywords, FunctionalKeywords, ListKeywords, SetKeywords):
    """ """

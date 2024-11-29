from robot.api.logger import error
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from .markers import MarkersKeywords
from .variables import VariablesKeywords


@library(scope="GLOBAL", version="0.0.1", doc_format="reST", auto_keywords=True)
class Fuzz(MarkersKeywords, VariablesKeywords):
    """ """

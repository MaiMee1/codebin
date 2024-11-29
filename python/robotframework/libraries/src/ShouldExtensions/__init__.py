from robot.api.logger import error
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from .type_keywords import TypeKeywords
from .cmp_keywords import CmpKeywords


@library(scope="GLOBAL", version="0.0.1", doc_format="reST", auto_keywords=True)
class ShouldExtensions(TypeKeywords, CmpKeywords):
    """ """

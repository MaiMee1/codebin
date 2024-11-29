from robot.api.deco import library

from .json_keywords import JsonKeywords


@library(scope="GLOBAL", version="0.0.1", doc_format="reST", auto_keywords=True)
class JSONLibraryExtensions(JsonKeywords):
    """ """

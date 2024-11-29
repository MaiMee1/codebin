import json
import os

import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from robot.api.logger import error, info
    
    
from pathlib import Path
import json

from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource


PathLike = str | bytes | os.PathLike[str] | os.PathLike[bytes]


# See function ``is_git_directory`` in https://github.com/git/git/blob/master/setup.c
def is_git_directory(suspect: Path) -> bool:
    head = suspect / 'HEAD'
    refs = suspect / 'refs'
    objects = suspect / 'objects'

    if not head.exists() or not refs.exists or not objects.exists():
        return False
    if not (head.is_symlink() or head.is_file()) or not refs.is_dir() or not objects.is_dir():
        return False
    if not head.read_text().startswith('ref: '):
        return False
    return True

def find_git_repository(fp: PathLike) -> Path:
    """Returns the path to the base repository if found.

    Examples:
    >>> find_git_repository('json_keywords.py').stem
    'core-workspace'
    """
    path = Path(fp).absolute()

    found = False
    while not found:
        if not is_git_directory(path / '.git'):
            if not path == path.parent:
                path = path.parent
            else:
                raise ValueError('git directory not found in ancestry')
        else:
            return path

def get_file_registry(wd: Path, *, encoding = None, default_specification = DRAFT202012) -> Registry:
    def retrieve_from_filesystem(uri: str) -> Resource:
        path = Path(uri)
        if not path.is_absolute():
            # add support for non-canonical relative file URI
            path = wd / path

        contents = json.loads(path.read_text(encoding=encoding))
        return Resource.from_contents(contents, default_specification=default_specification)
    
    return Registry(retrieve=retrieve_from_filesystem)

class JsonKeywords:
    """

    Examples:
    >>> obj = json.loads('{"code":0,"message":"","data":{"trees":[{"name":"A3WY0PQB","label":{"en":{"text":"A3WY0PQB nothing stand report","image_url":""},"th":{"text":"A3WY0PQB หน้ากาก วัง เกม","image_url":""}},"description":"Class audience later activity. Throw minute group even. Service piece onto others industry onto remember seek.","result_field_name":"nmyynyNa","created_at":1732011295,"updated_at":1732011298,"deleted_at":0,"type":"DECISION","parent_tree":"","argument_field_list":null,"field_set":""},{"name":"72yHd03V","label":{"en":{"text":"72yHd03V direction close take","image_url":""},"th":{"text":"72yHd03V บัดนี้ คำถาม โก๋แก่","image_url":""}},"description":"South type perhaps finish. Remember when represent for building building front. Blue prevent head hope avoid. Prevent win bag just less style.","result_field_name":"l_UkFXRW","created_at":1732011295,"updated_at":1732011297,"deleted_at":0,"type":"DECISION","parent_tree":"","argument_field_list":null,"field_set":""},{"name":"AMGLeri3","label":{"en":{"text":"AMGLeri3 research wide lot","image_url":""},"th":{"text":"AMGLeri3 ยูทูบ ยา คนตาย","image_url":""}},"description":"Perhaps choose activity read of mouth spend water. Home do seven hair spring. Research physical play similar realize once recently. Each decision outside election financial trial share goal.","result_field_name":"OA76o_B_","created_at":1732011295,"updated_at":1732011296,"deleted_at":0,"type":"DECISION","parent_tree":"","argument_field_list":null,"field_set":""}],"total":3}}')
    >>> JsonKeywords().validate_json_by_extended_schema_file(obj, 'tests/e2e-api/libraries/src/JsonLibraryExtensions/test-schema.json')
    """
    def validate_json_by_extended_schema_file(
        self, json_object, filepath, encoding=None
    ) -> None:
        """Validate JSON object by a JSON Schema file with extended definitions.

        Fails if json object does not match the schema.
        """
        
        with open(filepath, encoding=encoding) as f:
            schema = json.load(f)

        try:
            # TODO: better path-finding?
            working_directory = find_git_repository(filepath)
            registry = get_file_registry(wd=working_directory, encoding=encoding)
            jsonschema.validate(json_object, {'$ref': filepath}, registry=registry)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Json does not match the schema: {e.schema}")
        except jsonschema.SchemaError as e:
            raise AssertionError(f"Json schema error: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

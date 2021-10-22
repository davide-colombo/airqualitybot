#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: this script defines the classes for parsing file content from different extensions.
#
#################################################
import json
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError


class FileParser(ABC):

    @abstractmethod
    def parse(self, raw_string: str) -> Dict[str, Any]:
        """Abstract method that defines the common interface for parsing raw string from file into Dict[str, Any]."""
        pass


class JSONFileParser(FileParser):
    """JSONFileParser class defines the business rules for parsing JSON file format."""

    def parse(self, raw_string: str) -> Dict[str, Any]:
        """Core method of this every FileParser instance that takes a raw string and parses it.

        If 'raw_string' is empty, SystemExit exception is raised.

        If some error occur while parsing the string, SystemExit exception is raised."""

        if not raw_string:
            raise SystemExit(f"{JSONFileParser.__name__}: cannot parse empty raw string.")

        try:
            parsed = json.loads(raw_string)
        except JSONDecodeError as jerr:
            raise SystemExit(f"{JSONFileParser.__name__}: {str(jerr)}")
        return parsed


class FileParserFactory(builtins.object):
    """This class defines a @staticmethod for creating a FileParser object given the file extension."""


    @staticmethod
    def file_parser_from_file_extension(file_extension: str) -> FileParser:
        """Factory method for creating FileParser objects from file extension.

        Supported file extensions are: [ json ].

        If invalid file extension is passed, SystemExit is raised."""

        if file_extension == 'json':
            return JSONFileParser()
        else:
            raise SystemExit(f"{FileParserFactory.__name__}: unknown parser for file extension '{file_extension}'.")
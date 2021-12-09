######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as cmd
import airquality.filter.filter as flt
import airquality.database.repo.repo as dbrepo
import airquality.types.line.line as linetype


class ServiceInitCommand(cmd.Command):

    def __init__(
            self,
            file_lines: Generator[linetype.LineABC, None, None],
            file_filter: flt.FilterABC,
            db_repo: dbrepo.DatabaseRepoABC,
            log_filename="geonames"
    ):
        super(ServiceInitCommand, self).__init__(log_filename=log_filename)
        self.file_lines = file_lines
        self.file_filter = file_filter
        self.db_repo = db_repo

    @log_decorator.log_decorator()
    def execute(self):
        filtered_lines = self.file_filter.filter(self.file_lines)
        self.db_repo.push(filtered_lines)

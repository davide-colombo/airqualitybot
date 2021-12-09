######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import List
import airquality.command.initsrv.cmd as cmd
import airquality.command.basefact as fact
import airquality.logger.util.decorator as log_decorator
import airquality.file.util.line_parser as lineparser
import airquality.file.line.builder as linebuilder
import airquality.filter.geonames as flt
import airquality.database.conn.adapt as db
import airquality.database.repo.geonames as dbrepo
import airquality.database.util.query as qry
import airquality.file.structured.json as jsonfile
import airquality.file.repo.geonames as filerepo
import airquality.source.file as filesource
import airquality.types.file.type as filetype


class InitServiceCommandFactory(fact.CommandFactory):

    def __init__(
            self, query_file: jsonfile.JSONFile, conn: db.DatabaseAdapter,
            log_filename="log", only_new_places=True, only_patient_poscodes=True, keep_unique_lines=False
    ):
        super(InitServiceCommandFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)
        self.only_new_places = only_new_places
        self.only_patient_poscodes = only_patient_poscodes
        self.keep_unique_lines = keep_unique_lines

    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str) -> List[cmd.ServiceInitCommand]:

        tsv_parser = lineparser.get_line_parser("\t", log_filename=self.log_filename)

        path2filter = f"{os.environ['directory_of_resources']}/{sensor_type}/filter"
        poscode_source = self.craft_poscode_source(path2directory=path2filter, line_parser=tsv_parser)

        path2geonames = f"{os.environ['directory_of_resources']}/{sensor_type}"
        geonames_source = self.craft_geonames_source(path2directory=path2geonames, line_parser=tsv_parser)
        files = geonames_source.get()

        db_repo = self.craft_database_repo()

        commands_to_execute = []
        for file in files:
            file_filter = self.craft_file_filter(file=file, db_repo=db_repo, poscode_source=poscode_source)
            commands_to_execute.append(self.craft_command(file=file, file_filter=file_filter, db_repo=db_repo))

        n = len(commands_to_execute)
        self.log_info(f"{self.__class__.__name__} create {n}/{n} commands to execute")
        return commands_to_execute

    ################################ craft_command() ################################
    @log_decorator.log_decorator()
    def craft_command(
            self, file: filetype.GeonamesFileType, db_repo: dbrepo.GeonamesRepo, file_filter: flt.GeonamesFilter
    ) -> cmd.ServiceInitCommand:

        file_lines = file.lines
        if self.keep_unique_lines:
            file_lines = file.unique_lines()

        command = cmd.ServiceInitCommand(
            file_lines=file_lines, db_repo=db_repo, file_filter=file_filter, log_filename=self.log_filename
        )
        command.set_console_logger(self.console_logger)
        command.set_file_logger(self.file_logger)
        return command

    ################################ craft_poscode_source() ################################
    @log_decorator.log_decorator()
    def craft_poscode_source(self, path2directory: str, line_parser: lineparser.LineParser) -> filesource.PostalcodeFileSource:
        poscode_repo = filerepo.GeonamesFileRepo(path2directory)
        poscode_builder = linebuilder.PostalcodeLineBuilder()
        poscode_source = filesource.PostalcodeFileSource(repo=poscode_repo, parser=line_parser, builder=poscode_builder)
        return poscode_source

    ################################ craft_geonames_source() ################################
    @log_decorator.log_decorator()
    def craft_geonames_source(self, path2directory: str, line_parser: lineparser.LineParser) -> filesource.GeonamesFileSource:
        geonames_repo = filerepo.GeonamesFileRepo(path2directory)
        geonames_builder = linebuilder.GeonamesLineBuilder(log_filename=self.log_filename)
        geonames_source = filesource.GeonamesFileSource(repo=geonames_repo, parser=line_parser, builder=geonames_builder)
        return geonames_source

    ################################ craft_file_filter() ################################
    @log_decorator.log_decorator()
    def craft_file_filter(self, file: filetype.GeonamesFileType, db_repo, poscode_source) -> flt.GeonamesFilter:
        file_filter = flt.GeonamesFilter(log_filename=self.log_filename)
        if self.only_new_places:
            places = db_repo.with_country_code(file.country_code).lookup_place_names()
            file_filter.with_database_place_names(places)
        if self.only_patient_poscodes:
            poscode_file = poscode_source.retrieve(file.filename)
            file_filter.with_postalcodes(poscode_file.postal_codes)
        file_filter.set_file_logger(self.file_logger)
        file_filter.set_console_logger(self.console_logger)
        return file_filter

    ################################ craft_database_repo() ################################
    @log_decorator.log_decorator()
    def craft_database_repo(self) -> dbrepo.GeonamesRepo:
        query_builder = qry.QueryBuilder(self.query_file)
        db_repo = dbrepo.GeonamesRepo(db_adapter=self.database_conn, query_builder=query_builder)
        return db_repo

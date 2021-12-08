######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.basefact as fact
import airquality.command.update.cmd as cmd
import airquality.file.util.text_parser as fp
import airquality.file.structured.json as file
import airquality.api.fetchwrp as apiwrp
import airquality.api.url.public as url
import airquality.api.resp.info.purpleair as resp
import airquality.database.repo.geolocation as dbrepo
import airquality.database.util.query as qry
import airquality.database.conn.adapt as db
import airquality.filter.geolocation as flt


################################ get_update_command_factory_cls ################################
def get_update_factory_cls(sensor_type: str) -> fact.CommandFactory.__class__:
    function_name = get_update_factory_cls.__name__
    valid_types = ["purpleair"]

    if sensor_type == 'purpleair':
        return PurpleairUpdateFactory
    else:
        raise SystemExit(f"{function_name}: bad type => VALID TYPES: [{'|'.join(t for t in valid_types)}]")


################################ PURPLEAIR UPDATE COMMAND FACTORY ################################
class PurpleairUpdateFactory(fact.CommandFactory):

    def __init__(self, query_file: file.JSONFile, conn: db.DatabaseAdapter, log_filename="log"):
        super(PurpleairUpdateFactory, self).__init__(query_file=query_file, conn=conn, log_filename=log_filename)

    ################################ create_command ################################
    @log_decorator.log_decorator()
    def create_command(self, sensor_type: str):

        response_builder, url_builder, fetch_wrapper = self.get_api_side_objects()

        repo = self.get_database_side_objects(sensor_type=sensor_type)
        response_filter = flt.GeoFilter(repo=repo)
        response_filter.set_file_logger(self.file_logger)
        response_filter.set_console_logger(self.console_logger)

        command = cmd.UpdateCommand(
            ub=url_builder,
            fw=fetch_wrapper,
            repo=repo,
            arb=response_builder,
            rf=response_filter,
            log_filename=self.log_filename
        )
        command.set_file_logger(self.file_logger)
        command.set_console_logger(self.console_logger)

        return command

    ################################ get_api_side_objects ################################
    @log_decorator.log_decorator()
    def get_api_side_objects(self):
        response_builder = resp.PurpleairAPIRespBuilder()
        url_builder = url.PurpleairURLBuilder(url_template=os.environ['purpleair_url'])

        fetch_wrapper = apiwrp.FetchWrapper(
            resp_parser=fp.JSONParser(log_filename=self.log_filename),
            log_filename=self.log_filename
        )
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)
        return response_builder, url_builder, fetch_wrapper

    ################################ get_database_side_objects ################################
    @log_decorator.log_decorator()
    def get_database_side_objects(self, sensor_type: str):
        query_builder = qry.QueryBuilder(query_file=self.query_file)
        repo = dbrepo.SensorGeoRepository(db_adapter=self.database_conn, query_builder=query_builder, sensor_type=sensor_type)
        return repo

######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.fetchcmd.fetch as command
import airquality.command.cmdconf as comm_const
import airquality.command.basecmdsetup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.api.fetchwrp as apiwrp

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.url.atmurl as atmurl
import airquality.api.url.thnkurl as thnkurl

import airquality.api.resp.atmresp as atmresp
import airquality.api.resp.thnkresp as thnkresp

import airquality.database.op.ins.mbmeasins as ins
import airquality.database.op.sel.mobilesel as mobsel
import airquality.database.op.sel.stationsel as stsel

import airquality.database.util.query as qry
import airquality.looper.datelooper as looper

import airquality.to_delete.db2api.param as par_adapt


class AtmotubeFetchSetup(setup.CommandSetup):

    def __init__(self, log_filename="atmotube"):
        super(AtmotubeFetchSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        api_file_obj = setup.load_file(
            file_path=comm_const.API_FILE_PATH, path_to_object=[sensor_type], log_filename=self.log_filename
        )

        # API parameters from file
        address = api_file_obj.address
        resp_fmt = api_file_obj.format
        options = api_file_obj.options

        # url_builder = atmurl.AtmotubeURLBuilder(address=address, key=, mac=)

        # FetchWrapper
        fetch_wrapper = apiwrp.FetchWrapper(
            resp_builder=atmresp.AtmoAPIRespBuilder(),
            resp_parser=fp.get_text_parser(file_ext=resp_fmt, log_filename=self.log_filename),
            log_filename=self.log_filename
        )
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_connection = setup.open_database_connection(connection_string=os.environ['DBCONN'],
                                                             log_filename=self.log_filename)

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)

        # QueryBuilder
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.MobileMeasureInsertWrapper(conn=database_connection, builder=query_builder, log_filename=self.log_filename)
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_wrapper = mobsel.MobileSelectWrapper(
            conn=database_connection,
            builder=query_builder,
            sensor_type=sensor_type,
            log_filename=self.log_filename
        )

        # Date looper class
        date_looper_class = looper.get_date_looper_class(sensor_type=sensor_type)

        # Build command object
        cmd = command.FetchCommand(fetch_wrapper=fetch_wrapper,
                                   insert_wrapper=insert_wrapper,
                                   date_looper_class=date_looper_class)
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)
        return cmd


class ThingspeakFetchSetup(setup.CommandSetup):

    def __init__(self, log_filename="atmotube"):
        super(ThingspeakFetchSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        address, url_param = setup.get_api_parameters(sensor_type=sensor_type, log_filename=self.log_filename)

        # Check if 'format' argument is not missing from 'url_param'
        if 'format' not in url_param:
            raise SystemExit(f"{ThingspeakFetchSetup.__name__}: bad 'api.json' file structure => missing key='format'")

        # Take the API resp format
        api_resp_fmt = url_param['format']

        # Setup API-side objects
        api_resp_parser = fp.get_text_parser(file_ext=api_resp_fmt, log_filename=self.log_filename)
        api_data_extractor = extr.ThnkRespBuilder(log_filename=self.log_filename)
        url_builder = url.ThingspeakURLBuilder(address=address, url_param=url_param, log_filename=self.log_filename)

        # FetchWrapper
        fetch_wrapper = setup.get_fetch_wrapper(url_builder=url_builder,
                                                response_parser=api_resp_parser,
                                                response_builder=api_data_extractor,
                                                log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_connection = setup.open_database_connection(connection_string=os.environ['DBCONN'],
                                                             log_filename=self.log_filename)

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)

        # QueryBuilder
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.FetchStationInsertWrapper(
            conn=database_connection,
            query_builder=query_builder,
            sensor_measure_rec=rec.StationMeasureRecord(time_rec=t.TimeRecord()),
            log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_type_wrapper = sel_type.StationTypeSelectWrapper(conn=database_connection,
                                                                query_builder=query_builder,
                                                                sensor_type=sensor_type)
        # SensorIDSelectWrapper
        sensor_id_select_wrapper = sel_type.SensorIDSelectWrapper(conn=database_connection,
                                                                  query_builder=query_builder,
                                                                  log_filename=self.log_filename)

        ################################ ADAPTER-SIDE OBJECTS ################################
        # Used for reshaping the sensor data into a proper shape for converting into SQL rec
        api2db_adapter = adapt.ThingspeakMeasureAdapter(sel_type=select_type_wrapper)

        # Used for reshaping database api parameters for fetching data
        db2api_adapter = par_adapt.ThingspeakParamAdapter()

        # Date looper class
        date_looper_class = looper.get_date_looper_class(sensor_type=sensor_type)

        # Build command object
        cmd = command.FetchCommand(fetch_wrapper=fetch_wrapper,
                                   insert_wrapper=insert_wrapper,
                                   select_type_wrapper=select_type_wrapper,
                                   id_select_wrapper=sensor_id_select_wrapper,
                                   api2db_adapter=api2db_adapter,
                                   db2api_adapter=db2api_adapter,
                                   date_looper_class=date_looper_class)
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd

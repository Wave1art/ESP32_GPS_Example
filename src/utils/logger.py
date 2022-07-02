""" Micro Python simple logging framework"""

import time, json
from utils import folder
from utils.timeutils import strftime

class LogBackendBuffer():
    """ A list based log buffer"""

    logger_type = 'Buffer logger backend'

    def __init__(self) -> None:
        self.__log_buffer = []

    def log_data(self, log_data):
        """ Appends the latest log message to the buffer """
        self.__log_buffer.append(log_data)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        # Stop iteration if there's nothing left to return
        if self.i >= len(self.__log_buffer):
            raise StopIteration

        # else return the next item in the list
        lb = self.__log_buffer[self.i]
        self.i += 1

        return json.dumps(lb)


class LogBackendFile():
    """ A file based logging backend """

    logger_type = 'File logger backend'

    def __init__(self, target_directory:str = None, file_name_pattern: str = None, file_format: str = 'JSON_LINE',
                 over_write: bool = False):
        self.__target_directory: str = target_directory
        self.__file_name_pattern: str = file_name_pattern
        self.__file_format: str = file_format,
        self.__over_write: bool = over_write

        # set up the file directory if it doesn't already exist
        folder.mkdir_if_not_exist(self.__target_directory)

        self.__open_file_backend(self.__file_name_pattern, time.gmtime(), self.__over_write)

    def __open_file_backend(self, file_name_pattern: str, timestamp: time, over_write: bool = False):
        """ Creates the filename string based on the pattern, log timestamp and supplied data or parameters """
        # todo: extend the filename patterns to be able to cope with different parameters
        # todo: implement the pattern detection!!!!

        filename = "{file_name_pattern}_{year}{month}{hour}{minute}{second}_UTC.jsonl".format(
            file_name_pattern = file_name_pattern,
            year = timestamp[0],
            month = timestamp[1],
            hour = timestamp[3],
            minute = timestamp[4],
            second = timestamp[5])

        self.__out_file_path = "{directory}/{filename}".format(directory = self.__target_directory, filename = filename)

        self.__logstream = open(self.__out_file_path,
                                mode=('w' if over_write else 'a'),
                                encoding='utf-8')

    def log_data(self, log_data, timestamp: time = time.gmtime()):
        """ logs a data payload to the logging backend """
        # todo: check for different logger types other than jsonlines
        # todo: check if time is after current duration, if so close and rotate fthe file

        # check if the backend is open, create it if not
        if self.__logstream is None:
            self.__open_file_backend(self.__file_name_pattern, timestamp, self.__over_write)

        # log the data to the backend
        self.__logstream.write(json.dumps(log_data))
        self.__logstream.write('\n')
        self.__logstream.flush()

    def close_logger(self):
        self.__logstream.close()

    def get_file_path(self) -> str:
        """ returns the full path and filename for the file currently writing to """
        return self.__out_file_path


class DataLogger():
    """" Data Logger is a lightweight MicroPython class which can write log files using a numer of different
    approaches """

    def __init__(self, logger_backend=None, print_outputs = False):
        self.__print_outputs = print_outputs
        self.__logstream = LogBackendBuffer() if logger_backend is None else logger_backend

    def log_data(self, log_data):
        if self.__print_outputs == True: print(str(log_data))

        self.__logstream.log_data(log_data)

    def log(self, message):
        """ Simple structure log message without a data payload. Will automatically wrap with a timestamp and the
        calling module """
        log_payload = {
            'datetime': strftime(time.gmtime()),
            'function': __name__,
            'log_level': '',
            'message': message
        }

        self.log_data(log_payload)

    def change_logger_backend(self, new_logger_backend, copy_logs=True, change_timestamp: int = 0, change_timestamp_key: str = '', delete_logs=False):
        """ Changes the logger backend whilst it is being used.
            Copy_logs = True:  will copy all previous log entries from the old log to the new log
            change_timestamp != 0 will modify any timestamp by the number of seconds given. This is useful when writing logs stored to a buffer before the RTC is set correctly
            change_timestanp_key: the key that should be associated with a timestamp to modify. this is applied only at the top level of each message, not recursive currently
            Delete_logs will delete any files associated with the current (previous) logging backend
        """

        if copy_logs == True:
            # loop through each of the entries in the current log
            for le in self.__logstream:
                # todo: if change timestamp is set then modify the timestamp it it's found
                if change_timestamp != 0 and change_timestamp_key != '':
                    log_message = json.loads(le)
                    if change_timestamp_key in log_message.keys():
                        # original timestamp is in formatted version
                        a = log_message[change_timestamp_key]

                        orig_time_s = time.mktime((int(a[0:4]), int(a[4:6]), int(a[6:8]), int(a[8:10]), int(a[10:12]), int(a[12:14]), 0, 1))

                        # convert to seconds after default
                        new_timestamp = orig_time_s + change_timestamp

                        log_message[change_timestamp_key] = strftime(time.gmtime(new_timestamp))

                else:
                    # only a simple copy is needed
                    log_message = le

                # Write the (potentially modified) log entry to the new backend
                new_logger_backend.log_data(log_message)

            # (maybe terminate the old logger) and swap the reference to the new logger
            self.__logstream = new_logger_backend




    def close_logger(self):
        self.__logstream.close_logger()
import time



def strftime(time_to_format: time, str_format:str = ''):
    """ Basic string from time function operating on time object """
    return f"{time_to_format[0]:04d}{time_to_format[1]:02d}{time_to_format[2]:02d}{time_to_format[3]:02d}{time_to_format[4]:02d}{time_to_format[5]:02d}"

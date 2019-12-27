"""
This file contains classes, methods and constants that would be used all across the Project
"""

# region imports
import traceback
import sys
import ntpath
# endregion imports


# region ConsoleLog
class Console(object):
    """
    This class is used in order to print color coded messages:
    -
    """
    def __init__(self):
        self._traceback_step = -2

        # region console log flags
        self.LOG_ERROR = 0x00
        self.LOG_WARNING = 0x01
        self.LOG_SUCCESS = 0x02
        self.LOG_INFO = 0x03
        self.LOG_DEFAULT = 0x04
        # endregion console log flags

        # region messages color codes
        self._CODE_RED = '\033[1;31;49m'
        self._CODE_YELLOW = '\033[1;33;49m'
        self._CODE_GREEN = '\033[1;32;49m'
        self._CODE_BLUE = '\033[1;34;49m'
        self._CODE_WHITE = '\033[1;39;49m'
        self._CODE_HIGHLIGHT = '\033[1;95;49m'
        self._CODE_DEFAULT = '\033[1;39;49m'
        # endregion messages color codes

        # region message parameters
        self._filename = None
        self._relative_filename = None
        self._line_number = None
        self._process_name = None
        self._message = None
        self._current_color_code = None
        self._label = None
        # endregion message parameters

    def log(self, message, priority=None):
        """
        This method is used in order to return color coded messages

        :param message: (String) The message that needs to be displayed
        :param priority: (Integer) The flag associated to a specific type of message. The accepted flag, alongside their
        associated color are:

        {
            LOG_ERROR: RED,

            LOG_WARNING: YELLOW,

            LOG_SUCCESS: GREEN,

            LOG_INFO: BLUE,

            LOG_DEFAULT: WHITE
        }

        Default value: LOG_DEFAULT

        :return: Boolean (True of False)
        """
        try:
            self._message = str(message).capitalize()

            stack = traceback.extract_stack()
            (self._filename, self._line_number, self._process_name, text) = stack[self._traceback_step]

            self._relative_filename = ntpath.basename(self._filename)

            if sys.exc_info()[-1] is not None:
                self._line_number = sys.exc_info()[-1].tb_lineno
            else:
                self._line_number = 'N/A'

            if priority == self.LOG_ERROR:
                self._label = 'Error'
                self._current_color_code = self._CODE_RED
            elif priority == self.LOG_WARNING:
                self._label = 'Warning'
                self._current_color_code = self._CODE_YELLOW
            elif priority == self.LOG_SUCCESS:
                self._label = 'Success'
                self._current_color_code = self._CODE_GREEN
            elif priority == self.LOG_INFO:
                self._label = 'Info'
                self._current_color_code = self._CODE_BLUE
            elif priority == self.LOG_DEFAULT or priority is None:
                self._label = 'Regular'
                self._current_color_code = self._CODE_DEFAULT
            else:
                print('%s Warning: %s Invalid priority %s' % (self._CODE_YELLOW, self._CODE_HIGHLIGHT, str(priority)))
                return False

            dict_message_struct = {
                'header': ('%s %s: %s\n' % (self._current_color_code, self._label, self._CODE_HIGHLIGHT)),
                'filename': ('\t- Filename: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._relative_filename), self._CODE_HIGHLIGHT)),
                'line_number': '',
                'process': ('\t- Process: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._process_name), self._CODE_HIGHLIGHT)),
                'message': ('\t- Message: %s \"%s\" %s\n' % (
                    self._CODE_DEFAULT, str(self._message), self._CODE_HIGHLIGHT)),
                'delimiter': ('%s------------------------------\n' % self._CODE_DEFAULT)
            }

            if self._line_number != 'N/A':
                dict_message_struct['line_number'] = ('\t- Line Number: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._line_number), self._CODE_HIGHLIGHT))

            print('%s%s%s%s%s%s%s' % (dict_message_struct['delimiter'],
                                      dict_message_struct['header'],
                                      dict_message_struct['filename'],
                                      dict_message_struct['line_number'],
                                      dict_message_struct['process'],
                                      dict_message_struct['message'],
                                      dict_message_struct['delimiter']))

            return True

        except Exception as error_message:
            stack = traceback.extract_stack()
            (self._filename, self._line_number, self._process_name, text) = stack[-1]

            filename = self._filename.split('\\')
            self._relative_filename = filename[len(filename) - 1]

            if sys.exc_info()[-1] is not None:
                self._line_number = sys.exc_info()[-1].tb_lineno
            else:
                self._line_number = 'N/A'

            dict_message_struct = {
                'header': ('%s %s %s:\n' % (self._current_color_code, self._label, self._CODE_HIGHLIGHT)),
                'filename': ('\t- Filename: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._relative_filename), self._CODE_HIGHLIGHT)),
                'line_number': '',
                'process': ('\t- Process: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._process_name), self._CODE_HIGHLIGHT)),
                'message': ('\t- Message: %s \"%s\" %s\n' % (
                    self._CODE_DEFAULT, str(self._message), self._CODE_HIGHLIGHT)),
                'delimiter': ('%s------------------------------\n' % self._CODE_DEFAULT)
            }

            if self._line_number != 'N/A':
                dict_message_struct['line_number'] = ('\t- Line Number: %s %s %s\n' % (
                    self._CODE_DEFAULT, str(self._line_number), self._CODE_HIGHLIGHT))

            print('%s%s%s%s%s%s%s' % (dict_message_struct['delimiter'],
                                      dict_message_struct['header'],
                                      dict_message_struct['filename'],
                                      dict_message_struct['line_number'],
                                      dict_message_struct['process'],
                                      dict_message_struct['message'],
                                      dict_message_struct['delimiter']))
            return False
# endregion ConsoleLog


# region exports
console = Console()
# endregion exports

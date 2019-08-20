from termcolor import colored

from .utils import msg_template_reader


class Robot(object):

    msg_header = msg_template_reader\
        .get_template_from_file('robot_package/texts/msg_header.txt')
    msg_footer = msg_template_reader \
        .get_template_from_file('robot_package/texts/msg_footer.txt')

    def __init__(self, name='Robot'):
        self.name = name

    def print_msg(self, msg):
        print(colored(self.msg_header, 'blue'))
        print(colored(msg, 'blue'))
        print(colored(self.msg_footer, 'blue'))

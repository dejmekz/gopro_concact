#!/usr/bin/env python3

'''
GoPro-Concat-Automation  v 0.5
January 2025
created by: steven cucolo stevenc.github@gmail.com
updated by: Zdeněk Dejmek

GoPro records MP4 files that are segmented based on a 4Gb file size limit.
This script will go through a large batch of segmented GoPro files and
merge them based on their GoPro file number and creation dates.
An option to downconvert the merged file is also provided. The file merge
and downconvert is performed by FFMPEG.
'''

PROG_VERSION = 0.5
DEBUG_ENABLED = False

from argparse import ArgumentParser
import gopro_concat as gp
from os import chdir
import sys

def ParseInputArguments() -> list:
    global DEBUG_ENABLED

    #parser = ArgumentParser(prog="Alerta tester",description="Test create objects of Alerta", epilog="Execute automation test of CLI interface")
    parser = ArgumentParser(description="Test create objects of Alerta", epilog="Execute automation test of CLI interface")
    parser.add_argument('-s','--source', action='store', help='source input path', default=None, type=str)
    parser.add_argument('-o','--output', action='store', help='ouput path', default=None, type=str)
    parser.add_argument('-a','--all', action='store_true', help='concat all files in one file')
    parser.add_argument('-v','--version', action='version', help='print version information and exit', version="%(prog)s " + PROG_VERSION)
    parser.add_argument('-d','--debug', action='store_true', help='print alertinguicli information')

    parsed_args=parser.parse_args()

    source = parsed_args.source
    output = parsed_args.output

    if (source is None) or (output is None):
        parser.print_help()
        sys.exit("Missing source path or output path")

    DEBUG_ENABLED = parsed_args.debug
    all_in_one = parsed_args.all

    #print(parsed_args)

    return [source, output, all_in_one]

def gopro_main(source_path: str, output_path: str, all_in_one: bool):
    '''
    Get the user input and pass it into the concat and/or downconvert
    functions.
    '''

    print(f"\n\
    ================================================================\n \
                GoPro Automation Script, version 0.5 \n \
    This script will take a collection of chaptered GoPro video files \n \
    and stitch them together with the option to also downconvert them \n \
    to a 10Mbit file. \n \
    ================================================================\n"
    )    

    print(f"\
    ================================================================\n \
        Starting the GoPro concat with these values : \n \
            Source Path: {str(source_path)} \n \
            Output Path: {str(output_path)} \n \
             All in one: {str(all_in_one)} \n \
      DownConvert (Y/N): No \n \
    ===========================================================\n ")

    grouped_gopro_files = gp.get_grouped_files(source_path, DEBUG_ENABLED)
    file_numer_list = sorted(list(grouped_gopro_files.keys()))

    chdir(output_path)

    if all_in_one == True:
        print('Processing concat now...')
        gp.ffmpeg_concat_as_one_file(file_numer_list, grouped_gopro_files, source_path, output_path, DEBUG_ENABLED)            
    else:
        print('Processing concat now...')
        for file_number in file_numer_list:            
            gp.ffmpeg_concat_by_file_number(file_number, grouped_gopro_files, source_path, output_path, DEBUG_ENABLED)            

    #else:
    #    print( "Processing downconvert now...")
    #    for file_number in file_numer_list:
    #        gp.ffmpeg_downconvert(file_number, grouped_gopro_files, source_path, output_path)

    print('FFMPEG process complete.')

if __name__ == '__main__':
    args = ParseInputArguments()
    gopro_main(args[0], args[1], args[2])


#!/usr/bin/env python3

'''
GoPro-Concat-Automation  v 0.2
March 2019

Concat Steps:
    Make a list of all the files in a GoPro a directory.
    Loop through the list and group files based on name and creation.
    Get the mediainfo for these files.
    Create a .txt file(s) with the full paths of files used for sub to FFMPEG.
    FFMPEG concats the grouped MP4 into one file, and gives the option to
    downconvert.
'''

from os import listdir
from os.path import isfile, join
import re
import subprocess
import get_mediainfo as media

from datetime import datetime
from pathlib import Path

def get_grouped_files(source_path: str, debug: bool = False) -> dict:
    '''
    Create a list of all the MP4 files in the given Source Dir.
    File names must follow the specific pattern defined in the
    regex statement.
    '''

    all_gopro_files = []
    grouped_gopro_files = {}

    only_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]

    if debug is True:
        print("FILE LIST: " + str(only_files))

    pat = re.compile(r"[gGhH]{2}\d{6}\.[mMpP]{2}4")

    for file_name in only_files:
        if pat.match(file_name):
            all_gopro_files.append(file_name)

    if debug is True:
        print("Valid gopro files: " + str(all_gopro_files))

    for file_name in all_gopro_files:
        file_number = file_name[4:8]

        if file_number not in grouped_gopro_files:
            fstring = f"[gGhH]\\d{{2}}{file_number}\.[mM][pP]4"
            r = re.compile(fstring)
            gplist = sorted(list(filter(r.match, all_gopro_files)))
            grouped_gopro_files.update({file_number:gplist})

    if debug is True:
        print("Grouped gopro files by part number: " + str(grouped_gopro_files))

    return grouped_gopro_files


def create_datetime(encoded_date):
    '''
    Create datetime string values based on the encoded_time value
    contained in the mediainfo for a MP4 file.
    '''

    year = int(encoded_date[4:8])
    month = int(encoded_date[9:11])
    day = int(encoded_date[12:14])
    hour = int(encoded_date[15:17])
    minute = int(encoded_date[18:20])
    second = int(encoded_date[21:23])

    gp_datetime = datetime(year, month, day, hour, minute, second)
    creation_date_str = gp_datetime.strftime("%Y%m%d%H%M%S")

    # print(gp_datetime)
    # print(creation_date_str)

    return creation_date_str


def create_ffmpeg_txtfile(file_number :str, grouped_files :dict, source_path :str, output_path :str, debug :bool = False) -> str:

    '''
    create a txt file with paths to a set our MP4 source files.
    the text file is passed into the FFMEG statment as the input.
    file '/path/to/file1'
    file '/path/to/file2'
    file '/path/to/file3'
    '''
    output_text_file_path = Path(output_path + file_number + '.txt')

    if debug is True:
        print("OUTPUT TEXT FILE PATH: " + str(output_text_file_path))

    output_text_file = open(output_text_file_path, 'w')
    gprfile_list = grouped_files[file_number]

    for file in gprfile_list:
        file_stmnt = "file " + '\'' + source_path + file + '\'' + "\n"
        output_text_file.write(file_stmnt)

    output_text_file.close()

    return output_text_file_path

def create_ffmpeg_txtfile_big(file_numbers :list, grouped_files :dict, source_path :str, output_path :str, debug :bool = False) -> str:

    '''
    create a txt file with paths to a set our MP4 source files.
    the text file is passed into the FFMEG statment as the input.
    file '/path/to/file1'
    file '/path/to/file2'
    file '/path/to/file3'
    '''
    output_text_file_path = Path(output_path + 'all_in_one.txt')

    if debug is True:
        print("OUTPUT TEXT FILE PATH: " + str(output_text_file_path))

    output_text_file = open(output_text_file_path, 'w')
    
    for file_number in file_numbers:   
        gprfile_list = grouped_files[file_number]
        for file in gprfile_list:
            file_stmnt = "file " + '\'' + source_path + file + '\'' + "\n"
            output_text_file.write(file_stmnt)

    output_text_file.close()

    return output_text_file_path

def ffmpeg_concat_by_file_number(file_number :str, grouped_files :dict, source_path :str, output_path :str, debug :bool = False):
    '''
    Use FFMPEG subprocess call to merge a set of MP4 files.
    '''

    gpr_txt_path = create_ffmpeg_txtfile(file_number, grouped_files, source_path, output_path, debug)

    firstfile = grouped_files[file_number][0]
    mediainfo = media.get_mediainfo(source_path, firstfile)

    if debug is True:
        print("MEDIA INFO: " + str(mediainfo))

    encoded_date = mediainfo['v_encoded_date']
    creation_time = 'creation_time=' + encoded_date
    gprkey_date = create_datetime(encoded_date)

    if debug is True:
        print("CREATION TIME: " + creation_time + " [ " + encoded_date + " ]")

    mp4_output = file_number + '_' + gprkey_date[:-6] + '.MP4'

    ffmpeg_cmd = [
                  'ffmpeg', '-safe', '0', '-f', 'concat',  '-i',
                  gpr_txt_path, '-c', 'copy', '-metadata', creation_time,
                  mp4_output
                  ]

    output_log = open(output_path + '/' + file_number + '_output.log', 'a')

    sp = subprocess.Popen(ffmpeg_cmd,
                          shell=False,
                          stderr=output_log,
                          stdout=output_log)

    _, _ = sp.communicate(input='N')

    output_log.close()

def ffmpeg_concat_as_one_file(file_numbers :list, grouped_files :dict, source_path :str, output_path :str, debug :bool = False):
    '''
    Use FFMPEG subprocess call to merge a set of MP4 files.
    '''

    gpr_txt_path = create_ffmpeg_txtfile_big(file_numbers, grouped_files, source_path, output_path, debug)

    firstfile = grouped_files[file_numbers[0]][0]
    mediainfo = media.get_mediainfo(source_path, firstfile)

    if debug is True:
        print("MEDIA INFO: " + str(mediainfo))

    encoded_date = mediainfo['v_encoded_date']
    creation_time = 'creation_time=' + encoded_date
    gprkey_date = create_datetime(encoded_date)

    if debug is True:
        print("CREATION TIME: " + creation_time + " [ " + encoded_date + " ]")

    mp4_output = 'all_in_one_' + gprkey_date[:-6] + '.MP4'

    ffmpeg_cmd = [
                  'ffmpeg', '-safe', '0', '-f', 'concat',  '-i',
                  gpr_txt_path, '-c', 'copy', '-metadata', creation_time,
                  mp4_output
                  ]

    output_log = open(output_path + '/all_in_one_output.log', 'a')

    sp = subprocess.Popen(ffmpeg_cmd,
                          shell=False,
                          stderr=output_log,
                          stdout=output_log)

    _, _ = sp.communicate(input='N')

    output_log.close()

def ffmpeg_downconvert(gprkey, gopr_dict, source_path, output_path):
    '''
    Use a FFMPEG subprocess call to downconvert a merged MP4 file.
    '''

    mp4_output, mediainfo, creation_time = ffmpeg_concat_by_file_number(gprkey, gopr_dict, source_path, output_path)

    bitrate = mediainfo['v_bit_rate']
    bitratemode = mediainfo['v_bit_rate_mode']
    codec = mediainfo['v_codec_id']
    framerate = mediainfo['v_frame_rate']
    encoded_date = mediainfo['v_encoded_date']
    width = mediainfo['v_width']
    height = mediainfo['v_height']
    a_format = mediainfo['a_format'].lower()
    a_bitrate = mediainfo['a_bit_rate']

    video_siz = str(width) + 'x' + str(height)

    mp4_source = mp4_output
    mp4_output = output_path + mp4_source[:-4] + "_downconvert.mp4"

    print("MP4 SOURCE:" + str(mp4_source))
    print("MP4 OUTPUT:" + str(mp4_output))

    output_log = open(output_path + '/' + gprkey + '_output.log', 'a')

    ffmpeg_cmd = ['ffmpeg', '-i', mp4_source, '-map', '0:0',
          '-map', '0:1', '-c:a', a_format, '-ab', '128k',
          '-strict', '-2', '-async', '1', '-c:v', 'libx264',
          '-b:v', '5000k', '-maxrate', '5000k', '-bufsize',
          '10000k', '-r', framerate, '-s', video_siz, '-aspect',
          '16:9', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
          '-level', '41', '-partitions',
          'partb8x8+partp4x4+partp8x8+parti8x8', '-b-pyramid',
          '2', '-weightb', '1', '-8x8dct', '1', '-fast-pskip',
          '1', '-direct-pred', '1', '-coder', 'ac', '-trellis',
          '1', '-me_method', 'hex', '-flags', '+loop',
          '-sws_flags', 'fast_bilinear', '-sc_threshold', '40',
          '-keyint_min', '60', '-g', '600', '-qmin', '3', '-qmax',
          '51', '-metadata', creation_time, '-sn', '-y', mp4_output]

    sp = subprocess.Popen(ffmpeg_cmd, shell=False,
                      stderr=output_log, stdout=output_log)

    (stderr, stdout) = sp.communicate(input='N')

    print(stderr, stdout)

    output_log.close()

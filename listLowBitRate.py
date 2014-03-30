import os
import re
import sys
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def init_list():
    traverse_directories()


def get_dir_name():
    return os.path.dirname(__file__)


def traverse_directories(root=__file__):
    root = os.path.dirname(os.path.abspath(root))
    log_file = root + '/mp3_list.txt'
    error_file = root + '/error_log.txt'
    counters = {'errors': 0, 'song_count': 0}
    total_counters = {'errors': 0, 'song_count': 0}
    visited = [root]
    while len(visited) > 0:
        parent = visited.pop()
        counters = search_dir(parent, log_file, error_file)
        total_counters['errors'] += counters['errors']
        total_counters['song_count'] += counters['song_count']
        child_dirs = add_child_dirs(parent, visited)
        for child in child_dirs:
            if child not in visited:
                visited.append(child)
    print 'program completed with ' + str(total_counters['errors']) + ' errors see error log for more details'
    print 'there are ' + str(total_counters['song_count']) + ' below 200 kb'


def add_child_dirs(path, visited=[]):
    siblings = os.listdir(path)
    sub_dirs = []

    for item in siblings:
        item = path + '/' + item
        if os.path.isdir(item) and item not in visited:
            sub_dirs.append(item)
    return sub_dirs


def search_dir(path, log_file, error_log):
    total_counters = {'errors': 0, 'song_count': 0}
    counters = {'errors': 0, 'song_count': 0}

    if path != '':
        siblings = os.listdir(path)
        if siblings:
            for item in siblings:
                if re.match('.*\.mp3', item):
                    counters = write_mp3_info(path + '/' + item, log_file, error_log)
                    total_counters['errors'] += counters['errors']
                    total_counters['song_count'] += counters['song_count']

    return total_counters


def write_mp3_info(file_name, log_file='', error_file=''):
    print 'Reading file ' + file_name
    audio = MP3(file_name)
    audio_id3 = EasyID3(file_name)

    error_log = os.open(error_file.encode('utf8'), os.O_RDWR|os.O_APPEND|os.O_CREAT)
    counters = {'errors': 0, 'song_count': 0}
    audio_info = ''
    bitrate = -1

    try:
        bitrate = audio.info.bitrate / 1000
        audio_info = str.format('Artist: {0:30} | Title: {1:40} | Album: {2:40} | Bitrate: {3}',
            unicode(audio_id3['artist'][0])[:30],
            unicode(audio_id3['title'][0])[:40],
            unicode(audio_id3['album'][0])[:40],
            str(bitrate))

        print 'Writing information to file'

    except Exception, ex:
        os.write(error_log, 'error reading file ' + file_name + ' ' + ex.message + '\n')
        print 'error reading file ' + file_name + ' ' + ex.message + '\n'
        counters['errors'] += 1

    try:
        if bitrate != -1 and bitrate < 256 and audio_info != '':
            counters['song_count'] += 1
            log = os.open(log_file.encode('utf8'), os.O_RDWR|os.O_APPEND|os.O_CREAT)
            os.write(log, audio_info)
            os.write(log, '\n')
    except Exception, ex:
        os.write(error_log, 'error writing ' + log_file + ' ' + ex.message + '\n')
        print 'error writing ' + log_file + ' ' + ex.message + '\n'
        counters['errors'] += 1

    return counters


if __name__ == '__main__':
    init_list()
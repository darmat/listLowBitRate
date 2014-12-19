import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


""" Constants """
LOG_NAME = 'Bitrate.log'
THRESHOLD = 256


def mp3_list(root='.'):
    """ Return a list of MP3 files from lower directory levels """
    return [os.path.join(root, file) 
                for root, dirs, files in os.walk(root) if files 
                for file in files if file.endswith('.mp3')]

def check_bitrate():
    """ This routine checks the bitrate of every MP3 and writes id tag information to a log file """
    with open(LOG_NAME, 'wb') as f:
        errors = 0
        for file in mp3_list():
            audio = MP3(file)
            audio_id3 = EasyID3(file)
            bitrate = audio.info.bitrate / 1000
            
            if bitrate > 0 and bitrate < THRESHOLD:
                f.write('Artist: %s | Album: %s | Title: %-40s | Bitrate: %i \n' % (unicode(audio_id3['artist'][0]),
                                                                                    unicode(audio_id3['album'][0]),
                                                                                    unicode(audio_id3['title'][0]),
                                                                                    bitrate))
            else:
                errors += 1
                
        f.write('Terminated with %i errors.' % (errors))

if __name__ == '__main__':
    check_bitrate()

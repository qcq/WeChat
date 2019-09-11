import logging
from watchdog.events import PatternMatchingEventHandler


class PicturePathHandler(PatternMatchingEventHandler):
    def __init(self, patterns, ignore_patterns, ignore_directories, case_sensitive):
        super(PicturePathHandler, self).__init__(patterns=patterns, ignore_patterns=ignore_patterns,
            ignore_directories = ignore_directories, case_sensitive = case_sensitive)
        #self._media = media

    def on_modified(self, event):
        print 'qcq is here with modify'

    def on_created(self, event):
        '''
        here will get the event when new file created under pictures path.
        when receive this event, will upload this picture to tencent, and
        insert corresponding media id into database.
        '''
        if event.src_path:
            logging.info('file %s created.' % event.src_path)
        print 'qcq is here with created', event.src_path

    def on_deleted(self, event):
        print 'qcq is here with delete'

    def on_moved(self, event):
        print 'qcq is here moved'

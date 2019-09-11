import logging
from pyeventbus import *
from watchdog.events import PatternMatchingEventHandler
from com.qcq.events.file_event import *


class PicturePathHandler(PatternMatchingEventHandler):
    def __init(self, patterns, ignore_patterns, ignore_directories, case_sensitive):
        super(PicturePathHandler, self).__init__(patterns=patterns, ignore_patterns=ignore_patterns,
            ignore_directories = ignore_directories, case_sensitive = case_sensitive)

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
        PyBus.Instance().post(FileEvent(FileEventType.CREATE,
                                        os.path.abspath(event.src_path), None))
        print 'qcq sent out the message'

    def on_deleted(self, event):
        print 'qcq is here with delete'

    def on_moved(self, event):
        print 'qcq is here moved'

    def register(self, aInstance):
            PyBus.Instance().register(aInstance, self.__class__.__name__)

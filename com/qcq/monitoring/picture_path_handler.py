import logging
from pyeventbus import *
from watchdog.events import PatternMatchingEventHandler
from com.qcq.events.file_event import *


class PicturePathHandler(PatternMatchingEventHandler):
    def __init(self, patterns, ignore_patterns, ignore_directories, case_sensitive):
        super(PicturePathHandler, self).__init__(patterns=patterns, ignore_patterns=ignore_patterns,
            ignore_directories = ignore_directories, case_sensitive = case_sensitive)

    def on_created(self, event):
        '''
        here will get the event when new file created under pictures path.
        when receive this event, will upload this picture to tencent, and
        insert corresponding media id into database.
        '''
        print 'qcq is here with created', event.src_path
        PyBus.Instance().post(FileEvent(FileEventType.CREATE,
            os.path.abspath(event.src_path), None))
        logging.info('file %s created. sent out event' % event.src_path)


    def on_deleted(self, event):
        '''
        '''
        PyBus.Instance().post(FileEvent(FileEventType.DELETE,
            os.path.abspath(event.src_path), None))
        logging.info("%s deleted. sent out event" % event.src_path)

    def on_moved(self, event):
        PyBus.Instance().post(FileEvent(FileEventType.MOVE, os.path.abspath(event.src_path),
            os.path.abspath(event.dest_path)))
        logging.info("%s renamed to %s. sent out event" % (event.src_path, event.dest_path))

    def register(self, aInstance):
            PyBus.Instance().register(aInstance, self.__class__.__name__)

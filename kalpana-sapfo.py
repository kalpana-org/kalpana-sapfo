from os.path import join, dirname, basename, isfile

from PyQt4 import QtCore, QtGui

from libsyntyche.common import read_json, parse_stylesheet, read_file, make_sure_config_exists
from pluginlib import GUIPlugin


class UserPlugin(GUIPlugin):
    def __init__(self, objects, get_path):
        super().__init__(objects, get_path)
        self.pluginpath = get_path()
        self.configpath = objects['settings manager'].get_config_directory()
        self.textarea = objects['textarea']
        self.textarea.file_opened.connect(self.set_title)
        self.textarea.file_saved.connect(self.set_title)

    def read_config(self):
        configfile = join(self.configpath, 'kalpana-sapfo.conf')
        make_sure_config_exists(configfile, join(self.pluginpath, 'defaultconfig.json'))
        self.settings = read_json(configfile)

    def set_title(self):
        if not self.settings['use sapfo title']:
            return
        fname = self.textarea.file_path
        metadatafile = join(dirname(fname), '.' + basename(fname) + '.metadata')
        if isfile(metadatafile):
            try:
                metadata = read_json(metadatafile)
                title = metadata['title']
            except:
                title = "##metadata error##"
            self.textarea.filename_changed.emit(title)

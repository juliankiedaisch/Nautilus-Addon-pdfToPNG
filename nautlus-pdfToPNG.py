import subprocess
import urllib.parse
from gi.repository import Nautilus, GObject
from pdf2image import convert_from_path
from typing import List

SUPPORTED_FORMATS = 'application/pdf'

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        print("Initialized test extension")

    def menu_activate_cb(self, menu: Nautilus.MenuItem, files: List[Nautilus.FileInfo],) -> List[Nautilus.MenuItem]:
        for item in files:
            pages = convert_from_path(urllib.parse.unquote(item.get_uri().replace("file://", "")), 500)
            for index in range(len(pages)):
                pages[index].save(urllib.parse.unquote(item.get_uri().replace("file://", "").split(".")[0] + "_" + str(index) + ".png"), 'PNG')
    def get_file_items(self, files: List[Nautilus.FileInfo],) -> List[Nautilus.MenuItem]:

        for item in files:
            if not item.get_mime_type() in SUPPORTED_FORMATS:
                return []
            if item.get_uri_scheme() != 'file':
                return []

        item = Nautilus.MenuItem(
            name="SimpleMenuExtension::FileCopy", label="PDF in PNG umwandeln", tip="", icon=""
        )
        item.connect("activate", self.menu_activate_cb, files)
        return [item,]

    def get_background_items(self, current_folder: Nautilus.FileInfo,) -> List[Nautilus.MenuItem]: return []

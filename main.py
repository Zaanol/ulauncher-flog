import logging
import base64
import os
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.event import ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

logger = logging.getLogger(__name__)

class FLOGToolsExtension(Extension):

    def __init__(self):
        logger.info('init Flog Tools')
        super(FLOGToolsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def generate_key():
        current_date = datetime.today().strftime('%Y-%m-%d')
        current_date_bytes = current_date.encode("ascii")

        base64_bytes = base64.b64encode(current_date_bytes)
        base64_string = base64_bytes.decode("ascii")

        return FLOGToolsExtension.createItem("Tools Key", base64_string, CopyToClipboardAction(base64_string))

    def all_options_front():
        front_options = []

        front_options.append(FLOGToolsExtension.option_build_front())
        front_options.append(FLOGToolsExtension.option_update_build_front())
        front_options.append(FLOGToolsExtension.option_update_build_start_front())
        front_options.append(FLOGToolsExtension.option_start_front())

        return front_options

    def option_build_front():
        data = {"command": "front_build"}
        return FLOGToolsExtension.createItem("Tools Front Build", "Frontend Build", ExtensionCustomAction(data, keep_app_open=True))

    def build_front(extension):
        FLOGToolsExtension.executeBash("cd " + FLOGToolsExtension.getFrontPath(extension) + "; npm run build")

    def option_update_build_front():
        data = {"command": "front_update_build"}
        return FLOGToolsExtension.createItem("Tools Front Update Build", "Frontend Update Build", ExtensionCustomAction(data, keep_app_open=True))

    def update_build_front(extension):
        FLOGToolsExtension.executeBash("cd " + FLOGToolsExtension.getFrontPath(extension) + "; git pull; npm run build")

    def option_update_build_start_front():
        data = {"command": "front_update_build_start"}
        return FLOGToolsExtension.createItem("Tools Front Update Build Start", "Frontend Update Build Start", ExtensionCustomAction(data, keep_app_open=True))

    def update_build_start_front(extension):
        FLOGToolsExtension.executeBash("cd " + FLOGToolsExtension.getFrontPath(extension) + "; git pull; npm run build; npm run start")

    def start_front(extension):
        FLOGToolsExtension.executeBash("cd " + FLOGToolsExtension.getFrontPath(extension) + "; npm run start")

    def option_start_front():
        data = {"command": "front_start"}
        return FLOGToolsExtension.createItem("Tools Front Start", "Frontend Start", ExtensionCustomAction(data, keep_app_open=True))

    def create_suggestions():
        suggestions = []

        suggestions.append(FLOGToolsExtension.createItem(
            "Sugestão: Tools Key",
            "Comando para gerar key tools Financeiro",
            CopyToClipboardAction("flog key")))

        suggestions.append(FLOGToolsExtension.createItem(
                    "Sugestão: Tools Front",
                    "Comando para listar as ferramentas de front",
                    CopyToClipboardAction("flog front")))

        return suggestions

    def createItem(name, description, on_enter):
        return ExtensionResultItem(icon='images/icon.ico',
                                  name=name,
                                  description=description,
                                  highlightable=False,
                                  on_enter=on_enter)

    def executeBash(command):
        return os.system("gnome-terminal -e 'bash -c \"" + command + "\" '")

    def getFrontPath(extension):
        return extension.preferences.get('flog_front_directory')

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        query = event.get_argument() or str()

        if query == "key":
            items.append(FLOGToolsExtension.generate_key())
        elif query == "front":
            items.extend(FLOGToolsExtension.all_options_front())
        elif query == "front start":
            items.append(FLOGToolsExtension.option_start_front())
        elif query == "front build":
            items.append(FLOGToolsExtension.option_build_front())
        elif query == "front update build":
            items.append(FLOGToolsExtension.option_update_build_front())
        elif query == "front update build start":
            items.append(FLOGToolsExtension.option_update_build_start_front())

        items.extend(FLOGToolsExtension.create_suggestions())

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        command = event.get_data()["command"]

        if command == "front_start":
            FLOGToolsExtension.start_front(extension)
        elif command == "front_build":
            FLOGToolsExtension.build_front(extension)
        elif command == "front_update_build":
            FLOGToolsExtension.update_build_front(extension)
        elif command == "front_update_build_start":
            FLOGToolsExtension.update_build_start_front(extension)

if __name__ == '__main__':
    FLOGToolsExtension().run()
import logging
import base64
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class FLOGToolsExtension(Extension):

    def __init__(self):
        logger.info('init Flog Tools')
        super(FLOGToolsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def generate_key():
        current_date = datetime.today().strftime('%Y-%m-%d')
        current_date_bytes = current_date.encode("ascii")

        base64_bytes = base64.b64encode(current_date_bytes)
        base64_string = base64_bytes.decode("ascii")

        return FLOGToolsExtension.createItem("Tools Key", base64_string, CopyToClipboardAction(base64_string))

    def create_suggestions():
        suggestions = []

        suggestions.append(FLOGToolsExtension.createItem(
            "Sugestão: Tools Key",
            "Comando para gerar key tools Financeiro",
            CopyToClipboardAction("flog key")))

        return suggestions

    def createItem(name, description, on_enter):
        return ExtensionResultItem(icon='images/icon.ico',
                                  name=name,
                                  description=description,
                                  highlightable=False,
                                  on_enter=on_enter)

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        query = event.get_argument() or str()

        if query == "key":
            items.append(FLOGToolsExtension.generate_key())

        items.extend(FLOGToolsExtension.create_suggestions())

        return RenderResultListAction(items)

if __name__ == '__main__':
    FLOGToolsExtension().run()
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

class FLogToolsExtension(Extension):

    def __init__(self):
        logger.info('init Flog Tools')
        super(FLogToolsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        query = event.get_argument() or str()

        if query == "key":
            items.append(generate_key())

        return RenderResultListAction(items)

    def generate_key():
        current_date = datetime.today().strftime('%Y-%m-%d')
        current_date_bytes = current_date.encode("ascii")

        base64_bytes = base64.b64encode(current_date_bytes)
        base64_string = base64_bytes.decode("ascii")

        return ExtensionResultItem(icon='images/icon.ico',
                                    name="Tools Key",
                                    description=base64_string,
                                    highlightable=False,
                                    on_enter=CopyToClipboardAction(base64_string))

if __name__ == '__main__':
    FLogToolsExtension().run()
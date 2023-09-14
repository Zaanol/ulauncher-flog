import logging
import base64
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from random import randint
from time import sleep

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

        options = webdriver.ChromeOptions()
        #options.headless = True

        options.add_argument("--user-data-dir=/home/zanol/.config/google-chrome")
        options.binary_location = "/opt/google/chrome/chrome"
        options.add_argument("--profile-directory=Profile 1")
        options.add_argument("--user-cache-dir=/home/zanol/.cache/google-chrome")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        service = Service(r'/home/zanol/.local/share/ulauncher/extensions/com.github.zaanol.ulauncher-flog/chromedriver')

        driver = webdriver.Chrome(service=service, options=options)
        # Time to wait for element's presence
        driver.implicitly_wait(10)
        driver.get('https://login.tfc9924.k8s.us-central1.gcp.tks.sh/')
        #print (driver.page_source.encode("utf-8"))

        sleep(200)
        driver.quit()

        return RenderResultListAction(items)

if __name__ == '__main__':
    FLOGToolsExtension().run()

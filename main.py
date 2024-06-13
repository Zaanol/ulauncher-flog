import logging
import base64
import os
import csv
import requests
import json
from requests.auth import HTTPBasicAuth
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

    def option_jira_import_worklogs():
        data = {"command": "jira_import_worklogs"}
        return FLOGToolsExtension.createItem("Tools Jira Import Worklogs", "Jira Import Worklogs", ExtensionCustomAction(data, keep_app_open=True))

    def jira_import_worklogs(extension):
        jiraWorklogCsv = FLOGToolsExtension.getJiraWorklogCsvPath(extension)
        jiraConfig = FLOGToolsExtension.getJiraConfig(extension)

        with open(jiraWorklogCsv, newline='') as theFile:
            reader = csv.DictReader(theFile)

            for worklog in reader:
                FLOGToolsExtension.jira_import_worklog(jiraConfig, worklog)

    def jira_import_worklog(jiraConfig, worklog):
        print(worklog)

        data = {
            "originTaskId": worklog['issue'],
            "comment": worklog['comment'],
            "started": FLOGToolsExtension.formatDate(worklog['date']),
            "timeSpentSeconds": FLOGToolsExtension.hourToSeconds(worklog['hours']),
            "worker": jiraConfig['worker']
        }

        json_data = json.dumps(data)

        os.system(
            f"curl --request POST "
            f"--url '{jiraConfig['url']}' "
            f"--user '{jiraConfig['fullUser']}' "
            f"--header 'Accept: application/json' "
            f"--header 'Content-Type: application/json' "
            f"--data '{json_data}'"
        )

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
            "Sugestão: Jira import worklogs",
            "Comando para importar apontamentos de lista CSV para o Jira",
            CopyToClipboardAction("flog jira import worklogs")))

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
        print(f"gnome-terminal -- bash -c \"{command}; bash\"")
        return os.system(f"gnome-terminal -- bash -c \"{command}; bash\"")

    def getFrontPath(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_front_directory')

    def getJiraWorklogCsvPath(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_worklog_directory')

    def getJiraUrl(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_jira_url')

    def getJiraUser(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_jira_user')

    def getJiraPassowrd(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_jira_password')

    def getJiraWorker(extension):
        return FLOGToolsExtension.getPreference(extension, 'flog_jira_worker')

    def getPreference(extension, preference_id):
        return extension.preferences.get(preference_id)

    def getJiraConfig(extension):
        jiraUrl = FLOGToolsExtension.getJiraUrl(extension)

        jiraUser = FLOGToolsExtension.getJiraUser(extension)
        jiraPassword = FLOGToolsExtension.getJiraPassowrd(extension)

        return {
            "url": jiraUrl + "/rest/tempo-timesheets/4/worklogs/",
            "fullUser": jiraUser + ':' + jiraPassword,
            "worker": FLOGToolsExtension.getJiraWorker(extension)
        }

    def hourToSeconds(hour):
        return int(float(hour) * 3600)

    def formatDate(date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        return date_obj.strftime('%Y-%m-%dT12:00:00.000')

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        query = event.get_argument() or str()

        if query == "key":
            items.append(FLOGToolsExtension.generate_key())
        elif query == "jira import worklogs":
            items.append(FLOGToolsExtension.option_jira_import_worklogs())
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

        if command == "jira_import_worklogs":
            FLOGToolsExtension.jira_import_worklogs(extension)
        elif command == "front_start":
            FLOGToolsExtension.start_front(extension)
        elif command == "front_build":
            FLOGToolsExtension.build_front(extension)
        elif command == "front_update_build":
            FLOGToolsExtension.update_build_front(extension)
        elif command == "front_update_build_start":
            FLOGToolsExtension.update_build_start_front(extension)

if __name__ == '__main__':
    FLOGToolsExtension().run()
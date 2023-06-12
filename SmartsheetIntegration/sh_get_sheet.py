import smartsheet
import json
import requests
import re
import logging
import sys
import yaml

## Load config from yaml
config = yaml.safe_load(open("config.yml"))

## log handling
logging.basicConfig(filename='smartsheet_audit.log', format='>> %(asctime)s - %(levelname)s - %(message)s', level=logging.set_log_level)
def my_handler(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))
sys.excepthook = my_handler

## Smartsheet extraction and transformation
class smartsheetToLdif():
    ## Use a key store of your choice and return token to this variable
    smartsheet_token = ""

    ## connection to smartsheet
    smart = smartsheet.Smartsheet(str(smartsheet_token))

    ## base json and field mapping
    base_json = {
        "connectorType": "SmartsheetIntegration",
        "connectorId": "lxSmartsheetInboundConnector",
        "connectorVersion": "1.0.0",
        "lxVersion": "1.0.0",
        "description": "",
        "processingDirection": "inbound",
        "processingMode": "partial",
        "customFields": {},
        "content": []
    }

    ## returns array of workspace data and sheet to workspace map
    def get_all_workspaces(self, smart):
        self.sh_wkspc_map = {}
        self.all_wkspc = smart.Workspaces.list_workspaces()
        self.wkspc_arr = []
        num_wkspc, num_sht = 0, 0

        for wkspc in self.all_wkspc.data:
            num_wkspc += 1
            self.wkspc_arr.append([str(wkspc.id), wkspc.name])
            wkspc_data = smart.Workspaces.get_workspace(wkspc.id)
            # sheets and _sheets seem to be broken, works as dict
            wkspc_dict = wkspc_data.to_dict()
            logging.debug('Workspace data: %s',str(wkspc_dict))
            # create map of sheets to workspaces
            for a_sheet in wkspc_dict["sheets"]:
                num_sht += 1
                str_id = str(a_sheet["id"])
                new_wkspc = {}
                new_wkspc[str_id] = {}
                new_wkspc[str_id]["wkspc_id"] = str(wkspc.id)
                new_wkspc[str_id]["wkspc_name"] = wkspc.name
                new_wkspc[str_id]["type"] = "workspace"
                self.sh_wkspc_map.update(new_wkspc)

        logging.info('Processing %i sheets from %i workspaces.', num_sht, num_wkspc)
        return self.wkspc_arr, self.sh_wkspc_map


    ## returns id of all sheets
    def get_all_sheets(self, smart, sht_wkspc_map):
        # get all sheets
        self.response = smart.Sheets.list_sheets(include_all=True)
        self.sheets = self.response.data
        self.all_sheets = []
        # loop over sheets to get id"s
        for a_sheet in self.sheets:
            logging.debug('Sheet data: %s', str(a_sheet.to_dict()))
            str_id = str(a_sheet.id)
            row_data = {}
            row_data["type"] = "Sheet"
            row_data["id"] = str_id
            row_data["data"] = {}
            row_data["data"]["name"] = a_sheet.name
            row_data["data"]["createdAt"] = a_sheet._created_at.value.strftime("%Y-%m-%d")
            if str_id in sht_wkspc_map:
                row_data["data"]["parentId"] = sht_wkspc_map[str_id]["wkspc_id"]
            self.all_sheets.append(row_data)

        logging.info('Processing %i total sheets (including from workspaces).', len(self.all_sheets))
        return self.all_sheets

    ## returns dict of sheet data to feed ldif
    def get_sheet_data(self, smart, all_sheets, field_mapper):
        self.all_columns = {}
        self.all_sheet_data = []
        self.i = 1
        self.webhook_map = {}
        num_sht, num_row, num_cell = 0, 0, 0

        for a_sheet in all_sheets:
            num_sht += 1
            sheet_data = smart.Sheets.get_sheet(int(a_sheet["id"])) 
            # populate dict of column id:name 
            for a_column in sheet_data.columns:
                self.all_columns[str(a_column.id)] = a_column.title

            # build dict for each row
            for a_row in sheet_data.rows:
                logging.debug('Row data: %s', str(a_row.to_dict()))
                num_row += 1
                row_data = {}
                row_data["type"] = "Task"
                row_data["id"] = str(a_row.id)
                row_data["data"] = {}
                row_data["data"]["createdAt"] = str(a_row._created_at.value.strftime("%Y-%m-%d"))
                row_data["data"]["modifiedAt"] = str(a_row._modified_at.value.strftime("%Y-%m-%d"))
                row_data["data"]["modifiedBy"] = str(a_row._modified_by.value)
                row_data["data"]["parentId"] = str(a_row._parent_id)
                row_data["data"]["projectId"] = str(a_sheet["id"])
                row_data["data"]["projectName"] = str(sheet_data.name)

                all_cells = a_row.cells
                for a_cell in all_cells:
                    try:
                        logging.debug('Cell data: %s', str(a_cell.to_dict()))
                        num_cell += 1
                        if self.all_columns[str(a_cell._column_id)] in field_mapper:
                            row_data["data"][field_mapper[self.all_columns[str(a_cell._column_id)]]] = a_cell._value
                        else:
                            row_data["data"][self.all_columns[str(a_cell._column_id)]] = a_cell._value
                    except KeyError:
                        logging.debug('Column not in map: %s', str(a_cell._column_id))
                        pass

                self.all_sheet_data.append(row_data)

        logging.info('Extracted data from %i cells, %i rows, %i sheets.', num_cell, num_row, num_sht)
        return self.all_sheet_data 

    ## transform 
    def transform_to_ldif(self, base_json, all_sheets, all_tasks, workspaces="None"):
        if workspaces != "None":
            for wrkspc in workspaces:
                new_content = {}
                new_content["type"] = "Workspace"
                new_content["id"] = wrkspc[0]
                new_content["data"] = {}
                new_content["data"]["name"] = wrkspc[1]
                base_json["content"].append(new_content)

        for a_sheet in all_sheets:
            base_json["content"].append(a_sheet)

        for a_task in all_tasks:
            base_json["content"].append(a_task)

        return base_json

## Load Smartsheet data to LeanIX workspace
class ldifToWorkspace:
    ## Load inbound processor to variable
    with open("sh_processor.json") as json_file:
        ldif_processor = json.load(json_file)

    ## Use a key store of your choice and return token to this variable
    lix_api_token = ""

    ## Create header for LeanIX connection
    def createLeanixConnection(self, lix_api_token, auth_url):
        self.response = requests.post(auth_url, auth=("apitoken", lix_api_token), data={"grant_type": "client_credentials"})
        self.response.raise_for_status()
        header = {"Authorization": "Bearer " + self.response.json()["access_token"], "Content-Type": "application/json"}

        return header

    ## Create connector processor if it does not exists
    def createProcessorRun(self, ldif_processor, request_url, header, lix_api_token):
        self.data = {
            "connectorType": "SmartsheetIntegration",
            "connectorId": "lxSmartsheetInboundConnector",
            "connectorVersion": "1.0.0",
            "processingDirection": "inbound",
            "processingMode": "partial",
            "credentials": {
                "apiToken": lix_api_token
            },
            "variables": {
                "deploymentMaturity": {
                    "default": "0"
                }
            },
            "processors": ldif_processor['processors']
        }
        self.data = json.dumps(self.data)
        new_data = re.sub(r': True', ': true', self.data)
        response = requests.put(url=request_url + "configurations/", headers=header, data=new_data)

    ## Create connector with LDIF content
    def createRun(self, content, request_url, header):
        self.data = {
            "connectorType": "SmartsheetIntegration",
            "connectorId": "lxSmartsheetInboundConnector",
            "connectorVersion": "1.0.0",
            "lxVersion": "1.0.0",
            "description": "Creates LeanIX Projects from Smartsheet workspaces",
            "processingDirection": "inbound",
            "processingMode": "partial",
            "customFields": {},
            "content": content['content']
        }
        
        self.response = requests.post(url=request_url + "synchronizationRuns/", headers=header, data=json.dumps(self.data))
        return (self.response.json())

    ## Process data / load into LeanIX workspace
    def startRun(self, run, request_url, header):
        response = requests.post(url=request_url + "synchronizationRuns/" + run["id"] + "/start?test=false", headers=header)


if __name__ == "__main__":
    logging.info('----- Start -----')
    #### Get smartsheet data, transform to LDIF
    sh = smartsheetToLdif()
    ## get data from Smartsheet
    workspaces, sht_wkspc_map = sh.get_all_workspaces(sh.smart)
    all_sheets = sh.get_all_sheets(sh.smart,sht_wkspc_map)
    all_tasks = sh.get_sheet_data(sh.smart, all_sheets, config.field_mapper)
    ## transform data to LDIF
    ldif_output = sh.transform_to_ldif(sh.base_json, all_sheets, all_tasks, workspaces)
    logging.info('Trasformed data to LDIF.')
    logging.debug('LDIF: %s', str(ldif_output))

    #### send data to Lean IX workspace
    lx = ldifToWorkspace()
    logging.info('Begin data load into LeanIX iAPI.')
    lix_header = lx.createLeanixConnection(lx.lix_api_token, config.auth_url)
    lx.createProcessorRun(lx.ldif_processor, config.request_url, lix_header, lx.lix_api_token)
    run = lx.createRun(ldif_output, config.request_url, lix_header)
    lx.startRun(run, config.request_url, lix_header)
    logging.info('LDIF processed by LeanIX iAPI.')
    logging.info('----- End -----')

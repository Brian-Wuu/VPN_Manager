import pickle
import os
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

#coach: 14WKBpStX30TN5gKCHJQu9P270j6xDpFK

class Google_drive():
    def __init__(self) -> None:
        #Google Drive Api通过ID识别文件(文件夹), self.fold保存主文件夹id
        self.fold ={
            'fold_name' : ['coach', 'firstbase', 'secondbase','thirdbase','catcher''pitcher','shortstop','leftfield','centerfield','rightfield','designatedhitter'],
            'coach' : '14WKBpStX30TN5gKCHJQu9P270j6xDpFK',
            'firstbase' : '1RMBrxdmb50YTmTZpeETxBP-IgUpC_p2G',
            'secondbase' : '1TbTkIMsF5omDDPk9Pyapqa3VATYIw918',
            'thirdbase' : '1rzNXfv5agAx3TqVOizN9orp4f70b-KHk',
            'catcher' : '1f75hfO7NSZi_ByLN4maDW9UVjhrKO87H',
            'pitcher' : '1rnR8jPsnXB7vI4GfWQg-5yF5Fw8V5S4K',
            'shortstop' : '1wAlWDuvywnBdM8mju6bfd2b8uetC3jou',
            'leftfield' : '12kWYwsx4_Ugla498D3rvOR6AUthSmQmU',
            'centerfield' : '1_WN4IAsyl6ngh7otaxCDgg2EMOEwTj87',
            'rightfield' : '1s9ATb0flimCP5n-nPWTGYuTj4nMUpHTX',
            'designatedhitter' : '1y3n4yLDrju6txJ8Pueqlo0m3Zps0d2gk'
            }
        #Google Drive Api相关操作需通过SCOPES进行授权
        #token.pickle为相关授权凭证
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
                  'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/drive.file',
                  'https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive.appdata'
                  ]
        creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
        self.service = build('drive', 'v3', credentials=creds)
    
    def delete_drive_service_file(self, file_id):
        service = self.service
        service.files().delete(fileId=file_id).execute()

    def search_file(self, update_drive_service_name, drive_fold_id, is_delete_search_file=False) -> str:
        """
        本地端取得到云端名称, 可在下载时取得file id下载
        :param update_drive_service_name: 上传到云端的名称
        :param drive_fold_id:存到云端文件夹ID
        :param is_delete_search_file: 判断是否需要刪除文件
        """
        service = self.service
        results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                       q="name = '" + update_drive_service_name + "' and trashed = false and '" + drive_fold_id + "' in parents"
                                       ).execute()

        items = results.get('files', [])
        if items:
            for item in items:
                #print(u'{0} ({1})'.format(item['name'], item['id']))
                if is_delete_search_file is True:
                    self.delete_drive_service_file(file_id=item['id'])
                    return ''
                    
                else:
                    return item['id']

    def update_file(self, update_drive_service_name, local_file_path, drive_fold_id) -> None:
        """
        將本地端的文件上传到云端
        :param update_drive_service_name: 存到云端上得名称
        :param local_file_name: 本地端的文件名称
        :param local_file_path: 本地端的文件夹
        :param drive_fold_id:存到云端文件夹ID
        """
        service = self.service
        ###查看是否存在同名文件，若存在则删除
        self.search_file(update_drive_service_name, drive_fold_id, is_delete_search_file=True)
        file_metadata = {'name': update_drive_service_name,
                        'parents': [drive_fold_id]}
        media = MediaFileUpload(local_file_path, )
        file_metadata_size = media.size()
        #start = time.time()
        file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        #end = time.time()
        #print("上传文件成功！")
        #print('云端文件名称为: ' + str(file_metadata['name']))
        #print('云端文件ID为: ' + str(file_id['id']))
        #print('文件大小为: ' + str(file_metadata_size) + ' byte')
        #print("上传时间为: " + str(end-start))
        #return file_metadata['name'], file_id['id']
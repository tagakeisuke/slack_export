import os
import requests
import codecs
import datetime
import math
import csv
import json
import re
from dictknife import deepmerge

#user情報取得用  #Bot scope(users:read), User scope(users:read)
url_user = "https://slack.com/api/users.info" 

#channel取得用  #Bot scope(channels:read,groups:read,im:read,mpim:read), User scope(channels:read, groups:read, im:read, mpim:read)
url_ch = "https://slack.com/api/conversations.list" 

#メッセージ取得用   #Bot scope(channels:history, groups:history, im:history, mpim:history), User scope(channels:history, groups:history, im:history, mpim:history)
url_mg = "https://slack.com/api/conversations.history"
url_rp = "https://slack.com/api/conversations.replies" 

#ファイル取得用  #Bot scope(files:read), User scope(files:read)
url_fl = "https://slack.com/api/files.list" 


def channel_list(workspace,header):
    #チャンネル一覧の取得
    payload = {
                "types": "public_channel, private_channel, mpim,im",
                "exclude_archived":True
                }
    data = requests.get(url_ch, headers=header, params=payload).json()
    with open(f"{workspace}/channel_list.txt","w",encoding="utf-8") as list:
    #nameとidをchannellistに書き込み       
        for i in data["channels"]:
            if("name" in i):
                name=i["name"]
            else:
                user_id= i["user"]
                user_name=requests.get(url_user, headers=header, params={"user" : user_id}).json()
                name=user_name["user"]["profile"]["real_name"]
            id=i["id"]
            print(f"{name}\t{id}",file=list)
        print("EOF\tEOF",file=list)


def get_message(workspace,header):
    os.makedirs(f"{workspace}/csv", exist_ok=True)
    os.makedirs(f"{workspace}/json", exist_ok=True)
    print("メッセージ出力開始")
    with open(f"{workspace}/channel_list.txt","r",encoding="utf-8") as list:
        channel_name, channel_id = list.readline().replace("\n","").split("\t")
        while channel_name != "EOF":         
            print(f"{channel_name}：メッセージ出力中")
            payload  = {
                        "channel" : f"{channel_id}",
                        "include_all_metadata": True,
                        "limit"   : 200
                        }
            
            with open(f"./{workspace}/json/{channel_name}.json", 'w', encoding="utf-8") as json_file:  #json出力
                with open(f"./{workspace}/csv/{channel_name}.csv", 'w', encoding="utf_8_sig", newline="") as Csv:
                    j_mg={}
                    writer = csv.writer(Csv)
                    writer.writerow(["date", "user_name", "id", "message", "reply","files"])
                    has_more=True
                    while(has_more==True):
                        response = requests.get(url_mg, headers=header, params=payload)
                        res=response.json()
                        j_mg=deepmerge(j_mg,res)#json出力
                        for i in res["messages"]:
                            if "user" in i:
                                user_id=i["user"]
                                user_name=(requests.get(url_user, headers=header, params={"user" : user_id}).json())["user"]["name"]
                            elif "bot_id" in i:
                                user_id=i["bot_id"]
                                user_name=i.get("username", "")
                            else:
                                user_name=""
                            ts=i["ts"]
                            date=datetime.datetime.fromtimestamp(math.floor(float(ts)))
                            text=i["text"]
                            inputText=[date, user_name, user_id, text,""]
                            if("files" in i):
                                for f in i["files"]:
                                    inputText.append(f["id"]+"_"+f["title"])
                            writer.writerow(inputText)
                            if("thread_ts" in i):
                                th_ts=i["thread_ts"]
                                payload  = {
                                            "channel" : f"{channel_id}",
                                            "ts"   : th_ts
                                            }
                                reply=requests.get(url_rp, headers=header, params=payload)
                                rep=reply.json()
                                j_mg=deepmerge(j_mg,rep) #json出力
                                for j, r in enumerate(rep["messages"]):
                                    if(j!=0):
                                        if "user" in r:
                                            user_id=r["user"]
                                            user_name=(requests.get(url_user, headers=header, params={"user" : user_id}).json())["user"]["name"]
                                        elif "bot_id" in r:
                                            user_id=r["bot_id"]
                                            user_name=r.get("username", "")
                                        else:
                                            user_name=""
                                        date=datetime.datetime.fromtimestamp(math.floor(float(r["ts"])))
                                        text=r["text"]
                                        inputText=[date, user_name, user_id, "",text]
                                        if("files" in r):
                                            for f in r["files"]:
                                                if "title" in f:
                                                    inputText.append(f["title"])
                                                else:
                                                    inputText.append(f["file_not_found"])
                                        writer.writerow(inputText)

                        json.dump(j_mg,json_file)#json出力
                        if("response_metadata" in i):
                            next_cursor = i["response_metadata"]["next_cursor"]
                            payload  = {
                                        "channel" : f"{channel_id}",
                                        "include_all_metadata": True,
                                        "limit"   : 200,
                                        "cursor"  : next_cursor
                                        }
                            has_more = i["has_more"]
                        else:
                            has_more=False
            channel_name, channel_id = list.readline().replace("\n","").split("\t")
    print("出力完了")

def file_download(workspace,header):
    print("ダウンロード開始")
    with open(f"{workspace}/channel_list.txt","r",encoding="utf-8") as list:
        channel_name, channel_id = list.readline().replace("\n","").split("\t")
        while channel_name != "EOF":
            os.makedirs(f"{workspace}/files/{channel_name}", exist_ok=True)
            print(f"{channel_name}：ダウンロード開始")
            files = requests.get(url_fl, headers=header, params={"channel" : f"{channel_id}"}).json()
            for i in files["files"]:
                file_id=i["id"]
                file_name = re.sub(r'[\\/:*?"<>|]+', '-', i["name"])
                print(f"{file_name}：ダウンロード中")
                download_url = i["url_private"]
                data = requests.get(download_url,headers=header ,stream=True).content
                with codecs.open(f"./{workspace}/files/{channel_name}/{file_id}_{file_name}", mode="wb") as f:
                    f.write(data)
            print(f"{channel_name}：ダウンロード完了")
            channel_name, channel_id = list.readline().replace("\n","").split("\t")
    print("ダウンロード完了")

if __name__ == '__main__':
    workspace=input("workspace>>")
    os.makedirs(f"{workspace}", exist_ok=True)
    token=input("usertoken>>")
    header={"Authorization": "Bearer {}".format(token)}
    while(True):
        task=input("\"l\": create channel list,\"m\": export messages,\"f\": export files>>")
        if(task=="l"):
            channel_list(workspace=workspace, header=header)
        elif(task=="m"):
            get_message(workspace=workspace, header=header)
        elif(task=="f"):
            file_download(workspace=workspace, header=header)
        else:
            print("error: input \"l\", \"m\" or \"f\".")

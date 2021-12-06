import requests
import json
from flask import Flask,render_template,request,flash,redirect
from os import path

app=Flask(__name__)


def relation(id):
    url="https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3B%0Arel%28"+str(id)+"%29%3B%0Anode%28r%29%5Bpublic_transport~%22platform%7C%22%5D%3B%0Aout%20geom%3B"
    # url="https://overpass-api.de/api/interpreter?data=[out:json][timeout:25];relation(10831518);out%3Ebody;"


    op=json.loads(requests.get(url).text)["elements"]
    
    errNodeId=[]
    
    def checkTag(tags):
        
        onlineTag=[]
        tagTemplate=["public_transport","highway","bus","name","shelter"]
        for i in tags["tags"]:
            onlineTag.append(i)

        check=all(item in onlineTag for item in tagTemplate)
        if not check:
            # errNodeId tags["id"]
            return(tags["id"])
        
    for i in op:
        if checkTag(i) != None:
            errNodeId.append(checkTag(i))
    return errNodeId


# dictionary=dict op
print(relation(12))

# print(dictionary)
@app.route("/",methods=['POST','GET'])                #first line / represents the route dir 
def home():
    if request.method =='POST':
        relationIds=request.form.get('relation_id')
        errData=[]
        for g in relationIds.split(","):
            errData0=relation(g)
            print(errData0)
            for av in errData0:
            errData.append(av)
        if len(errData)>0:
            return(str(errData))
        else:
            return("Every this is fine")

    return render_template("home.html")        



if __name__ == "__main__":#check wether the ___name__ == __main__ conforming only devoloper can debug the code... if this command is not here anyone can access and debug the code..
    app.run()


# https://overpass-turbo.eu/s/1dKK

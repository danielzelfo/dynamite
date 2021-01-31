from flask import Flask, render_template, request, url_for
import os
import string
import random

app = Flask(__name__)




data = {

}

@app.route('/')
def index():
    page = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    data[page] = {
		"section-data": [
            {
                "type": "reading",
                "content": {}
            }
        
        
        ]
	}
    print(data)
    return render_template('index.html', page=page)   
    
    
@app.route('/page')
def render_page():

    current_page = request.args.get("page")

    render = "<!DOCTYPE html>\r\n<html>\r\n"
    render += "<head>\r\n<title>Page " + current_page + "</title>\r\n"
    
    render += "<style>h1, p, textarea, video{min-width: 50%} textarea{min-height: 50vh}</style></head>\r\n<body>"
    

    

    
    
    if not current_page in data:
        return "404 NOT FOUND"
    
    c_data = data[current_page]
    
    
    emptySections = True
    for section in c_data["section-data"]:
        if len(section["content"])  != 0:
            emptySections = False
            break
            
    if emptySections:
        return "EMPTY PAGE"
    
    
    
    for section in c_data["section-data"]:
    
        if len(section["content"]) == 0:
            continue
            
        content = {
            "reading": [ ["title", "h1", ""], ["text","p", ""]],
            "free": [["text", "h1", ""], ["", "textarea", ""]],
            "video": [["link", "video controls", "src"]]
        }
    
    
        render += "<div class='section'>\r\n"
        
        for x in content[section["type"]]:
            render+="<"+ x[1] 
            
            if x[2]!="":
                render+= " " + x[2] + "='" + section["content"][x[0]] + "'>"
            else:
                render += ">"
                if x[0]!="":
                    render+= section["content"][x[0]]
            
            render+="</"+ x[1].split()[0] +">\r\n"
        
        render += "</div>\r\n"
        
        
    render += "<button id='next'>next</button>\r\n"
    render += "</body>"
    
    with open("templates/includes/global_scripts.html") as jq:
        render += jq.read() + "\r\n"
    render+= "<script type='text/javascript' src="+ url_for('static', filename='render.js') +"></script>"
    
    render += "</html>"
    
    return render
   
@app.route('/addSection')
def background_process_add():
    page = request.args.get("pageID")

    sectionData = {
        "type": "reading",
        "content": {}
    }
    
    data[page]["section-data"].append(sectionData)
    
    
    print(data)
    return ""
    
    
@app.route('/changeSection')
def background_process_change():
    page = request.args.get("pageID")

    i = int(request.args.get("i"))
    typ = request.args.get("type")
    
    
    
    data[page]["section-data"][i]["type"] = typ
    
    
    print(data)
    with open("templates/includes/section-"+typ+".html") as f:
        return f.read()



@app.route('/saveSection')
def background_process_save():
    
    page = request.args.get("pageID")
    
    categorizedContent = {
        "reading": ["title", "text"],
        "free": ["text"],
	"video": ["link"]
    }


    i = int(request.args.get("i"))
    
    
    typ = request.args.get("type")
    
    content = {}
    
    
    for x in categorizedContent[typ]:
        content[x] = request.args.get("content["+x+"]")
    
    
    
    data[page]["section-data"][i]["content"] = content
    
    print(data)
    
    return ""
        
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')

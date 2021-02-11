from flask import Flask, render_template, request, url_for, Markup
import os
import string
import random
import html

os.chdir(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__)

data = {

}

#home page
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
    return render_template('index.html', page=page)   

#custom lesson page
@app.route('/page')
def render_page():

    current_page = request.args.get("page")
    c_data = data[current_page]
    render = ""
    color = "black"
    
    #404 Error
    if not current_page in data:
        return f'<p style="color: {color}">404 NOT FOUND</p>'
    
    #Checking if all there are no sections or all sections are empty
    emptySections = True
    for section in c_data["section-data"]:
        if len(section["content"])  != 0:
            emptySections = False
            break

    if emptySections:
        return f'<p style="color: {color}">EMPTY PAGE</p>'
    
    #rendering all sections
    for section in c_data["section-data"]:
        
        #skip empty
        if len(section["content"]) == 0:
            continue

        #content html data by type
        content = {
            "reading": [ ["title", "h1", ""], ["text","p", ""]],
            "free": [["text", "h1", ""], ["", "textarea class='contentInput'", ""]],
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

    with open("templates/includes/global_scripts.html") as jq:
        return render_template('lesson.html', current_page=current_page, sections=Markup(render), globalscripts=Markup(jq.read()))

#background process - add section
@app.route('/addSection')
def background_process_add():
    page = request.args.get("pageID")

    sectionData = {
        "type": "reading",
        "content": {}
    }

    data[page]["section-data"].append(sectionData)

    return ""

#background process - change section
@app.route('/changeSection')
def background_process_change():
    page = request.args.get("pageID")

    i = int(request.args.get("i"))
    typ = request.args.get("type")


    data[page]["section-data"][i]["type"] = typ

    with open("templates/includes/section-"+typ+".html") as f:
        return f.read()

#background process - save section
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
        content[x] = html.escape(request.args.get("content["+x+"]"))


    data[page]["section-data"][i]["content"] = content

    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0')

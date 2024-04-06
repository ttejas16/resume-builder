import os
import copy
import pdfkit
from resume_builder import app,db,WKHTML_PATH
from flask import render_template,request,Response
from bs4 import BeautifulSoup
from resume_builder.authentication import login_required
from resume_builder.models.Resume import Resume

config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)

basedir = os.path.abspath(os.path.dirname(__file__))

templatePaths = ["static/html/resume1.html","static/html/resume2.html","static/html/resume3.html"]
templates = {}

for index,path in enumerate(templatePaths):
    html = ""

    abs_path = os.path.join(basedir, path)
    with open(abs_path,encoding="utf-8") as fp:
        html = BeautifulSoup(fp,"html.parser")
    key = str(index + 1)
    templates[key] = html



def dict_to_array(D:dict):
    result = []
    # print(D)

    max_length = max(len(values) for values in D.values())

    for i in range(max_length):
        new_dict = {}

        for key,values in D.items():
            new_dict[key] = values[i]
        
        result.append(new_dict)
    
    return result


def generate_dictionary(raw_data):
    # dictionary format
    # {
    #     'resume-choice':'1|2|3|4|5',
    #     'personal':{},
    #     'education':[{ key->value},],
    #     'projects':[{ key->value},],
    #     'experience':[{ key->value},],
    #     'skill':[{ key->value},],
    #     'other':[{ key->value},]
    # }
    
    raw_dict = {}
    for item in raw_data:
        key = item[0]
        value = item[1]
        raw_dict[key] = value


    resume_fields = ["personal","education","project","experience","skill","other"]
    res = {}
    
    res["resume-choice"] = raw_dict["resume-choice"][0]
    res["submit"] = raw_dict["submit"][0]

    for field in resume_fields:
        field_data = {} 

        for key in raw_dict.keys():
            if field == "personal" and (field in key):
                field_data[key] = raw_dict[key][0]
            else:
                if field in key:
                    field_data[key] = raw_dict[key]

        if not field_data:
            res[field] = []
        else:
            if field == "personal":
                res[field] = field_data
            else:
                arr = dict_to_array(field_data)
                res[field] = arr


    return res           


def insert_into_template(resume_data:dict):
     # dictionary format
    # {
    #     'resume-choice':'1|2|3|4|5',
    #     'submit':'preview'|'submit'
    #     'personal':{ key -> values },
    # 
    #     'education':[{ key -> value },... ],
    #     'projects':[{ key -> value},... ],
    #     'experience':[{ key -> value},... ],
    #     'skill':[{ key -> value},... ],
    #     'other':[{ key -> value},... ]
    # }

    choice = resume_data["resume-choice"]
    template_string:BeautifulSoup = copy.deepcopy(templates[choice])
    
    # print(template_string.prettify())

    for key,data_values in resume_data.items():

        if key == "personal":
            for k,v in data_values.items():
                element = template_string.find(id = k)
                if (not v) and element:
                    element.extract()

                if v and element:

                    if "link" in k:
                        element["href"] = v
                        element.string = k[k.find("-") + 1:]
                    else:
                        element.string = v

        else:
            if len(data_values) == 0:
                container = template_string.find(id = key);
                if container:
                    container.extract()
                continue

            wrapper = template_string.find(id = f"{key}-wrapper")
            item = template_string.find(id = f"{key}-item")

            if wrapper and item:
                wrapper.string = ""

                for data_item in data_values:
                    item_copy = copy.deepcopy(item)

                    for k,v in data_item.items():
                        elem = item_copy.find(id=k)
                        if (not v) and elem:
                            elem.extract()

                        if v and elem:

                            if "link" in k:
                                elem["href"] = v
                                elem.string = k[k.find("-") + 1:]
                            else:
                                elem.string = v

                    wrapper.append(item_copy)

    return template_string



                

@app.get("/create")
@login_required
def resume_form():
    return render_template("create.html")

@app.post("/create")
@login_required
def create_resume():
    
    resume_data = generate_dictionary(request.form.lists())
    result = insert_into_template(resume_data)

    if resume_data["submit"] == "preview":
        
        resume = Resume.query.first()
        resume.resume_created = Resume.resume_created + 1
        db.session.commit()

        return render_template('preview.html',html = result)
    else:
        options = {
            'page-width': '210mm',
            'page-width': '297mm',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
        }
        pdf = pdfkit.from_string(str(result),configuration=config,options=options)
        response = Response(pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
        
        resume = Resume.query.first()
        resume.resume_downloaded = Resume.resume_downloaded + 1
        db.session.commit()

        return response




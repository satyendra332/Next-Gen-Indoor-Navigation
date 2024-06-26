import json

from main import app
from flask import request
from DBMS import datahandler
from MallGraph.PathDrawer import Drawer
from MallGraph.Graph import generate_random_string, MakeGraph

def arrange_values(values):
    arranged_values = dict()

    for value in values:
        x, y, z = value

        if z in arranged_values:
            arranged_values[z].append((x, y, z))
        else:
            arranged_values[z] = [(x, y, z)]

    return json.dumps(arranged_values)

@app.route("/getPath", methods=["GET", "POST"])
def getPath():
    if request.method == "POST":
        start = request.form.get("start")
        destination = request.form.get("destination")
        step1 = MakeGraph()
        step1.create_connections()
        values = step1.find_path(start, destination)
        _ = generate_random_string(10) + ".png"
        arranged_values_json = json.loads(arrange_values(values))
        file_pool = list()

        for _ in arranged_values_json:
            filename = generate_random_string(10) + ".png"
            file_pool.append(filename)
        
        step2 = Drawer()
        length = len(file_pool)

        if length == 1:
            if "1" in arranged_values_json:
                step2.draw_for_floor_1(file_pool[0], arranged_values_json["1"], start=True, end=True)
                file_pool.append("public/2.png")
                file_pool.append("public/3.png")

            if "2" in arranged_values_json:
                var = file_pool[0]
                step2.draw_for_floor_2(var, arranged_values_json["2"], start=True, end=True)
                file_pool = list()
                file_pool.append("public/1.png")
                file_pool.append(var)
                file_pool.append("public/3.png")
                
            if "3" in arranged_values_json:
                var = file_pool[0]
                step2.draw_for_floor_3(var, arranged_values_json["3"], start=True, end=True)
                file_pool = list()
                file_pool.append("public/1.png")
                file_pool.append("public/2.png")
                file_pool.append(var)

        if length == 2:
            if '1' in arranged_values_json and '2' in arranged_values_json:
                if values[0][0]==arranged_values_json["1"][0][0] and values[0][1]==arranged_values_json["1"][0][1] and values[0][2]==arranged_values_json["1"][0][2]:

                    step2.draw_for_floor_1(file_pool[0], arranged_values_json["1"],start=True)
                    step2.draw_for_floor_2(file_pool[1], arranged_values_json["2"],end=True)
                    file_pool.append("public/3.png")
                else:
                    step2.draw_for_floor_1(file_pool[0], arranged_values_json["1"],end=True)
                    step2.draw_for_floor_2(file_pool[1], arranged_values_json["2"],start=True)
                    file_pool.append("public/3.png")
                
            if '2' in arranged_values_json and '3' in arranged_values_json:

                if values[0][0]==arranged_values_json["2"][0][0] and values[0][1]==arranged_values_json["2"][0][1] and values[0][2]==arranged_values_json["2"][0][2]:

                    var = file_pool[0]
                    var1 = file_pool[1]
                    step2.draw_for_floor_2(file_pool[0], arranged_values_json["2"],start=True)
                    step2.draw_for_floor_3(file_pool[1], arranged_values_json["3"],end=True)
                    file_pool = list()
                    file_pool.append("public/1.png")
                    file_pool.append(var)
                    file_pool.append(var1)
                else:
                    var = file_pool[0]
                    var1 = file_pool[1]
                    step2.draw_for_floor_2(file_pool[0], arranged_values_json["2"],end=True)
                    step2.draw_for_floor_3(file_pool[1], arranged_values_json["3"],start=True)
                    file_pool = list()
                    file_pool.append("public/1.png")
                    file_pool.append(var)
                    file_pool.append(var1)
        
        if length == 3:
            if values[0][0]==arranged_values_json["1"][0][0] and values[0][1]==arranged_values_json["1"][0][1] and values[0][2]==arranged_values_json["1"][0][2]:
                step2.draw_for_floor_1(file_pool[0], arranged_values_json["1"],start=True)
                step2.draw_for_floor_2(file_pool[1], arranged_values_json["2"])
                step2.draw_for_floor_3(file_pool[2], arranged_values_json["3"],end=True)
            else:
                step2.draw_for_floor_1(file_pool[0], arranged_values_json["1"],end=True)
                step2.draw_for_floor_2(file_pool[1], arranged_values_json["2"])
                step2.draw_for_floor_3(file_pool[2], arranged_values_json["3"],start=True)
        temp=datahandler.read_user(place=destination)
        similar=datahandler.get_locations_by_category(temp[0][2])
        average_speed = 150  # average speed in units per minute
        average_time = step1.calculate_average_time(start, destination, average_speed)
        average_time = round(average_time, 2)  

        return {
            "status": "ok",
            "1": {"img": "/static/" + file_pool[0], "floor": "1"},
            "2": {"img": "/static/" + file_pool[1], "floor": "2"},
            "3": {"img": "/static/" + file_pool[2], "floor": "3"},
            "similar": similar,
            "time":average_time,
        }, 200
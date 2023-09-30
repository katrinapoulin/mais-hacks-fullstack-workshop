from nicegui import ui
import requests
from datetime import date

def get_coffee():
    return requests.get("http://localhost:8000/coffee/").json()

def add_coffee(bean_name: str, description:str, roasted_on: date):
    return requests.post("http://localhost:8000/coffee/",
                         json={
                            "bean_name": bean_name,
                            "description": description,
                            "roasted_on": roasted_on
                        }).json()["status"]

def upload_image(bean_name, image):
    return requests.post(f"http://localhost:8000/coffee/upload/{bean_name}", 
                         files={"upload_file": image}).json()["status"]

input_bean_name = {"value": ""}
input_roasted_on = {"value": ""}
input_description = {"value": ""}
input_file = {"value": None}

ui.input(label='Bean name' ).bind_value_to(input_bean_name)
ui.input(label='Description').bind_value_to(input_description)
ui.label("Roasted on:")
ui.date(value='2023-01-01').bind_value_to(input_roasted_on)
ui.upload(on_upload=lambda e: ui.notify(upload_image(bean_name=input_bean_name['value'], image=e.content)))

ui.button('Submit', on_click=lambda: ui.notify(add_coffee(
    bean_name=input_bean_name['value'],
    roasted_on=input_roasted_on['value'], 
    description=input_description['value']
)))

ui.run()
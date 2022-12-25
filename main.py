import dearpygui.dearpygui as dpg
import math
from numpy.random import normal
import time

max_value = 480
angle_width = 180
divisions = 6
size = 18
interval = 1
cash = []
start = time.time()

def set_interval(_, app_data):
    global interval
    interval = int(app_data)

dpg.create_context()

# загрузка фона
width, height, channels, data = dpg.load_image('nekotach.png')

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, tag='nekotach')

with dpg.window(label='Voltmeter Window'):

    # рисуем фон
    with dpg.drawlist(width=width, height=height, tag='gauge'):
        with dpg.draw_node(tag='analog'):
            dpg.draw_image('nekotach', (0, 0), (width, height))
            # dpg.draw_line((width/2, height/2), (width/2, 30), color=(255, 255, 255, 127.5), thickness=10)

            for i in range(divisions+1):
                rad = (math.pi/180)*(angle_width/divisions)*i + math.pi/2
                val = (max_value/divisions)*i

                x = (width/2-30)*math.cos(rad) + width/2
                y = (height/2-30)*math.sin(rad) + height/2

                x1 = (width/2-5)*math.cos(rad) + width/2
                y1 = (height/2-5)*math.sin(rad) + height/2

                dpg.draw_line((x, y), (x1, y1), color=(100, 0, 0, 255), thickness=5)
                dpg.draw_text((x,y-size/2), int(val), size=size, color=(20, 50, 255, 255))
            
    dpg.add_combo([1, 3, 5, 10], callback=set_interval, label="interval (in seconds)", width=width/4, default_value=1)

def update_hand(val):
    dpg.delete_item('hand')
    rad = (math.pi/180)*angle_width*(val/max_value) + math.pi/2
    x = (width/2-30)*math.cos(rad) + width/2
    y = (height/2-30)*math.sin(rad) + height/2
    dpg.draw_line((width/2, height/2), (x, y), color=(200, 200, 200, 200), thickness=10, tag='hand', parent='analog')

def update_digits(val):
    dpg.delete_item('digits')
    dpg.draw_text((width/2, height/2), val, size=size*2, color=(20, 50, 255, 255), tag='digits', parent='analog')

dpg.create_viewport(title='Voltmeter Viewport', width=400, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    val = normal(max_value/2, max_value/divisions)
    update_hand(val)
    cash.append(val)

    if time.time() - start >= interval:
        start = time.time()
        if len(cash) > 0:
            update_digits(sum(cash)/len(cash))
            cash = []

    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()
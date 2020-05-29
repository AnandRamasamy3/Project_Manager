import pygame,sys,time,math,threading,os
from pygame.locals import *
import sqlite3
import json
import datetime

pygame.init()
WIDTH,HEIGHT=1220,670
surface=pygame.display.set_mode((WIDTH,HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Project manager')

title_font=pygame.font.SysFont("Times New Roman",31,bold=False,italic=False)
text_font=pygame.font.SysFont("Calibri",19,bold=False,italic=False)




class curves:
    def __init__(self,x=0,y=0):
        pass
    def midpoint(self,p1,p2,T,t):
        result=[0,0]
        result[0]=p1[0]+((p2[0]-p1[0])/T)*t
        result[1]=p1[1]+((p2[1]-p1[1])/T)*t
        return result
    def make_(self,points,T,t):
        if len(points)==2:
            return self.midpoint(points[0],points[1],T,t)
        new_points=[]
        for point_index in range(len(points)-1):
            mid_=self.midpoint(points[point_index],points[point_index+1],T,t)
            new_points.append(mid_)
        return self.make_(new_points,T,t)
    def find_curve(self,points,T=10):
        curve=[points[0]]
        t=1
        while t<T:
            new_points=self.make_(points,T,t)
            curve.append(new_points)
            t+=1
        curve.append(points[-1])
        return curve

# points=[
#     (100,480),
#     (100,80),
#     (600,480),
#     (800,80)
# ]
#
# curve=curves()
# result=curve.find_curve(points,T=100)
#
# print (result)


class Main:
    def __init__(self,surface):
        self.surface=surface
        self.database={}
        self.User_Name=""
        self.get_database()
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.get_colors()
        self.default_font_title_size=21
        self.default_font_text_size=17
        self.months_list=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.menu_bar_size=40
        self.height_for_a_task_bar_line=25
        self.bar_buttons={}
        self.column_delete_buttons={}
        self.column_minimize_buttons={}
        self.column_move_left_buttons={}
        self.column_move_right_buttons={}
        self.task_minimize_buttons=[]
        self.task_delete_buttons=[]
        self.column_title_text_cards={}
        self.task_title_text_cards=[]
        self.task_description_text_cards=[]
        self.task_cards_for_selection={}
        self.task_move_left_buttons=[]
        self.task_move_right_buttons=[]
        self.add_task_buttons={}
        self.last_showable_column=0
        self.last_button_clicked=time.time()
        self.last_text_card_clicked=time.time()
        self.font_family="Menlo, Consolas, DejaVu Sans Mono, monospace"
        self.text=""
        self.most_number_of_columns=5
        self.active={
            "column":None,
            "task":None,
            "title_or_Description":None
        }
        self.input_text_enabled=False
        self.input_text=""
        self.input_text_target=None
        self.current_cursor_position={}
    def calculate_basic_metrices(self):
        pass
        self.showable_columns=[]
        self.bar_columns=[]
        self.width_for_add_column=0
        for column_index in range(len(self.database)):
            if self.database[column_index]["minimized"]=="False":
                self.showable_columns.append(column_index)
                if column_index not in self.current_cursor_position:
                    self.current_cursor_position.update({column_index:0})
            else:
                self.bar_columns.append(column_index)
        # print (len(self.database))
        # self.unit_width_for_column=WIDTH-self.width_for_add_column
        # if len(self.database)<6:
        #     self.width_for_add_column=100
        #     self.unit_width_for_column=WIDTH-self.width_for_add_column
        # elif len(self.showable_columns)>0:
        #     self.unit_width_for_column=int((WIDTH-self.width_for_add_column)/len(self.showable_columns))
        # else:
        #     self.unit_width_for_column=WIDTH-self.width_for_add_column
        # print (len(self.database),len(self.showable_columns),self.unit_width_for_column,len(self.bar_columns),self.width_for_add_column)
        # print (len(self.bar_columns))
        if len(self.database)==0:
            self.width_for_add_column=WIDTH*7//8
            self.unit_width_for_column=0
        elif len(self.showable_columns)==0:
            self.width_for_add_column=0
            self.unit_width_for_column=0
        else:
            if len(self.database)<self.most_number_of_columns:
                self.width_for_add_column=int(WIDTH/(len(self.showable_columns)+1))
                self.unit_width_for_column=int(WIDTH/(len(self.showable_columns)+1))
            else:
                self.width_for_add_column=0
                self.unit_width_for_column=int(WIDTH/len(self.showable_columns))
    def get_database(self):
        fobj=open("src/database.json",)
        temp=json.load(fobj)
        self.User_Name=temp["User_Name"]
        self.database=temp["database"]
        fobj.close()
    def get_colors(self):
        fobj=open("src/colors.json",)
        self.color=json.load(fobj)
        fobj.close()
    def update_database_in_file(self):
        pass
        fobj=open("src/database.json","w")
        # fobj.write()
        final_database={
          "User_Name":"Anand Ramasamy",
          "database":self.database
        }
        json.dump(final_database,fobj)
        fobj.close()
    def get_apt_message(self,message,length=26):
        result=[""]
        mess=message
        # print ("\n\n\n",len(message))
        # print (message)
        # print (length)
        message=message.split(" ",)
        # print (message)
        # print (length)
        while len(message)>0:
            if len(result[-1])<length:
                if (len(result[-1])+len(message[0]))<length:
                    result[-1]+=" "+message[0]
                    message.remove(message[0])
                elif len(result[-1])<(length/2):
                    # print (result)
                    rem_length=length-len(result[-1])-1
                    result[-1]+=" "+message[0][0:rem_length]
                    message[0]=message[0].replace(message[0][0:rem_length],"")
                else:
                    result.append("")
            else:
                result.append("")
        return result
    def set_database(self):
        with open("src/database.json","w") as fobj:
            # json.dump(self.database,fobj)
            pass
    def euclidean_distance(self,point_1,point_2):
        point=math.sqrt( ((point_1[0]-point_2[0])**2)+((point_1[1]-point_2[1])**2) )
        return point
    def manage_text_cards(self):
        # return None
        if self.click[0]==1 and time.time()>=self.last_text_card_clicked+0.3:
            self.last_text_card_clicked=time.time()
            for column_index in self.column_title_text_cards:
                # print (self.column_title_text_cards[column_index]["x"])
                if self.column_title_text_cards[column_index]["x"]<=self.mouse[0]<=self.column_title_text_cards[column_index]["x"]+self.column_title_text_cards[column_index]["width"] and self.column_title_text_cards[column_index]["y"]<=self.mouse[1]<=self.column_title_text_cards[column_index]["y"]+self.column_title_text_cards[column_index]["height"]:
                    print (self.database[column_index]["title"])
                    self.active["column"]=column_index
                    self.active["task"]=None
                    self.active["title_or_Description"]="title"
                    return None
            for column_task in self.task_title_text_cards:
                if column_task["x"]<=self.mouse[0]<=column_task["x"]+column_task["width"] and column_task["y"]<=self.mouse[1]<=column_task["y"]+column_task["height"]:
                    self.active["column"]=column_task["column"]
                    self.active["task"]=column_task["task"]
                    self.active["title_or_Description"]="Description"
                    # print ("got here")
                    return None
            for column_task in self.task_description_text_cards:
                if column_task["x"]<=self.mouse[0]<=column_task["x"]+column_task["width"] and column_task["y"]<=self.mouse[1]<=column_task["y"]+column_task["height"]:
                    # print ("hahahaha")
                    self.active["column"]=column_task["column"]
                    self.active["task"]=column_task["task"]
                    self.active["title_or_Description"]="Description"
                    return None
    def manage_buttons(self):
        # point_1=(bar_x,(self.menu_bar_size//2)+5)
        # print (self.euclidean_distance(point_1,self.mouse)<=self.menu_bar_size//2)
        if self.click[0]==1 and time.time()>=self.last_button_clicked+0.3:
            self.last_button_clicked=time.time()
            for column_pos in self.bar_buttons:
                # print (self.bar_buttons[column_pos])
                point=(self.bar_buttons[column_pos]["x"],self.bar_buttons[column_pos]["y"])#self.bar_buttons[]
                if self.euclidean_distance(point,self.mouse)<=self.bar_buttons[column_pos]["radius"]:
                    # print (column_pos,self.last_showable_column)
                    # self.database[self.last_showable_column]["minimized"]="True"
                    # print (column_pos)
                    self.database[column_pos]["minimized"]="False"
                    # print (self.database[self.last_showable_column]["minimized"],self.database[column_pos]["minimized"])
                    return None
            for column_pos in self.column_delete_buttons:
                point=(self.column_delete_buttons[column_pos],65)
                if self.euclidean_distance(point,self.mouse)<=10:
                    # print (self.database[column_pos]["title"])
                    # self.database.pop(column_pos)
                    self.database.remove(self.database[column_pos])
                    return None
            for column_pos in self.column_minimize_buttons:
                point=(self.column_minimize_buttons[column_pos],65)
                if self.euclidean_distance(point,self.mouse)<=10:
                    # print (column_pos,"minimized")
                    self.database[column_pos]["minimized"]="True"
                    return None
            for column_pos in self.column_move_left_buttons:
                point=(self.column_move_left_buttons[column_pos],65)
                if self.euclidean_distance(point,self.mouse)<=10:
                    # print (column_pos,"left moved")
                    # print (self.showable_columns,column_pos)#self.showable_columns.index(column_pos))
                    self.database[column_pos],self.database[column_pos-1]=self.database[column_pos-1],self.database[column_pos]
                    return None
            for column_pos in self.column_move_right_buttons:
                point=(self.column_move_right_buttons[column_pos],65)
                if self.euclidean_distance(point,self.mouse)<=10:
                    # print (column_pos,"right moved")
                    self.database[column_pos],self.database[column_pos+1]=self.database[column_pos+1],self.database[column_pos]
                    return None
            for task_pos in self.task_minimize_buttons:
                # print (task_pos["column"])
                # print (task_pos["task"])
                point=(task_pos["x"],task_pos["y"])
                # print (point,self.mouse)
                if self.euclidean_distance(point,self.mouse)<=5:
                    # print (task_pos,"minimized")
                    if self.database[task_pos["column"]]["tasks"][task_pos["task"]]["minimized"]=="False":
                        self.database[task_pos["column"]]["tasks"][task_pos["task"]]["minimized"]="True"
                    elif self.database[task_pos["column"]]["tasks"][task_pos["task"]]["minimized"]=="True":
                        self.database[task_pos["column"]]["tasks"][task_pos["task"]]["minimized"]="False"
                #     self.database[column_pos],self.database[column_pos+1]=self.database[column_pos+1],self.database[column_pos]
                    return None
            for task_pos in self.task_delete_buttons:
                point=(task_pos["x"],task_pos["y"])
                if self.euclidean_distance(point,self.mouse)<=5:
                    # self.database[task_pos["column"]]["tasks"][task_pos["task"]]["minimized"]="False"
                    # print (self.database[task_pos["column"]]["tasks"])
                    del self.database[task_pos["column"]]["tasks"][task_pos["task"]]
                    return None
            for column in self.task_move_right_buttons:
                point=(column["x"],column["y"])
                if self.euclidean_distance(point,self.mouse)<=5:
                    next_index_in_showable=self.showable_columns[self.showable_columns.index(column["column"])+1]
                    self.database[next_index_in_showable]["tasks"].update({
                        column["task"]:self.database[column["column"]]["tasks"][column["task"]]
                    })
                    del self.database[column["column"]]["tasks"][column["task"]]
                    return None
            for column in self.task_move_left_buttons:
                point=(column["x"],column["y"])
                if self.euclidean_distance(point,self.mouse)<=5:
                    previous_index_in_showable=self.showable_columns[self.showable_columns.index(column["column"])-1]
                    self.database[previous_index_in_showable]["tasks"].update({
                        column["task"]:self.database[column["column"]]["tasks"][column["task"]]
                    })
                    del self.database[column["column"]]["tasks"][column["task"]]
                    return None
            for column in self.add_task_buttons:
                if self.add_task_buttons[column]["x"]<=self.mouse[0]<=self.add_task_buttons[column]["x"]+self.add_task_buttons[column]["width"] and self.add_task_buttons[column]["y"]<=self.mouse[1]<=self.add_task_buttons[column]["y"]+self.add_task_buttons[column]["height"]:
                    # print (column)
                    # date_=str(datetime.datetime.now()).split(" ",)[0].split("-",)+str(datetime.datetime.now()).split(" ",)[1].split(":",)[:-1]+[str(datetime.datetime.now()).split(" ",)[1].split(":",)[2].split(".",)[0]]
                    # for task in self.database[column]["tasks"]:
                    #     print (task)
                    # for task in self.database[column]["tasks"]:
                    #     print (task)
                    self.input_text_enabled=True
                    self.input_text_target=column
                    pass
            if WIDTH-self.width_for_add_column<=self.mouse[0]<=WIDTH and 50<=self.mouse[1]<=HEIGHT:
                # print ("ooops")
                if len(self.database)<6:
                    self.database.append({
                            "title":"New One",
                            "minimized":"False",
                            "tasks":{}
                            })
    def draw_curve_boxes(self,x=0,y=0,width=0,height=0,thickness=1,fill=False,radius=15,color=None,curve_accuracy=30):#25
        if color==None:
            color=self.color["border_lines"]
        fill_points=[]
        # draw full box
        # pygame.draw.rect(self.surface,self.color["border_lines"],(x,y,width,height),1)
        x1,x2=x+radius,x+width-radius
        y1,y2=y+radius,y+height-radius
        pygame.draw.line(self.surface,color,(x1,y1-radius),(x2,y1-radius),thickness)
        pygame.draw.line(self.surface,color,(x1-radius,y1),(x1-radius,y2),thickness)
        pygame.draw.line(self.surface,color,(x2+radius,y1),(x2+radius,y2),thickness)
        pygame.draw.line(self.surface,color,(x1,y2+radius),(x2,y2+radius),thickness)
        # curve left top
        left_top_points=[
        (x1-radius,y1),
        (x1-radius,y1-radius),
        (x1,y1-radius)
        ]
        curve=curves()
        result=curve.find_curve(left_top_points,T=curve_accuracy)
        for point in result:
            # self.surface.set_at((int(point[0]),int(point[1])),self.color["border_lines"])
            pygame.draw.rect(self.surface,color,(int(point[0]),int(point[1]),thickness,thickness))
        # curve right top
        right_top_points=[
        (x2,y1-radius),
        (x2+radius,y1-radius),
        (x2+radius,y1)
        ]
        curve=curves()
        result=curve.find_curve(right_top_points,T=curve_accuracy)
        for point in result:
            # self.surface.set_at((int(point[0]),int(point[1])),self.color["border_lines"])
            pygame.draw.rect(self.surface,color,(int(point[0]),int(point[1]),thickness,thickness))
        # curve left bottom
        left_bottom_points=[
        (x1-radius,y2),
        (x1-radius,y2+radius),
        (x1,y2+radius)
        ]
        curve=curves()
        result=curve.find_curve(left_bottom_points,T=curve_accuracy)
        for point in result:
            # self.surface.set_at((int(point[0]),int(point[1])),self.color["border_lines"])
            pygame.draw.rect(self.surface,color,(int(point[0]),int(point[1]),thickness,thickness))
        # curve right bottom
        right_bottom_points=[
        (x2+radius,y2),
        (x2+radius,y2+radius),
        (x2,y2+radius)
        ]
        curve=curves()
        result=curve.find_curve(right_bottom_points,T=curve_accuracy)
        for point in result:
            # self.surface.set_at((int(point[0]),int(point[1])),self.color["border_lines"])
            pygame.draw.rect(self.surface,color,(int(point[0]),int(point[1]),thickness,thickness))
        left_bottom_points.reverse()
        fill_points+=left_top_points
        fill_points+=right_top_points
        fill_points+=right_bottom_points
        fill_points+=left_bottom_points
        if fill:
            pygame.draw.polygon(self.surface,color,fill_points)
    def paint(self):
        # full box
        # pygame.draw.rect(self.surface,self.color["border_lines"],(0,0,WIDTH,HEIGHT),1)
        self.draw_curve_boxes(0,0,WIDTH-1,HEIGHT-1)
        # menu box
        # pygame.draw.line(self.surface,self.color["border_lines"],(0,50),(WIDTH,50),1)
        self.draw_curve_boxes(0,0,WIDTH-1,50)
        # User_Name
        temp_font=pygame.font.SysFont(self.font_family,self.default_font_title_size,bold=False,italic=False)
        object_name_text_bottom=temp_font.render(self.User_Name,False,self.color["User_Name"])
        self.surface.blit(object_name_text_bottom,(10,10))
        # main menu
        pass
        # columns
        column_x=0
        self.bar_buttons={}
        self.column_delete_buttons={}
        self.column_minimize_buttons={}
        self.column_move_left_buttons={}
        self.column_move_right_buttons={}
        self.task_minimize_buttons=[]
        self.task_delete_buttons=[]
        self.column_title_text_cards={}
        self.task_title_text_cards=[]
        self.task_description_text_cards=[]
        self.task_move_left_buttons=[]
        self.task_move_right_buttons=[]
        self.add_task_buttons={}
        bar_x=WIDTH-(len(self.bar_columns)*self.menu_bar_size)-20
        for column in self.database:
            pass
            if column["minimized"]=="False":
                # print (self.database.index(column),"=",column_x,end=" ")
                # column full box
                # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x,50,self.unit_width_for_column,HEIGHT-50),1)
                self.draw_curve_boxes(column_x,50,self.unit_width_for_column,HEIGHT-50)
                # column title box
                # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x,50,self.unit_width_for_column,30),1)
                self.draw_curve_boxes(column_x,50,self.unit_width_for_column,30)
                self.column_title_text_cards.update({
                    self.database.index(column):{
                        "x":column_x,
                        "y":50,
                        "width":self.unit_width_for_column-100,
                        "height":30
                    }
                })
                # column title
                temp_font=pygame.font.SysFont(self.font_family,self.default_font_title_size*3//4,bold=False,italic=False)
                object_name_text_bottom=temp_font.render(column["title"][:10],False,self.color["column_title"])
                self.surface.blit(object_name_text_bottom,(column_x+10,60))
                # tasks
                y_cursor_init=y_cursor=80-self.current_cursor_position[self.database.index(column)]
                for task in column["tasks"]:
                    characters_allowed_on_a_line=int(((self.unit_width_for_column-50)/self.default_font_text_size*3//4)*3)
                    message=self.get_apt_message(column["tasks"][task]["Description"],length=characters_allowed_on_a_line)
                    y_cursor+=self.height_for_a_task_bar_line
                    # task title
                    temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*3//4,bold=False,italic=False)
                    object_name_text_bottom=temp_font.render(task[:17],False,self.color["task_title"])
                    self.surface.blit(object_name_text_bottom,(column_x+30,y_cursor+5))
                    # for header full box
                    if self.active["column"]==self.database.index(column) and self.active["task"]==task:
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,20),3)
                        self.draw_curve_boxes(column_x+20,y_cursor,self.unit_width_for_column-50,self.height_for_a_task_bar_line,thickness=2)
                    else:
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,20),1)
                        self.draw_curve_boxes(column_x+20,y_cursor,self.unit_width_for_column-50,self.height_for_a_task_bar_line)
                    self.task_title_text_cards.append({
                        "column":self.database.index(column),
                        "task":task,
                        "x":column_x+20,
                        "y":y_cursor,
                        "width":self.unit_width_for_column-50,
                        "height":20
                    })
                    # for header delete button
                    pygame.draw.circle(self.surface,self.color["delete_buttons"],(column_x+self.unit_width_for_column-40,y_cursor+10),5)
                    self.task_delete_buttons.append({
                        "column":self.database.index(column),
                        "task":task,
                        "x":column_x+self.unit_width_for_column-40,
                        "y":y_cursor+10
                    })
                    # for header minimize button
                    pygame.draw.circle(self.surface,self.color["minimize_button"],(column_x+self.unit_width_for_column-85,y_cursor+10),5)
                    self.task_minimize_buttons.append({
                        "column":self.database.index(column),
                        "task":task,
                        "x":column_x+self.unit_width_for_column-85,
                        "y":y_cursor+10
                    })
                    # for move right button
                    if self.database.index(column)!=self.showable_columns[-1]:
                        pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-55,y_cursor+10),5)
                        self.task_move_right_buttons.append({
                            "column":self.database.index(column),
                            "task":task,
                            "x":column_x+self.unit_width_for_column-55,
                            "y":y_cursor+10
                        })
                    pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-55,y_cursor+10),5,1)
                    # for move left button
                    if self.database.index(column)!=self.showable_columns[0]:
                        pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,y_cursor+10),5)
                        self.task_move_left_buttons.append({
                            "column":self.database.index(column),
                            "task":task,
                            "x":column_x+self.unit_width_for_column-70,
                            "y":y_cursor+10
                        })
                    pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,y_cursor+10),5,1)
                    if column["tasks"][task]["minimized"]=="False":
                        # for lines of task
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,(len(message)*20)+20),1)
                        self.draw_curve_boxes(column_x+20,y_cursor+self.height_for_a_task_bar_line,self.unit_width_for_column-50,(len(message)*self.height_for_a_task_bar_line))
                        self.task_description_text_cards.append({
                            "column":self.database.index(column),
                            "task":task,
                            "x":column_x+20,
                            "y":y_cursor,
                            "width":self.unit_width_for_column-50,
                            "height":(len(message)*self.height_for_a_task_bar_line)+self.height_for_a_task_bar_line
                        })
                        # for footer
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,(len(message)*20)+20+20),1)
                        self.draw_curve_boxes(column_x+20,y_cursor+(len(message)*self.height_for_a_task_bar_line)+self.height_for_a_task_bar_line,self.unit_width_for_column-50,self.height_for_a_task_bar_line)
                        for line in message:
                            y_cursor+=self.height_for_a_task_bar_line
                            temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*3//4,bold=False,italic=False)
                            object_name_text_bottom=temp_font.render(line,False,self.color["task_description"])
                            self.surface.blit(object_name_text_bottom,(column_x+30,y_cursor+5))
                            pass
                    else:
                        # for lines of task
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,20),1)
                        self.draw_curve_boxes(column_x+20,y_cursor,self.unit_width_for_column-50,self.height_for_a_task_bar_line)
                        # for footer
                        # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,20+20),1)
                        self.draw_curve_boxes(column_x+20,y_cursor+self.height_for_a_task_bar_line,self.unit_width_for_column-50,self.height_for_a_task_bar_line)
                    # for footer
                    y_cursor+=self.height_for_a_task_bar_line
                    footer_text=str(column["tasks"][task]["time"]["date"])+" "+str(self.months_list[column["tasks"][task]["time"]["month"]-1])+" "+str(column["tasks"][task]["time"]["year"])+" "+str(column["tasks"][task]["time"]["day"])+" "+str(column["tasks"][task]["time"]["hour"])+":"+str(column["tasks"][task]["time"]["minute"])+":"+str(column["tasks"][task]["time"]["second"])
                    temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*3//4,bold=False,italic=False)
                    object_name_text_bottom=temp_font.render(footer_text,False,self.color["task_time"])
                    self.surface.blit(object_name_text_bottom,(column_x+30,y_cursor+5))
                    # for extra space
                    y_cursor+=self.height_for_a_task_bar_line
                    # # save time by not allowing cursor to print on out of the screen
                    # if y_cursor>700:
                    #     # print (task)
                    #     break
                y_cursor+=self.height_for_a_task_bar_line
                # ask for adding new task
                # add task box
                # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x+20,y_cursor,self.unit_width_for_column-50,20+20),1)
                self.draw_curve_boxes(column_x+20,y_cursor,self.unit_width_for_column-50,self.height_for_a_task_bar_line+self.height_for_a_task_bar_line)
                # add task label
                temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size,bold=False,italic=False)
                object_name_text_bottom=temp_font.render("+",False,self.color["task_time"])
                self.surface.blit(object_name_text_bottom,(column_x+self.unit_width_for_column//2-30,y_cursor+5))
                # add points for buttons
                self.add_task_buttons.update({
                    self.database.index(column):{
                        "x":column_x+20,
                        "y":y_cursor,
                        "width":self.unit_width_for_column-50,
                        "height":self.height_for_a_task_bar_line+self.height_for_a_task_bar_line
                    }
                })
                # add column and tasks list to task_minimize_buttons
                # draw minimize button
                pygame.draw.circle(self.surface,self.color["minimize_button"],(column_x+self.unit_width_for_column-95,65),10)
                self.column_minimize_buttons.update({
                    self.database.index(column):column_x+self.unit_width_for_column-95
                })
                # draw left move button
                # print (self.database.index(column))
                if self.database.index(column)!=self.showable_columns[0]:
                    pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,65),10)
                    self.column_move_left_buttons.update({
                        self.database.index(column):column_x+self.unit_width_for_column-70
                    })
                pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,65),10,1)
                # draw right move button
                # print (self.database.index(column))
                if self.database.index(column)!=self.showable_columns[-1]:
                    pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-45,65),10)
                    self.column_move_right_buttons.update({
                        self.database.index(column):column_x+self.unit_width_for_column-45
                    })
                pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-45,65),10,1)
                # draw delete buttons
                pygame.draw.circle(self.surface,self.color["delete_buttons"],(column_x+self.unit_width_for_column-20,65),10)
                self.last_showable_column=self.database.index(column)
                if self.database.index(column) not in self.column_delete_buttons:
                    self.column_delete_buttons.update({
                    self.database.index(column):column_x+self.unit_width_for_column-20
                    })
                else:
                    self.column_delete_buttons[self.database.index(column)]=column_x+self.unit_width_for_column-20
                # print (column_x,self.unit_width_for_column)
                # print (self.database.index(column))
                # if column["title"]=="to do":
                #     print (column["title"],y_cursor)#y
                pass
                # draw cursor control bars
                # self.draw_curve_boxes(column_x+self.unit_width_for_column-20,50+20,,)
                total_page_height=y_cursor-50+self.height_for_a_task_bar_line+80-y_cursor_init
                viewable_page_height=HEIGHT-50-self.height_for_a_task_bar_line-30
                x_of_task_bar=column_x+self.unit_width_for_column-10
                y_of_task_bar=50+30
                width_of_task_bar=10
                height_of_task_bar=HEIGHT-50-35
                self.draw_curve_boxes(x_of_task_bar,y_of_task_bar,width_of_task_bar,height_of_task_bar,radius=8,color=self.color["cursor_bar"],thickness=1)
                # if self.database.index(column)==3:
                #     print (self.current_cursor_position[self.database.index(column)])
                #     print (total_page_height-viewable_page_height,total_page_height-viewable_page_height+20)
                if self.click[0]==1:
                    if x_of_task_bar<=self.mouse[0]<=x_of_task_bar+width_of_task_bar and y_of_task_bar<=self.mouse[1]<=y_of_task_bar+height_of_task_bar:
                        column_index=self.database.index(column)
                        # print (column["title"])
                        # print (y_cursor_init,y_cursor,total_page_height,viewable_page_height)
                        # print (y_cursor-total_page_height)
                        # print (total_page_height)
                        # if 0<=self.current_cursor_position[column_index] or self.current_cursor_position[column_index]<=total_page_height-viewable_page_height:
                        if self.mouse[1]<=height_of_task_bar//2:
                            # print ("ups")
                            # print (self.current_cursor_position[column_index])
                            if self.current_cursor_position[column_index]<=total_page_height-viewable_page_height:
                                self.current_cursor_position[column_index]+=30
                        else:
                            # print ("downs")
                            if self.current_cursor_position[column_index]>0:
                                self.current_cursor_position[column_index]-=30
                            # print (self.current_cursor_position[column_index])
                            # self.current_cursor_position[column_index]-=30
                pass
                # increase column x value
                column_x+=self.unit_width_for_column
                # print (self.database.index(column),"=",column_x,end=" ")
                # print (self.database.index(column),"=",column_x,end=" ")
                # print (self.database.index(column),"=",column_x,end=" ")
                # print ()
            else:
                # print (column["title"])
                # print (bar_x,self.menu_bar_size,end=", ")
                pygame.draw.circle(self.surface,self.color["bar_buttons"],(bar_x,(self.menu_bar_size//2)+5),self.menu_bar_size//2)
                temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size,bold=False,italic=False)
                object_name_text_bottom=temp_font.render(column["title"][0],False,self.color["background"])
                self.surface.blit(object_name_text_bottom,(bar_x-self.menu_bar_size//4,(self.menu_bar_size//2)+5-self.menu_bar_size//4))
                if self.database.index(column) not in self.bar_buttons:
                    self.bar_buttons.update({
                        self.database.index(column):{
                            "x":bar_x,
                            "y":(self.menu_bar_size//2)+5,
                            "radius":self.menu_bar_size//2
                        }
                    })
                else:
                    self.bar_buttons[self.database.index(column)]["x"]=bar_x
                    self.bar_buttons[self.database.index(column)]["y"]=(self.menu_bar_size//2)+5
                    self.bar_buttons[self.database.index(column)]["radius"]=self.menu_bar_size//2
                    # print (column["title"])
                bar_x+=self.menu_bar_size+10
                # if bar_x<=self.mouse[0]<=bar_x+self.menu_bar_size and (self.menu_bar_size//2)+5)<=:
                    # print ("ooops")
        # print ()
        if len(self.database)<self.most_number_of_columns:
            if len(self.database)==0:
                pass
            temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*4,bold=False,italic=False)
            object_name_text_bottom=temp_font.render("+",False,self.color["border_lines"])
            self.surface.blit(object_name_text_bottom,(column_x+(self.width_for_add_column//2)-self.default_font_text_size,((HEIGHT-50)//2)-self.default_font_text_size))
            self.draw_curve_boxes(column_x,50,self.width_for_add_column,HEIGHT-50)
    def paint_headings(self):
        pygame.draw.rect(self.surface,self.color["background"],(0,0,WIDTH,80))
        # full box
        # pygame.draw.rect(self.surface,self.color["border_lines"],(0,0,WIDTH,HEIGHT),1)
        self.draw_curve_boxes(0,0,WIDTH-1,HEIGHT-1)
        # menu box
        # pygame.draw.line(self.surface,self.color["border_lines"],(0,50),(WIDTH,50),1)
        self.draw_curve_boxes(0,0,WIDTH-1,50)
        # User_Name
        temp_font=pygame.font.SysFont(self.font_family,self.default_font_title_size,bold=False,italic=False)
        object_name_text_bottom=temp_font.render(self.User_Name,False,self.color["User_Name"])
        self.surface.blit(object_name_text_bottom,(10,10))
        # main menu
        pass
        # columns
        column_x=0
        bar_x=WIDTH-(len(self.bar_columns)*self.menu_bar_size)-20
        for column in self.database:
            pass
            if column["minimized"]=="False":
                # print (self.database.index(column),"=",column_x,end=" ")
                # column full box
                # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x,50,self.unit_width_for_column,HEIGHT-50),1)
                self.draw_curve_boxes(column_x,50,self.unit_width_for_column,HEIGHT-50)
                # column title box
                # pygame.draw.rect(self.surface,self.color["border_lines"],(column_x,50,self.unit_width_for_column,30),1)
                self.draw_curve_boxes(column_x,50,self.unit_width_for_column,30)
                # column title
                temp_font=pygame.font.SysFont(self.font_family,self.default_font_title_size*3//4,bold=False,italic=False)
                object_name_text_bottom=temp_font.render(column["title"][:10],False,self.color["column_title"])
                self.surface.blit(object_name_text_bottom,(column_x+10,60))
                # tasks
                y_cursor_init=y_cursor=80-self.current_cursor_position[self.database.index(column)]
                y_cursor+=self.height_for_a_task_bar_line
                # add column and tasks list to task_minimize_buttons
                # draw minimize button
                pygame.draw.circle(self.surface,self.color["minimize_button"],(column_x+self.unit_width_for_column-95,65),10)
                # draw left move button
                # print (self.database.index(column))
                if self.database.index(column)!=self.showable_columns[0]:
                    pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,65),10)
                pygame.draw.circle(self.surface,self.color["move_left"],(column_x+self.unit_width_for_column-70,65),10,1)
                # draw right move button
                # print (self.database.index(column))
                if self.database.index(column)!=self.showable_columns[-1]:
                    pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-45,65),10)
                pygame.draw.circle(self.surface,self.color["move_right"],(column_x+self.unit_width_for_column-45,65),10,1)
                # draw delete buttons
                pygame.draw.circle(self.surface,self.color["delete_buttons"],(column_x+self.unit_width_for_column-20,65),10)
                column_x+=self.unit_width_for_column
            else:
                # print (column["title"])
                # print (bar_x,self.menu_bar_size,end=", ")
                pygame.draw.circle(self.surface,self.color["bar_buttons"],(bar_x,(self.menu_bar_size//2)+5),self.menu_bar_size//2)
                temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size,bold=False,italic=False)
                object_name_text_bottom=temp_font.render(column["title"][0],False,self.color["background"])
                self.surface.blit(object_name_text_bottom,(bar_x-self.menu_bar_size//4,(self.menu_bar_size//2)+5-self.menu_bar_size//4))
                if self.database.index(column) not in self.bar_buttons:
                    self.bar_buttons.update({
                        self.database.index(column):{
                            "x":bar_x,
                            "y":(self.menu_bar_size//2)+5,
                            "radius":self.menu_bar_size//2
                        }
                    })
                else:
                    self.bar_buttons[self.database.index(column)]["x"]=bar_x
                    self.bar_buttons[self.database.index(column)]["y"]=(self.menu_bar_size//2)+5
                    self.bar_buttons[self.database.index(column)]["radius"]=self.menu_bar_size//2
                    # print (column["title"])
                bar_x+=self.menu_bar_size+10
                # if bar_x<=self.mouse[0]<=bar_x+self.menu_bar_size and (self.menu_bar_size//2)+5)<=:
                    # print ("ooops")
        # print ()
        if len(self.database)<self.most_number_of_columns:
            if len(self.database)==0:
                pass
            temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*4,bold=False,italic=False)
            object_name_text_bottom=temp_font.render("+",False,self.color["border_lines"])
            self.surface.blit(object_name_text_bottom,(column_x+(self.width_for_add_column//2)-self.default_font_text_size,((HEIGHT-50)//2)-self.default_font_text_size))
            self.draw_curve_boxes(column_x,50,self.width_for_add_column,HEIGHT-50)
            # print ()
    def paint_input_text_box(self):
        pass
        # text section
        message="Please select a good title. This cannot be changed later."
        message_lines=self.get_apt_message(message,length=50)
        width=400
        height=(len(message_lines)*20)+80
        x=(WIDTH//2)-(width//2)
        y=(HEIGHT//2)-(height//2)
        # set background
        # pygame.draw.rect(self.surface,self.color["background"],(x,y,width,height))
        self.draw_curve_boxes(x,y,width,height,fill=True,color=self.color["background"])
        self.draw_curve_boxes(x,y,width,height)
        # pygame.draw.rect(self.surface,self.color["border_lines"],(x,y,width,height),3)
        self.draw_curve_boxes(x,y,width,height,thickness=3)
        # set heading
        temp_font=pygame.font.SysFont(self.font_family,self.default_font_text_size*3//4,bold=False,italic=False)
        y_cursor=y+20
        for line in message_lines:
            text=temp_font.render(line,False,self.color["task_title"])
            self.surface.blit(text,(x+30,y_cursor))
            y_cursor+=20
            # print (x+30,y_cursor)
            # print (self.color["task_title"])
        # set text title
        y_cursor=y+80
        text=temp_font.render(self.input_text,False,self.color["task_description"])
        self.surface.blit(text,(x+30,y_cursor))
    def add_column(self):
        pass
        if self.click[0]==1:
            if WIDTH-self.width_for_add_column<=self.mouse[0]<=WIDTH and 50<=self.mouse[1]<=HEIGHT:
                # print ("ooops")
                if len(self.database)<self.most_number_of_columns:
                    self.database.append({
                            "title":"New One",
                            "minimized":"False",
                            "tasks":{}
                            })
    def set_text_into_tasks(self,character,erase=False):
        pass
        try:
            if self.active["title_or_Description"]=="title" and self.active["task"]==None:
                pass
                # print (self.database[self.active["column"]]["tasks"])
                existing_title=self.database[self.active["column"]]["title"]
                # print (existing_title)
                if erase:
                    self.database[self.active["column"]]["title"]=existing_title[:-1]
                else:
                    self.database[self.active["column"]]["title"]=existing_title+character
                # self.database[self.active["column"]]["tasks"][self.active["task"]]=[]
            elif self.active["title_or_Description"]=="Description":
                if erase:
                    self.database[self.active["column"]]["tasks"][self.active["task"]]["Description"]=self.database[self.active["column"]]["tasks"][self.active["task"]]["Description"][:-1]
                else:
                    self.database[self.active["column"]]["tasks"][self.active["task"]]["Description"]+=character
                    pass
        except:
            pass
    def add_new_title_into_database(self):
        date=datetime.datetime.now()
        self.database[self.input_text_target]["tasks"].update({
            self.input_text: {
                "time": {
                  "year":date.year,
                  "month":date.month,
                  "date":date.day,
                  "hour":date.hour,
                  "minute":date.minute,
                  "second":date.second,
                  "day":date.strftime("%A")[:3]
                },
                "Description": "",
                "minimized":"False"
              }
        })
        self.input_text_enabled=False
    def do_main_operations(self):
        try:
            self.calculate_basic_metrices()
            self.paint()
            self.paint_headings()
            if self.input_text_enabled:
                pass
                self.paint_input_text_box()
            else:
                ___=self.manage_text_cards()
                ___=self.manage_buttons()
            self.update_database_in_file()
        except:
            print ("please report this")
    def set_mouse_and_clicks(self):
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
    def main(self):
        play=True
        for column_index in range(len(self.database)):
            for task in self.database[column_index]["tasks"]:
                # self.database[column_index]["tasks"][task]["minimized"]="True"
                pass
        while play:
            surface.fill(self.color["background"])
            # print (self.mouse)
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_BACKSPACE:
                        # self.text=""
                        pass
                    if event.key==K_TAB:
                        play=False
                        # self.view_letter()
                    if 97<=event.key<=122 or 48<=event.key<=57 or event.key==32 or event.key==95 or event.key==13:
                        # 32=space
                        # 95=_
                        # 13=ENTER
                        if self.input_text_enabled:
                            pass
                            if event.key==K_RETURN:
                                self.add_new_title_into_database()
                                self.input_text=""
                            else:
                                self.input_text+=chr(event.key)
                        else:
                            self.set_text_into_tasks(chr(event.key))
                        # self.text+=chr(event.key)
                    if event.key==K_BACKSPACE:
                        if self.input_text_enabled:
                            pass
                            self.input_text=self.input_text[:-1]
                        else:
                            self.set_text_into_tasks(None,erase=True)
            #-----
            tid1=threading.Thread(target=self.do_main_operations,args=())
            tid2=threading.Thread(target=self.set_mouse_and_clicks,args=())
            tid1.start()
            tid2.start()
            tid1.join()
            tid2.join()
            #-----
            pygame.display.update()
            ft.tick(fps)




if __name__=="__main__":
    Main(surface).main()






# #----------------

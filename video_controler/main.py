import tkinter as tk
import tkinter.messagebox
import os
from PIL import Image, ImageTk


main_window = tk.Tk()
main_window.geometry("1920x1140")
main_window.title("Video Controler")
#main_window.config(bg="white")

width = 1920
height = 1140
main_window.minsize(width,height)
main_window.maxsize(width,height)
folder_items_dict = {}

default_font = ("Arial", 16)
var_main_path = "C:\My documents\ACGN\Anime\\"
side_image_path = "C:\My documents\ACGN\TuTu\side_image.jpg"
side_bottom_img_path = "C:\My documents\ACGN\TuTu\side_bottom_img.png"

labels = []
label_images = []
label_images_names = []
var_page = 0
def delete_all_label_images():
    for label_img in label_images:
        label_img.destroy()
    for label_img_name in label_images_names:
        label_img_name.destroy()
    label_images.clear()   
    label_images_names.clear()


def create_item_in_main_window(event):
    label = event.widget
    
    
    canvas_item = tk.Canvas(main_window, width=765,height=1080)
    

    image_path = var_main_path.get() + label['text'] + "\\" + "cover.jpg"
    # for insert_backflash in range(0, len(image_path)-2):
    #     if image_path[insert_backflash] == "\\":

    img_pil = Image.open(image_path)
    img = ImageTk.PhotoImage(img_pil)
    image = canvas_item.create_image(400,540,anchor="center",image=img)
    canvas_item.pack(side="top")
    folder_items_dict[image_path + "_one"] = img
    folder_items_dict[image_path + "_two"] = image

    image_label = tk.Label(main_window, image=img)
    #canvas_item.bind("<Button-1>",delete_image)
    image_label.pack()

def resize_image(image_path, base_width=200):  
    """  
    调整图像大小以适应给定的基础宽度，同时保持图像的宽高比。  
    """  
    with Image.open(image_path) as img:  
        # 计算新的高度，保持宽高比  
        w_percent = (base_width / float(img.size[0]))  
        h_size = int((float(img.size[1]) * float(w_percent)))  
        img = img.resize((base_width, h_size), Image.LANCZOS)  
        img = ImageTk.PhotoImage(img)  
    return img  
  
def create_resiezed_images(start_sign):  
    #delete_all_label()
  
    # 创建一个Canvas，大小为1280x720  
    
    
    
    list_length = len(os.listdir(var_main_path))
    image_label_x_num = 0
    image_label_y_num = 0
    image_label_name_x_num = 0
    image_label_name_y_num = 0
    std_num = 0 #用来统计有效cover文件数量
    page_signs = 0
    for cover in range(start_sign, list_length):
        if (len(label_images) == 15):
            break
        without_situation_path = var_main_path + (os.listdir(var_main_path))[cover] + "\\"
        try:
            if 'cover.jpg' not in os.listdir(without_situation_path):
                print(f"{(os.listdir(var_main_path))[cover]}还没有cover图片")
                continue
            cover_path = var_main_path + (os.listdir(var_main_path))[cover]  + "\\" + "cover.jpg"
            if std_num % 5 == 0 and std_num != 0:
                image_label_x_num = 0
                image_label_y_num += 1
                image_label_name_x_num = 0
                image_label_name_y_num += 1
            image_label_x = 50 + image_label_x_num*300
            image_label_y = 60 + image_label_y_num*350
            image_label_x_num += 1
        # 加载并调整图像大小  
            image_path = cover_path  # 替换为你的图片路径  
            resized_image = resize_image(cover_path)  

            # 将调整后的图像添加到Canvas上  
            image_label = tk.Label(main_window, image=resized_image)  
            label_images.append(image_label)
            page_signs += 1
            image_label.path = var_main_path + (os.listdir(var_main_path))[cover]   
            image_label.bind("<Button-1>",press_to_playvideo)
            image_label.image = resized_image  # 防止图像被垃圾回收  
            image_label.place(x=image_label_x,y=image_label_y)

            #cover图片下的动画名称
            image_label_name_x = 70 + image_label_name_x_num*300
            image_label_name_y = 360 + image_label_name_y_num*355

            ch_word = 0
            for char in (os.listdir(var_main_path))[cover]:
                if ('\u4e00' <= char <= '\u9fff') or ('\u3400' <= char <= '\u4dbf'):
                    ch_word  += 2
                else:
                    ch_word += 1
            if ch_word > 14:
                label = tk.Label(main_window, bg="#F2EC9C", width=12,height=1,text=((os.listdir(var_main_path))[cover])[0:7] + "...",font=("微软雅黑", 16,'bold'))
                label_images_names.append(label)
                page_signs += 1
            else:
                label = tk.Label(main_window, bg="#F2EC9C",width=12,height=1,text=(os.listdir(var_main_path))[cover],font=("微软雅黑",16,'bold'))
                label_images_names.append(label)
                page_signs += 1
            label.path = image_label.path
            label.bind("<Button-1>",press_to_playvideo)
            label.place(x=image_label_name_x, y=image_label_name_y)
            image_label_name_x_num += 1
            std_num += 1
        except:
            continue

def press_to_playvideo(event):
    press_event = event.widget
    for filename in os.listdir(press_event.path):
        if ".mp4"  in filename:
            os.startfile(press_event.path + "\\" + filename)
            return
        elif ".mkv" in filename:
            os.startfile(press_event.path + "\\" + filename)
            return
        else:
            continue
    return tkinter.messagebox.showerror("Error","该目录下没有视频文件")

def next_page():
    global var_page
    delete_all_label_images()
    var_page += 1
    create_resiezed_images(var_page * 15)

def prev_page():
    global var_page
    if(var_page - 1 < 0):
        tkinter.messagebox.showerror('error','前面没有内容了哦')
        return
    delete_all_label_images()
    var_page -= 1
    create_resiezed_images(var_page * 15)

btn_1 = tk.Button(main_window,text="上一页",font=("微软雅黑",14,'bold'),command=prev_page)
btn_1.place(x=1600, y=750)
btn_2 = tk.Button(main_window, text="下一页",font=("微软雅黑",14,'bold'),command=next_page)
btn_2.place(x=1700, y=750)

#界面侧边图片
side_img_pil = Image.open(side_image_path)
side_img_ready = ImageTk.PhotoImage(side_img_pil)
side_img = tk.Label(main_window,image=side_img_ready)
side_img.place(x=1480,y=60,width=side_img_pil.width,height=side_img_pil.height)

#界面侧边下方图片
side_bottom_img_pil = Image.open(side_bottom_img_path)
side_bottom_img_ready = ImageTk.PhotoImage(side_bottom_img_pil)
side_bottom_img = tk.Label(main_window,image=side_bottom_img_ready)
side_bottom_img.place(x=1480,y=850,width=side_bottom_img_pil.width,height=side_bottom_img_pil.height)


create_resiezed_images(0)

main_window.mainloop()
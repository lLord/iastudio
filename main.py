from PIL import Image, ImageTk
from gradio_client import Client, handle_file
from random import randrange
import time
from ui import *

# load from prompt.txt
with open("./config/prompt.txt", 'r') as file:
    content = file.read()
    textPrompt.delete(1.0, tk.END)  # Clear previous content
    textPrompt.insert(tk.END, content)

# load from prompt.txt
with open("./config/negative_prompt.txt", 'r') as file:
    content = file.read()
    textNegPrompt.delete(1.0, tk.END)  # Clear previous content
    textNegPrompt.insert(tk.END, content)

def promt_to_text():
    #save prompts
    texto_positivo = textPrompt.get('1.0', tk.END)
    fl = open("./config/prompt.txt", "w")
    fl.write(texto_positivo)
    fl.close()
    texto_negativo = textNegPrompt.get('1.0', tk.END)
    fl = open("./config/negative_prompt.txt", "w")
    fl.write(texto_negativo)
    fl.close()

    print("Cargar")
    tiempo = generate(texto_positivo, texto_negativo)
    lblRightTime.config(text="Generado en" + str(tiempo))

    print("Cargado")

def generate(texto_positivo, texto_negativo):
    PROMPT= texto_positivo
    NEG_PROMPT= texto_negativo
    start_time = time.time()
    client = Client("doevent/stable-diffusion-3.5-large-turbo")
    print('generando')
    result = client.predict(
            prompt=PROMPT,
            negative_prompt=NEG_PROMPT,
            seed=0,
            randomize_seed=True,
            width=768,
            height=768,
            guidance_scale=0,
            num_inference_steps=4,
            api_name="/infer"
    )
    print('Guardando imagen...')
    im=Image.open(result[0])  
    im.save('./result.png')
    im=Image.open('./result.png')  
    current_timestamp = time.time()
    im.save( "./history/" + str(current_timestamp) + ".png")
    tiempo = time.time() - start_time
    photo2 = ImageTk.PhotoImage(Image.open('./result.png'))
    label.configure(image=photo2)
    label.image = photo2
    print("%s" % (tiempo))
    return tiempo

def Upscaler():
    client = Client("https://bookbot-image-upscaling-playground.hf.space/")
    result = client.predict(
                    "./result.png",	# str (filepath or URL to image)
                    "modelx4",	# str in 'Choose Upscaler' Radio component
                    api_name="/predict"
    )
    print(result)
    print('Guardando imagen...')
    im=Image.open(result)  
    im.save('./result_upscale.png')

button = tk.Button(mainFrameRight, text="Generar", fg="white", bg="gray20", command=promt_to_text, font=("Arial", 14))
button.pack()
root.bind("<Return>", promt_to_text)

################################

def upscaler_window():
    new_window = tk.Toplevel()
    new_window.title('IA Studio ::: Upscaler')
    new_window.iconbitmap("./assets/icon.ico")
    new_window.geometry("1000x900+50+50")
    new_window.configure(bg="black")

    upscaleFrameCenter = tk.Frame(new_window, width=800, height=800, bg = "gray40")
    upscaleFrameCenter.pack_propagate(False)
    upscaleFrameCenter.pack( side="left", fill='both', expand='true')

    photo = ImageTk.PhotoImage(Image.open('./result.png'))
    label = tk.Label(upscaleFrameCenter, image=photo)
    label.configure(image=photo)
    label.image = photo
    label.pack()

    upscaleFrameRight = tk.Frame(new_window, width=800, height=800, bg = "gray40")
    upscaleFrameRight.pack_propagate(False)
    upscaleFrameRight.pack( side="left", fill='both', expand='true')

    button = tk.Button(upscaleFrameRight, text="Upscale X4", fg="white", bg="gray20", command=Upscaler, font=("Arial", 14))
    button.pack()

iconUpscale = ImageTk.PhotoImage(file = "./assets/upscale_icon.png") 
btnUpscaleMode = tk.Button(mainFrameLeft, image = iconUpscale, bd = 0, command=upscaler_window, height = 50, width = 50, bg="gray10", font=("Arial", 12))
btnUpscaleMode.pack(side = "top")
ToolTip(btnUpscaleMode, msg="Upscaler")


icon3 = ImageTk.PhotoImage(file = "./assets/inpaint_icon.png") 
btnGenerateMode3 = tk.Button(mainFrameLeft, image = icon3, bd = 0, command=inpainting_window,  height = 50, width = 50, bg="gray10", font=("Arial", 12))
btnGenerateMode3.pack(side = "top")
ToolTip(btnGenerateMode3, msg="Inpainting")

icon4 = ImageTk.PhotoImage(file = "./assets/pose_icon.png") 
btnGenerateMode4 = tk.Button(mainFrameLeft, image = icon4, bd = 0, command=controlnet_window,  height = 50, width = 50, bg="gray10", font=("Arial", 12))
btnGenerateMode4.pack(side = "top")
ToolTip(btnGenerateMode4, msg="ControlNET")







# Execute tkinter
tk.mainloop()

# Pyistaller make EXE
# python -m PyInstaller --name AISTudio --windowed --collect-data gradio_client --add-data=./config:./config main.py
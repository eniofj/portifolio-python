import tkinter.messagebox as messagebox
from pyautogui import ImageNotFoundException
import datetime
import pyautogui as pyg
import sys
import time



def verificar_screen(img):
    while True:
        try:
            time.sleep(1)
            # Tenta localizar a imagem
            if pyg.locateOnScreen(f'telas/{img}', grayscale=True, confidence=0.7):
                break  # Sai do loop se encontrar a imagem
        except ImageNotFoundException:
            # Se a exceção ocorrer, apenas continua no loop
            pass
        time.sleep(1)  # Aguarda 1 segundo antes de tentar novamente
    time.sleep(1)  # Aguarda 1 segundos extras antes de retornar
    return True





def verificar_screen_timeout(img, codigo, timeout=2):
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).total_seconds() < timeout:
        try:
            if pyg.locateOnScreen(f'telas/{img}', grayscale=True, confidence=0.9):
                messagebox.showinfo("Aviso", f"A estrutura do {codigo} já está cadastrada!")
                exit()  # ou return, ou raise, dependendo do que você quiser fazer ao detectar
        except ImageNotFoundException:
            pass
        time.sleep(0.2)  # tenta várias vezes dentro dos 2s


import tkinter as tk
from tkinter import ttk
import time

# Тестовый список
bank_list = [i for i in range(10000)]

# Тестовая функция для прогресс бара
def scan():
    for i in bank_list:
        print(i)
        pr_bar.step(100/len(bank_list)) # изменение шага для перемещения прогресс бара
        pr_bar.update() # обновление строки прогресс бара
    finish_label.place(relx=0.427, rely=0.8)

# Создание окна программы
root = tk.Tk()

root.title('Парсинг монет')

#Задание размеров окна программы
w = 600
h = 300

#Определение разрешения экрана
ws = root.winfo_screenwidth()
wh = root.winfo_screenheight()

#Определение верхнего левого угла окна программы
x = int(ws/2 - w/2)
y = int(wh/2 - h/2)

# Выравнивание окна программы по центру экрана
root.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))
root.resizable(False, False)

# Установка иконки в окне программы
root.iconbitmap('icon.ico')

# Установка фона программы
bgimage = tk.PhotoImage(file = 'background.png')
backgr = tk.Label(root, image = bgimage)
backgr.pack()

#Создание и размещение прогресс бара
pr_bar=ttk.Progressbar(root, orient="horizontal", length=300, mode = "determinate")
pr_bar.place(relx=0.251, rely=0.6)

# Создание кнопки запуска парсера
start_button = tk.Button(root, text = "Запустить парсер!", bg = 'white',
                          font = 'Arial 15 italic', activebackground = '#C5FCDD', command=scan
)
start_button.place(relx = 0.33, rely = 0.3)

# Создание отметки для отображения завершения парсинга
finish_label = tk.Label(root, text = "Готово!", bg='white', font= 'Arial 15 italic')
#finish_label.place(relx=0.427, rely=0.8)


root.mainloop()
import tkinter as tk

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

# Установка иконки в окне программы
root.iconbitmap('icon.ico')

# Установка фона программы
bgimage = tk.PhotoImage(file = 'background.png')
backgr = tk.Label(root, image = bgimage)
backgr.pack()

root.mainloop()
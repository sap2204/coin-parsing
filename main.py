import tkinter as tk

# Создание окна программы
root = tk.Tk()

root.title('Парсинг монет')

# Создание ширины и высоты окна
w = 800
h = 600

# Определение ширины и высоты экрана пользователя
ws = root.winfo_screenwidth()
wh = root.winfo_height()

# Определение верхнего левого угла программы
x = int(ws/2 - w/2)
y = int(wh/2 - h/2)

# Вывод окна программы по центру экрана
root.geometry("{0} x {1} + {2} + {3}".format(w, h, x, y))
root.mainloop()
import cv2
import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from pyzxing import BarCodeReader
def decode_qr():
    lang = LANGUAGES[current_lang]
    filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]
    filepath = filedialog.askopenfilename(title=lang['decode_title'] if 'decode_title' in lang else 'Выберите файл QR-кода', filetypes=filetypes)
    if not filepath:
        return
    # Не выбираем папку заранее, теперь пользователь решает после показа результата
    import numpy as np
    def imread_unicode(path):
        try:
            with open(path, 'rb') as f:
                arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            return img
        except Exception:
            return None
    try:
        import os
        reader = BarCodeReader()
        result = reader.decode(filepath)
        if not result or not result.get('barcodes'):
            detector = cv2.QRCodeDetector()
            img = imread_unicode(filepath)
            if img is None:
                messagebox.showerror(lang['error'], lang.get('decode_error', 'Не удалось открыть файл изображения!'))
                return
            data, points, _ = detector.detectAndDecode(img)
            if not data:
                messagebox.showwarning(lang['error'], lang.get('decode_not_found', 'QR-код не найден!'))
                return
            # Показываем результат и предлагаем сохранить
            show_save_result_window(data, filepath)
            return
        raw_data = b''.join([
            b['raw'] if isinstance(b.get('raw'), bytes) else b.get('raw', '').encode('utf-8')
            for b in result['barcodes'] if b.get('parsed') or b.get('raw')
        ])
        if not raw_data:
            messagebox.showwarning(lang['error'], lang.get('decode_not_found', 'QR-код не найден!'))
            return
        # Показываем результат и предлагаем сохранить
        try:
            display = raw_data.decode('utf-8')
        except Exception:
            display = raw_data.hex()
        show_save_result_window(display, filepath, raw_data)
    except Exception as e:
        try:
            detector = cv2.QRCodeDetector()
            img = imread_unicode(filepath)
            if img is None:
                messagebox.showerror(lang['error'], lang.get('decode_error', 'Не удалось открыть файл изображения!'))
                return
            data, points, _ = detector.detectAndDecode(img)
            if not data:
                messagebox.showerror(lang['error'], lang.get('decode_error', f'Ошибка при расшифровке: {e}'))
                return
            show_save_result_window(data, filepath)
        except Exception as e2:
            messagebox.showerror(lang['error'], lang.get('decode_error', f'Ошибка при расшифровке: {e2}'))
# Окно для показа результата и кнопки сохранения
import os
def show_save_result_window(result_text, source_filepath, raw_bytes=None):
    lang = LANGUAGES[current_lang]
    win = tk.Toplevel()
    win.title(lang.get('decode_result', 'Результат'))
    win.geometry('450x350')
    win.resizable(False, False)
    # Текстовое поле с результатом
    text_widget = tk.Text(win, wrap='word', height=10, width=45)
    text_widget.insert('1.0', result_text)
    text_widget.config(state='disabled')
    text_widget.pack(pady=10)
    # Кнопка сохранения
    def save_to_txt():
        base_name = os.path.splitext(os.path.basename(source_filepath))[0]
        file_path = filedialog.asksaveasfilename(
            title=lang.get('save_result', 'Сохранить результат'),
            defaultextension='.txt',
            initialfile=base_name + '.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        if not file_path:
            return
        try:
            # Если переданы байты, сохраняем их, иначе строку
            if raw_bytes is not None:
                with open(file_path, 'wb') as f:
                    f.write(raw_bytes)
            else:
                with open(file_path, 'w' , encoding='utf-8') as f:
                    f.write(result_text)
            messagebox.showinfo(lang.get('success', 'Успех'), lang.get('saved_success', 'Результат успешно сохранён!'))
        except Exception as err:
            messagebox.showerror(lang.get('error', 'Ошибка'), f"{lang.get('error_msg', 'Не удалось сохранить файл: {e}').format(e=err)}")
    save_btn = tk.Button(win, text=lang.get('save_btn', 'Сохранить в .txt'), command=save_to_txt, bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'))
    save_btn.pack(pady=5)
    # Кнопка закрытия
    close_btn = tk.Button(win, text=lang.get('close_btn', 'Закрыть'), command=win.destroy)
    close_btn.pack(pady=2)
import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# Языковые словари
LANGUAGES = {
    'ru': {
        'title': 'Генератор QR-кодов',
        'enter_text': 'Введите текст для QR-кода:',
        'filename': 'Имя файла (без .png):',
        'create_btn': 'Создать QR-код',
        'decode_btn': 'Расшифровать QR-код',
        'decode_title': 'Выберите файл QR-кода',
        'decode_result': 'Результат',
        'decode_not_found': 'QR-код не найден!',
        'decode_error': 'Ошибка при расшифровке: {e}',
        'success': 'Успех',
        'success_msg': 'QR-код успешно создан и сохранён как {filename}.png в папке с программой.',
        'error': 'Ошибка',
        'error_msg': 'Не удалось сохранить файл: {e}',
        'fill_fields': 'Пожалуйста, заполните все поля!',
        'save_btn': 'Сохранить в .txt',
        'close_btn': 'Закрыть',
        'saved_success': 'Результат успешно сохранён!'
    },
    'en': {
        'title': 'QR Code Generator',
        'enter_text': 'Enter text for QR code:',
        'filename': 'File name (without .png):',
        'create_btn': 'Create QR code',
        'decode_btn': 'Decode QR code',
        'decode_title': 'Select QR code file',
        'decode_result': 'Result',
        'decode_not_found': 'QR code not found!',
        'decode_error': 'Decoding error: {e}',
        'success': 'Success',
        'success_msg': 'QR code successfully created and saved as {filename}.png in the program folder.',
        'error': 'Error',
        'error_msg': 'Failed to save file: {e}',
        'fill_fields': 'Please fill in all fields!',
        'save_btn': 'Save as .txt',
        'close_btn': 'Close',
        'saved_success': 'Result saved successfully!'
    }
}

# Текущий язык
current_lang = 'ru'

def set_language(lang):
    global current_lang
    current_lang = lang
    update_ui_language()

def update_ui_language():
    lang = LANGUAGES[current_lang]
    root.title(lang['title'])
    label_text.config(text=lang['enter_text'])
    label_filename.config(text=lang['filename'])
    btn_generate.config(text=lang['create_btn'])
    btn_decode.config(text=lang['decode_btn'])

def generate_qr():
    lang = LANGUAGES[current_lang]
    text = entry_text.get("1.0", tk.END).strip()
    filename = entry_filename.get()
    # Максимальный размер данных для QR-кода (версия 40, коррекция L): 2953 байта (UTF-8)
    max_bytes = 2953
    text_bytes = text.encode('utf-8')
    if not text or not filename:
        messagebox.showwarning(lang['error'], lang['fill_fields'])
        return
    if len(text_bytes) > max_bytes:
        messagebox.showerror(
            lang['error'],
            f"Слишком длинный текст!\n\nМаксимально допустимо: {max_bytes} байт (UTF-8). Сейчас: {len(text_bytes)} байт.\n\nУменьшите текст или разделите на несколько QR-кодов."
        )
        return
    try:
        img = qrcode.make(text)
        img.save(filename + ".png")
        show_qr_in_app(filename + ".png")
        messagebox.showinfo(lang['success'], lang['success_msg'].format(filename=filename))
    except Exception as e:
        messagebox.showerror(lang['error'], lang['error_msg'].format(e=e))

# Фрейм для отображения QR-кода
qr_frame = None
qr_label = None

def show_qr_in_app(filepath):
    global qr_frame, qr_label, qr_img
    try:
        if qr_frame is None:
            qr_frame = tk.Frame(root)
            qr_frame.pack(pady=5)
        if qr_label is not None:
            qr_label.destroy()
        img = Image.open(filepath)
        img = img.resize((120, 120), Image.LANCZOS)
        qr_img = ImageTk.PhotoImage(img)
        qr_label = tk.Label(qr_frame, image=qr_img)
        qr_label.image = qr_img  # Prevent garbage collection
        qr_label.pack()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось отобразить QR-код: {e}")

root = tk.Tk()
root.geometry("350x370")
root.resizable(False, False)

# Языковое меню
menubar = tk.Menu(root)
lang_menu = tk.Menu(menubar, tearoff=0)
lang_menu.add_command(label="Русский", command=lambda: set_language('ru'))
lang_menu.add_command(label="English", command=lambda: set_language('en'))
menubar.add_cascade(label="Язык / Language", menu=lang_menu)
root.config(menu=menubar)

label_text = tk.Label(root, text=LANGUAGES[current_lang]['enter_text'])
label_text.pack(pady=(15, 0))
# Используем Text вместо Entry для неограниченного ввода
entry_text = tk.Text(root, width=40, height=4, wrap="word")
entry_text.pack(pady=5)
# Добавляем стандартные бинды для вставки из буфера обмена
def bind_text_clipboard_shortcuts(widget):
    # Стандартные бинды для вставки (работают на всех раскладках)
    widget.bind('<Control-v>', lambda e: (widget.focus_force(), widget.event_generate('<<Paste>>')))
    widget.bind('<Control-V>', lambda e: (widget.focus_force(), widget.event_generate('<<Paste>>')))
    widget.bind('<Command-v>', lambda e: (widget.focus_force(), widget.event_generate('<<Paste>>')))
    widget.bind('<Command-V>', lambda e: (widget.focus_force(), widget.event_generate('<<Paste>>')))
    widget.bind('<Shift-Insert>', lambda e: (widget.focus_force(), widget.event_generate('<<Paste>>')))
    # Для ПКМ — показываем стандартное меню вставки
    def show_context_menu(event):
        try:
            widget.event_generate('<<Paste>>')
        except Exception:
            pass
    widget.bind('<Button-3>', show_context_menu)

bind_text_clipboard_shortcuts(entry_text)

label_filename = tk.Label(root, text=LANGUAGES[current_lang]['filename'])
label_filename.pack(pady=(10, 0))
entry_filename = tk.Entry(root, width=40)
entry_filename.pack(pady=5)


btn_generate = tk.Button(root, text=LANGUAGES[current_lang]['create_btn'], command=generate_qr, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
btn_generate.pack(pady=7)

btn_decode = tk.Button(root, text=LANGUAGES[current_lang]['decode_btn'], command=decode_qr, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
btn_decode.pack(pady=7)

update_ui_language()
root.mainloop()
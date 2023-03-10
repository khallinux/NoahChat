
import re
import subprocess
import threading
from tkinter import messagebox as msg
from awesometkinter.bidirender import add_bidi_support
from langdetect import detect
import arabic_reshaper
import openai
from bidi.algorithm import get_display
from gtts import gTTS
from mtranslate import translate
from api_key import API_KEY
from customtkinter import *
import speech_recognition as sr
from tkinter import *

from Api_check import ApiKey
from openai_response import text_to_speech
class Noah(Tk):
    openai.api_key = API_KEY
    def __init__(self, **kw):
        super().__init__()
        self.withdraw()
        self.api_key = ApiKey().api_key
        if not self.api_key:
            msg.showerror(title="Enter the API_KEY",message="API key is missing.You Can't Run the Program")
            exit()
        self.frameText = CTkFrame(self,fg_color="black",width=1035,height=600)
        self.framEntry = CTkFrame(self)
        self.previousText = ''
        # Define colors for the variouse types of tokens
        self.normal = self.rgb((234, 234, 234))
        self.keywords = self.rgb((234, 95, 95))
        self.comments = self.rgb((95, 234, 165))
        self.strings = self.rgb((234, 162, 95))
        self.functins = self.rgb((95, 211, 234))
        self.background = self.rgb((42, 42, 42))
        # Define a list of Regex Pattern that should be colored in a certain way
        self.repl = [
            [
                '(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )',
                self.keywords],
            ['".*?"', self.strings],
            ['\'.*?\'', self.strings],
            ['#.*?$', self.comments],
        ]
        #Animation
        self.num_liness = 14



        self.text_widget = CTkTextbox(self.frameText, width=80, height=320, wrap="word", fg_color="black",text_color="red", font=("console", 14, "bold"))
        self.label_Englich=Label(self,text="English")
        self.label_Arabic=Label(self,text="Arabic")


        self.text_widget.place(x=50, y=140, relx=0.415035890649, rely=0.5, anchor=W)
        self.lines = []
        self.scroll_text()#end animation
        #Entrys
        self.entry = Entry(self,width=101,background=self.background,foreground="white")
        #Buttons
        self.button_exit =CTkButton(master=self, text="Exit")
        self.button_send =CTkButton(master=self, text="Send",width=20,height=10,bg_color=self.background, command=self.send_and_clear_entry)
        self.button_run_python =CTkButton(master=self, text="Run",width=20,height=10,border_width=0, command=self.run_code)
        self.button_clear_teminal =CTkButton(master=self, text="Clear",bg_color=self.background,width=20,height=10,border_width=0, command=self.clear_terminal)
        self.button_delete_code_text =CTkButton(master=self, text="Delete",width=20,height=10,border_width=0, command=self.delete_code)
        self.stop_code_button =CTkButton(master=self, text="Stop",width=20,height=10,border_width=0,bg_color=self.background, command=self.stop_output)
        #VARIBLES
        self.stop_flag = BooleanVar(value=False)
        self.selected_option =IntVar()
        self.choice_langue = StringVar()
        #Menu langue
        self.option_langue =OptionMenu(self, self.choice_langue ,"en", "ar")

        self.python_button =CTkRadioButton(self, text="python",text_color="black", variable=self.selected_option, value=1,command=self.python_coding)
        self.qustion_button = CTkRadioButton(self, text="normal",text_color="black", variable=self.selected_option, value=0,command=self.normal_answer)
        self.english_button =CTkRadioButton(self, variable=self.choice_langue, value="en",command=self.on_radio_button_selected)
        self.arabic_button = CTkRadioButton(self, variable=self.choice_langue, value="ar",command=self.on_radio_button_selected)
        #TextBoxs
        self.english_answer = CTkTextbox(self.frameText ,fg_color=self.background,width=480,height=320)
        self.answerText = CTkTextbox(self.frameText,width=480,height=320,wrap="word", fg_color="white", text_color="black", font=("console", 14, "bold"))
        self.python_answer = CTkTextbox(self ,fg_color="white",text_color="black",width=950,height=120)

        self.frameText.place(x=2,y=5,relx=0.496595, rely=0.5, anchor=S)

        self.process = None  # initialize process variable to None


        self.answerText.place(x=50,y=140,relx=0.49, rely=0.5, anchor=W)
        self.english_answer.place(x=10,y=140,relx=0.45, rely=0.5, anchor=E)

        self.entry.place(x=0,y=250,relx=0.5, rely=0.5,height=85, anchor=CENTER)

        self.option_langue.place(x=0, y=250, relx=0.5, rely=0.15, anchor=CENTER)

        self.python_button.place(x=10,y=250,relx=0.0424, rely=0.178, anchor=CENTER)

        self.qustion_button.place(x=10,y=250,relx=0.0424, rely=0.136, anchor=CENTER)

        self.label_Englich.place(x=46,y=250,relx=0.90424, rely=0.178, anchor=CENTER)
        self.english_button.place(x=134,y=250,relx=0.90424, rely=0.178, anchor=CENTER)

        self.label_Arabic.place(x=46,y=250,relx=0.90424, rely=0.136, anchor=CENTER)
        self.arabic_button.place(x=134,y=250,relx=0.90424, rely=0.136, anchor=CENTER)

        self.button_send.place(x=10,y=250,relx=0.84327545, rely=0.45425, anchor=W)
        print(self.selected_option.get())
        self.bind('<Control-r>', self.execute)
        self.english_answer.bind('<KeyRelease>', self.changes)
        self.entry.bind("<Return>", self.send_and_clear_entry)
        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_conversion_type_selected(self, selection):
        if self.choice_langue == "en":
            if selection == "Ar to En":
                # Change the language to Arabic
                text = self.entry.get()
                self.entry.delete(0, END)
                self.entry.focus()
                self.entry.config(justify='right')
                justify = self.entry.cget("justify")
                if justify=="right":
                    print("right")
                    add_bidi_support(self.entry)

            else:
                # Change the language to English
                self.entry.delete(0, END)
                self.entry.focus()
                self.entry.config(justify='left')

        else:
            if selection == "ar to en":
                # Change the language to Arabic
                text = self.entry.get()
                self.entry.delete(0, END)
                self.entry.focus()
                self.entry.config(justify='right')
                justify = self.entry.cget("justify")
                if justify == "right":
                    print("right")
                    add_bidi_support(self.entry)
            else:
                # Change the language to English
                self.entry.delete(0, END)
                self.entry.focus()
                self.entry.config(justify='left')

        print(selection)

    def on_radio_button_selected(self):
        self.option_langue['menu'].delete(0, 'end')
        if self.choice_langue.get() == 'en':
            print("option 1")
            self.option_langue['menu'].add_command(label="Ar to En", command=lambda: self.on_conversion_type_selected("Ar to En"))
            self.option_langue['menu'].add_command(label="En to Ar", command=lambda: self.on_conversion_type_selected("En to Ar"))

        else :
            print("option 2")

            self.option_langue['menu'].add_command(label="en to ar", command=lambda: self.on_conversion_type_selected("en to ar"))
            self.option_langue['menu'].add_command(label="ar to en", command=lambda: self.on_conversion_type_selected("ar to en"))

    def on_closing(self):
        if msg.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            exit()
    def create_widgets(self):
        # create the context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_command(label="Delete", command=self.delete_text)
        self.context_menu.add_command(label="Select All", command=self.select_all)

        # bind the context menu to each widget individually
        widgets = [self.answerText, self.english_answer, self.python_answer, self.entry]
        for widget in widgets:
            widget.bind("<Button-3>", self.show_context_menu)
            widget.bind("<KeyRelease>", self.update_context_menu)
            widget.bind("<Button-1>", self.hide_context_menu)
            # bind the left button to hide the menu

    def update_context_menu(self, event):
        # enable or disable the copy, cut, delete, and select-all options based on whether text is selected
        self.widget = event.widget
        if isinstance(self.widget, Text):
            has_selection = len(self.widget.tag_ranges("sel")) != 0
            if has_selection:
                self.context_menu.entryconfigure("Cut", state=NORMAL)
                self.context_menu.entryconfigure("Copy", state=NORMAL)
                self.context_menu.entryconfigure("Delete", state=NORMAL)
                self.context_menu.entryconfigure("Select All", state=NORMAL)
            else:
                self.context_menu.entryconfigure("Cut", state=DISABLED)
                self.context_menu.entryconfigure("Copy", state=DISABLED)
                self.context_menu.entryconfigure("Delete", state=DISABLED)
                self.context_menu.entryconfigure("Select All", state=NORMAL)
        elif isinstance(self.widget, Entry):
            if isinstance(self.widget, Entry) and len(self.widget.get()) > 0:
                self.context_menu.entryconfigure("Cut", state=NORMAL)
                self.context_menu.entryconfigure("Copy", state=NORMAL)
                self.context_menu.entryconfigure("Paste", state=NORMAL)
                self.context_menu.entryconfigure("Delete", state=NORMAL)
                self.context_menu.entryconfigure("Select All", state=NORMAL)
            else:
                self.context_menu.entryconfigure("Cut", state=DISABLED)
                self.context_menu.entryconfigure("Copy", state=DISABLED)
                self.context_menu.entryconfigure("Paste", state=NORMAL)
                self.context_menu.entryconfigure("Delete", state=DISABLED)
                self.context_menu.entryconfigure("Select All", state=NORMAL)

    def show_context_menu(self, event):
        # show the context menu at the current mouse position
        self.widget = event.widget
        self.update_context_menu(event)
        self.context_menu.post(event.x_root, event.y_root)

    def hide_context_menu(self, event):
        # hide the context menu if it's currently shown
        if self.context_menu:
            self.context_menu.unpost()
    def cut_text(self):
        self.widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.widget.event_generate("<<Paste>>")

    def select_all(self):
        self.widget.event_generate("<<SelectAll>>")

    def delete_text(self):
        self.widget.event_generate("<<Clear>>")
    def normal_answer(self):
        self.answerText.delete("1.0","end")
        self.english_answer.delete("1.0","end")
        self.python_answer.place_forget()
        self.button_clear_teminal.place_forget()
        self.button_run_python.place_forget()
        self.button_delete_code_text.place_forget()
    def clear_terminal(self):
        self.english_answer.delete("1.0","end")
    def delete_code(self):
        self.answerText.delete("1.0","end")
    def send_and_clear_entry(self,event=None):
        self.answerText.delete("1.0","end")
        self.english_answer.delete("1.0","end")
        self.python_answer.delete("1.0","end")
        self.get_question()
        self.entry.delete(0, "end")

    #animation functions
    def scroll_text(self):
        line = "<<<o>>>"

        self.delay = 100

        self.lines.append(line)
        if len(self.lines) > self.num_liness:
            self.text_widget.delete(1.0, 2.0)
            self.lines.pop(0)
        self.text_widget.insert("end", line)
        self.text_widget.yview_moveto(1.0)
        if len(self.lines) == self.num_liness:
            self.after(self.delay*10, self.reset_text_widget)
        else:
            self.after(self.delay, self.scroll_text)

    def reset_text_widget(self):
        self.lines = []
        self.text_widget.delete(1.0, END)
        self.after(self.delay, self.scroll_text)
        #end functions animation

    def run_code(self):
        # enable the stop button
        self.stop_flag.set(False)
        self.stop_code_button.place(x=340, y=250, relx=0.09, rely=0.0915425, anchor=W)

        self.english_answer.delete("1.0", "end")
        script = self.answerText.get("1.0", "end")
        text_widget = self.english_answer
        text_widget.insert(END, "Code is running...\n", 'start')
        text_widget.tag_config('start', foreground='green')
        text_widget.see(END)
        text_widget.update()
        # start a subprocess to execute the script and capture the output
        self.process = subprocess.Popen(['python', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        is_error = False
        stop_output = False  # initialize flag to False
        err = ''  # define err variable before the try block

        try:
            # read and insert the output into the text widget in real-time
            while not self.stop_flag.get():  # check flag at each iteration
                line = self.process.stdout.readline().decode()
                if not line:
                    break
                text_widget.insert(END, line)
                text_widget.see(END)
                text_widget.update()
        except Exception as e:
            is_error = True
            err = str(e)  # update err variable if there's an error
            tb = ''
            text_widget.insert(END, err, 'error')
            text_widget.insert(END, tb, 'error')
            text_widget.tag_config('error', foreground='red')
        finally:
            # wait for the subprocess to complete and get the return code
            return_code = self.process.wait()
            text_widget.insert(END, f"\nProcess finished with exit code {return_code}.", 'end')
            text_widget.tag_config('end', foreground='blue')
            text_widget.see(END)
            text_widget.update()

        if is_error or return_code != 0:
            return err, f"Process returned error code {return_code}.", None
        else:
            return None, None, text_widget.get("1.0", "end")


    def stop_output(self):
        self.stop_flag.set(True)
        if self.process is not None:
            self.process.terminate()
            self.stop_code_button.place_forget()

    def python_coding(self):
        self.answerText.delete("1.0","end")
        self.english_answer.delete("1.0","end")
        self.python_answer.place(x=0,y=250,relx=0.5, rely=0.308352365, anchor=CENTER)
        self.button_clear_teminal.place(x=0,y=250,relx=0.000009, rely=0.0915425, anchor=W)
        self.button_run_python.place(x=10,y=250,relx=0.95310793684327545, rely=0.0915425, anchor=W)
        self.button_delete_code_text.place(x=10,y=250,relx=0.5310793684327545, rely=0.0915425, anchor=W)



    def rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
    # Execute the Programm
    def execute(self,event=None):
        # Write the Content to the Temporary File
        with open('run.py', 'w', encoding='utf-8') as f:
            f.write(self.answerText.get('1.0', END))
        # Start the File in a new CMD Window
        os.system('start cmd /K "python run.py"')
    def changes(self,event=None):
        global previousText
        # If actually no self.changes have been made stop / return the self.functins
        if self.english_answer.get('1.0', END) == self.previousText:
            return
        # Remove all tags so they can be redrawn
        for tag in self.answerText.tag_names():
            self.answerText.tag_remove(tag, "1.0", "end")
        # Add tags where the self.search_re self.functins found the pattern
        i = 0
        for pattern, color in self.repl:
            for start, end in self.search_re(pattern, self.answerText.get('1.0', END)):
                self.answerText.tag_add(f'{i}', start, end)
                self.answerText.tag_config(f'{i}', foreground=color)
                i += 1
        self.previousText = self.answerText.get('1.0', END)

    def translate_arabic(self, text,question):
        translation_answer = translate(text, "ar")
        translation_question = translate(question, "ar")
        reshaped_answer = arabic_reshaper.reshape(translation_answer)
        reshaped_question = arabic_reshaper.reshape(translation_question)
        return reshaped_question,reshaped_answer
    def translate_english(self, text,question):
        translation_answer = translate(text, "en")
        translation_question = translate(question, "en")

        return translation_question,translation_answer

    def is_english_or_arabic(self,text):
        """
        Returns True if the given text is in English or Arabic, False otherwise.
        """
        lang = detect(text)
        return lang == 'en' or lang == 'ar'
    def sound_arabic(self,translation_answer):
        tts = gTTS(text=translation_answer, lang='ar')
        tts.save("arabic.mp3")
        tts.speed = 0.5
        subprocess.Popen(['mpg321', 'arabic.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def reset_tabstop(self,event):
        event.widget.configure(tabs=(event.width - 8, "right"))
    def search_re(self,pattern, text, groupid=0):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
                )
        return matches
    def exitNoah(self):
        self.destroy()

    def insert_arabic_slowly(self,text_window, text,question):

                    words = text.split()
                    # Iterate over the list of words and concatenate 10 words at a time
                    lines = []
                    for i in range(0, len(words), 6):
                        line = ' '.join(words[i:i + 6])
                        lines.append(line)
                    # Join the lines into a string
                    wrapped_text = '\n'.join(lines)
                    reshaped_text = arabic_reshaper.reshape(wrapped_text)
                    bidi_text_arabic = get_display(reshaped_text)
                    reshaped_question = arabic_reshaper.reshape(question)
                    bidi_text_question = get_display(reshaped_question)+"\n"
                    # create a Text widget and set the font, wrap, and justify options
                    text_window.tag_config("bidi_question_question", foreground="green")
                    text_window.insert("end", bidi_text_question, "bidi_question_question")
                    for i in range(len(bidi_text_arabic)):
                            # Update the widget to show the new text
                        word = bidi_text_arabic[i]
                        text_window.insert("end", word)
                        text_window.tag_add("reverse", "1.0", "end", )
                        text_window.tag_config("reverse", justify="right")
                        text_window.see("end")
                        text_window.update()  # Update the widget to show the new text
                        delay_ms = 25  # Delay between words in milliseconds
                        self.after(delay_ms)

    def insert_code_slowly(self,text_window, text,question):
        text_window.tag_config("question", foreground="green")
        text_window.insert("end", question+"\n", "question")
        for i in range(len(text)):
            char = text[i]
            text_window.insert(END, char)
            text_window.see(END)  # Scroll the text widget to show the newly inserted text
            text_window.update()  # Update the widget to show the new text
            delay_ms = 65  # Delay between characters in milliseconds
            self.after(delay_ms)
    def insert_english_slowly(self,text_window, text,question):
        text_window.tag_config("question", foreground="green")
        text_window.insert("end", question+ "\n", "question")
        for i in range(len(text)):
            char = text[i]
            text_window.insert(END, char)
            text_window.see(END)  # Scroll the text widget to show the newly inserted text
            text_window.update()  # Update the widget to show the new text
            delay_ms = 65  # Delay between characters in milliseconds
            self.after(delay_ms)
    def extract_python_code(self,text):
        code_blocks = []
        for match in re.findall(r"(.*?)```python(.*?)```(.*?)", text, re.DOTALL):
            code_block = match[1].strip()
            if code_block:
                code_blocks.append(code_block)
            cleaned_codes = [re.sub(r'^\s*python\s*', '', block).strip('`') for block in code_blocks]
            print(cleaned_codes)
        codes = ""
        for code in code_blocks:
            codes += f"\n{code}"
        return codes
    def get_question(self,event=None):

        question =self.entry.get()
        if question== "":
            print('is empty')
            msg.showwarning(message="enter your question")
            return


        if self.selected_option.get()==1:

            question=f"{question},explain the code and split the code alone with '```python```' "

        else:
            print("i use this 1")

            question = self.entry.get()
            print("this the real one : ",question)
        # create a Lock object
        if self.is_english_or_arabic(question)==True:
            ques,ans=self.translate_english("",question)
            print(ans,ques)
            request = self.generate_openai_response(ques)

        else:
            request = self.generate_openai_response(question)
        lock = threading.Lock()

        #get the txt only
        start_index = request.find("```python")
        end_index = request.find("```", start_index + 3)
        if start_index != -1 and end_index != -1:
            extracted_text = request[:start_index] + request[end_index + 3:]
        else:
            extracted_text = request
        print(extracted_text)
        if self.selected_option.get() == 1:

            if self.choice_langue.get() == "ar":
                print("i use this 2")
                question_arab=self.entry.get()
                question_arab,answer_arab = self.translate_arabic(extracted_text, question_arab)
                code = self.extract_python_code(request)
                self.insert_code_slowly(self.answerText, code, "")
                self.changes()
                self.sound_arabic(answer_arab)
                with lock:
                    threadArab = threading.Thread(target=self.insert_arabic_slowly,args=(self.python_answer, answer_arab, question_arab))
                    threadArab.start()
            else:
                code = self.extract_python_code(request)
                question=self.entry.get()
                self.insert_code_slowly(self.answerText, code, "")
                self.changes()
                text_to_speech(extracted_text)
                with lock:
                    thread2 = threading.Thread(target=self.insert_english_slowly,args=(self.python_answer, extracted_text, question))
                    thread2.start()
        else:
            if self.choice_langue.get()=="ar":
                print("i use this 3")
                question_arab = self.entry.get()
                check_langue=self.is_english_or_arabic(question_arab)
                print(check_langue)
                if check_langue == True:
                    print("i use number 4")

                    question_en, answer_en = self.translate_english(extracted_text, question_arab)
                    question_arab, answer_arab = self.translate_arabic(extracted_text, question_en)

                    self.sound_arabic(answer_arab)
                    with lock:
                        thread1 = threading.Thread(target=self.insert_arabic_slowly(self.answerText,answer_arab,question_arab))
                        thread2 = threading.Thread(target=self.insert_english_slowly(self.english_answer,answer_en,question_en))
                        thread2.start()
                        thread1.start()
                else:
                    print("i use number 5")

                    question_en, answer_en = self.translate_english(extracted_text, question_arab)

                    question_arab, answer_arab = self.translate_arabic(answer_en, question_en)
                    self.sound_arabic(answer_arab)
                    with lock:
                        thread1 = threading.Thread(target=self.insert_arabic_slowly(self.answerText,answer_arab,question_arab))
                        thread2 = threading.Thread(target=self.insert_english_slowly(self.english_answer,answer_en,question_en))
                        thread2.start()
                        thread1.start()
            else:
                print("i use this 6")
                question_arab = self.entry.get()
                check_langue=self.is_english_or_arabic(question_arab)
                print(check_langue)
                if check_langue == True:
                    print("i use number 7")
                    question_en, answer_en = self.translate_english(extracted_text, question_arab)
                    question_arab, answer_arab = self.translate_arabic(extracted_text, question_en)
                    text_to_speech(extracted_text)
                    with lock:
                        thread1 = threading.Thread(
                            target=self.insert_arabic_slowly(self.answerText, answer_arab, question_arab))
                        thread2 = threading.Thread(
                            target=self.insert_english_slowly(self.english_answer, answer_en, question_en))
                        thread2.start()
                        thread1.start()
                else:
                    print("i use number 8")
                    question_en, answer_en = self.translate_english(extracted_text, question_arab)

                    question_arab, answer_arab = self.translate_arabic(answer_en, question_en)
                    text_to_speech(extracted_text)
                    with lock:
                        thread1 = threading.Thread(target=self.insert_arabic_slowly(self.answerText,answer_arab,question_arab))
                        thread2 = threading.Thread(target=self.insert_english_slowly(self.english_answer,answer_en,question_en))
                        thread2.start()
                        thread1.start()
    def get_speech_input(self,event=None):
        # Initialize speech recognizer
        r = sr.Recognizer()
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source)
            # Prompt user to start speaking
            print("Speak now...")
            # Record audio
            audio = r.listen(source)
        try:
            # Convert speech to text
            text = r.recognize_google(audio)
            print(text)
            if text == None:
                self.get_speech_input()
            # Return the text of the speech
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")

            return
        except sr.RequestError:
            print("Sorry, I'm having trouble connecting to the speech recognition service.")
            return

    def text_to_text(self,window,ans,ask):
        self.insert_arabic_slowly(window,ans,ask)






    def generate_openai_response(self,text_input):
        prompt = f" {text_input}"
        print("Prompt:", prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        answer = response['choices'][0]['text']

        return answer


if __name__ == '__main__':
    noah = Noah()
    noah.title("Noah Chat")
    noah.geometry("1030x644")
    noah.resizable(width=False, height=False)
    noah.deiconify()

    noah.mainloop()


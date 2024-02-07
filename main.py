import json
import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox
import os
import random
import subprocess


def load(subject, topic):
    with open(f"subjects/{subject}.json", "r") as retrieve:
        data = json.load(retrieve)[topic]
    questions = []
    for i in data:
        pair = (i, data[i])
        questions.append(pair)
    return questions


def check(attempt, answer, threshold=2):
    answer = answer.replace(" ", "")
    attempt = attempt.replace(" ", "")
    threshold = len(answer) - threshold
    answer = [*answer]
    correct = 0
    for i in attempt:
        if i in answer:
            correct += 1
            answer.remove(i)
        else:
            print(i)

    return correct > threshold


def clear(frame):
    for item in frame.winfo_children():
        item.destroy()


def menu(frame):
    clear(frame)
    baseY = 200
    titleText = "Select an Option"
    title = tkinter.Label(frame, text=titleText, font=("Helvetica", 20, "bold"))
    title.place(relx=0, y=20, width=500, height=50)

    # Test Button
    startText = "Test Yourself"
    testYourself = tkinter.Button(frame, text=startText, font=("Helvetica", 20), command=lambda: selection(frame))
    testYourself.place(x=50, y=baseY, width=400, height=50)

    # Add Button
    addText = "Add More Question Sets"
    addButton = tkinter.Button(frame, text=addText, font=("Helvetica", 20), command=lambda: addMenu(frame))
    addButton.place(x=50, y=baseY + 55, width=400, height=50)

    # View Button
    viewText = "View All Question Sets"
    viewButton = tkinter.Button(frame, text=viewText, font=("Helvetica", 20))
    viewButton.place(x=50, y=baseY + 110, width=400, height=50)

    # Remove Button
    removeText = "Remove a Question Set"
    removeButton = tkinter.Button(frame, text=removeText, font=("Helvetica", 20), command=lambda: remove_menu(frame))
    removeButton.place(x=50, y=baseY + 165, width=400, height=50)


# QUIZ =================================================================================================================
def selection(frame):
    clear(frame)

    # Getting Subjects
    options = ["Select an option"]
    for subject in os.listdir("subjects"):
        if subject.split(".")[1] == "json":
            options.append(subject.split(".")[0].title())

    # Title
    title = tkinter.Label(frame, text="Select a Subject and a Topic", font=("Helvetica", 20, "bold"))
    title.pack(pady=10)

    # Topic Box
    tkinter.Label(frame, text="Select a Topic", font=("Helvetica", 12, "bold")).place(x=105, y=215)
    topicSelect = ttk.Combobox(frame, values=["Select an Option"], state="disabled", width=42)
    topicSelect.current(0)
    topicSelect.place(x=105, y=250)

    # Subject Box
    tkinter.Label(frame, text="Select a Subject", font=("Helvetica", 12, "bold")).place(x=105, y=115)
    subjectSelect = ttk.Combobox(frame, values=options, width=20, font=("Helvetica", 10), state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=105, y=150)

    # Subject Button
    subjectButton = tkinter.Button(frame, text="Select",
                                   command=lambda: subject_check(subjectSelect.get(), topicSelect))
    subjectButton.place(x=275, y=150, width=100, height=22)

    # Start Button
    startButton = tkinter.Button(frame, text="Start", font=("Helvetica", 20), command=lambda: \
        questionGrab(frame, subjectSelect.get(), topicSelect.get()))
    startButton.place(x=105, y=350, width=280, height=50)

    # Return to Menu
    returnButton = tkinter.Button(frame, text="Menu", command=lambda: menu(frame))
    returnButton.place(x=10, y=470, width=50, height=25)


def subject_check(value, box):
    if value != "Select an option":
        box["state"] = "readonly"
        topics = ["Select an option"]
        with open(f"subjects/{value}.json", "r") as topicList:
            data = json.load(topicList)
            for topic in data:
                topics.append(topic)
        box["values"] = topics
    else:
        box['state'] = "disabled"
        box["values"] = ["Select an Option"]
        box.current(0)


def questionGrab(frame, subject, topic):
    try:
        questions = load(subject.lower(), topic.lower())
    except KeyError as e:
        tkinter.Label(frame, text="Select a valid topic", fg="red").place(x=105, y=400, width=280)
        print(e)
    except FileNotFoundError as e:
        print(e)
        tkinter.Label(frame, text="Select a valid subject", fg="red").place(x=105, y=400, width=280)
    else:
        quiz(frame, questions)


def quiz(frame, questions, questionNumber=1, correct=0, incorrect=0):
    clear(frame)
    random.shuffle(questions)
    title = tkinter.Label(frame, text=f"Question {questionNumber}", font=("Helvetica", 20, "bold"))
    title.place(x=0, y=10, width=500, height=50)

    if questions:
        questionAnswer = questions.pop(0)

        question = tkinter.Label(frame, text=questionAnswer[0], font=("Helvetica", 18), wraplength=455)
        question.place(x=0, y=100, width=500, height=150)

        answerBox = tkinter.Entry(frame, font=("Helvetica", 18), justify="center")
        answerBox.place(x=50, y=300, height=50, width=400)

        submitButton = tkinter.Button(frame, text="Submit", font=("Helvetica", 15),
                                      command=lambda: quiz_check(frame, answerBox.get(), questionAnswer, questions,
                                                                 questionNumber, correct, incorrect))
        submitButton.place(x=150, y=360, height=40, width=200)

        returnButton = tkinter.Button(frame, text="Return", command=lambda: selection(frame))
        returnButton.place(x=10, y=470, width=50, height=25)
    else:
        quizComplete(frame, correct, incorrect)


def quiz_check(frame, entered, questionAnswer, questions, questionNumber, correct, incorrect):
    right = check(entered.lower(), questionAnswer[1])
    questionNumber += 1
    if right:
        correctLabel = (tkinter.Label(frame, text="Correct", fg="green", font=("Helvetica", 12)))
        correctLabel.place(x=0, y=270, width=500, height=30)
        correct += 1
    else:
        incorrectText = f"Incorrect, it was {questionAnswer[1]}"
        incorrectLabel = tkinter.Label(frame, text=incorrectText, fg="red", font=("Helvetica", 12))
        incorrectLabel.place(x=0, y=270, width=500, height=30)
        incorrect += 1

    continueButton = tkinter.Button(frame, text="Continue", font=("Helvetica", 10),
                                    command=lambda: quiz(frame, questions, questionNumber, correct, incorrect))
    continueButton.place(x=200, y=405, width=100, height=30)


def quizComplete(frame, correct, incorrect):
    clear(frame)
    tkinter.Label(frame, text="Quiz Complete", font=("Helvetica", 25, "bold")).pack()
    correctAnswered = tkinter.Label(frame, text=f"{correct} correctly answered", font=("Helvetica", 20), fg="green")
    correctAnswered.place(x=0, y=200, width=500, height=50)
    incorrectAnswered = tkinter.Label(frame, text=f"{incorrect} incorrectly answered", font=("Helvetica", 20), fg="red")
    incorrectAnswered.place(x=0, y=250, width=500, height=50)
    menuReturn = tkinter.Button(frame, text="Return to menu", font=("Helvetica", 18), command=lambda: menu(frame))
    menuReturn.place(x=150, y=350, width=200, height=50)


# ADDING ===============================================================================================================
def addMenu(frame):
    clear(frame)
    title = tkinter.Label(frame, text="Add a New Study Set", font=("Helvetica", 20, "bold"))
    title.pack(pady=10)

    howToText = """
    1. create a text file anywhere on your computer\n
    2. name the file <topic name>.txt\n
    3. type the question then the answer with a separator between them\n
    4. copy/paste the text file location into the box\n
    TIP: keep any text files in a folder so you can redo\nthem if something goes wrong
    """

    info = tkinter.Label(frame, text=howToText, font=("Helvetica", 12))
    info.place(x=0, y=50, width=500, height=180)

    returnButton = tkinter.Button(frame, text="Menu", command=lambda: menu(frame))
    returnButton.place(x=10, y=470, width=50, height=25)

    subjectTitle = tkinter.Label(frame, text="Enter the name of the subject", font=("Helvetica", 10))
    subjectTitle.place(x=50, y=250)
    subject = tkinter.Entry(frame, justify="center", font=("Helvetica", 13))
    subject.place(x=50, y=270, width=225, height=30)

    separatorTitle = tkinter.Label(frame, text="Select the separator", font=("Helvetica", 10))
    separatorTitle.place(x=300, y=250)
    separators = ["Select an Option", "/", ",", ".", "-", "_"]
    separator = ttk.Combobox(frame, values=separators, state="readonly")
    separator.current(0)
    separator.place(x=300, y=275)

    fileTitle = tkinter.Label(frame, text="Enter the file location", font=("Helvetica", 10))
    fileTitle.place(x=50, y=320)
    location = tkinter.Entry(frame, justify="center", font=("Helvetica", 15))
    location.place(x=50, y=340, width=400, height=40)

    addSubmit = tkinter.Button(frame, text="Submit", font=("Helvetica", 13),
                               command=lambda: addChecks(frame, subject.get(), separator.get(), location.get(),
                                                         subjectTitle, separatorTitle, fileTitle))
    addSubmit.place(x=150, y=410, width=200, height=30)


def addChecks(frame, subject, separator, filename, sub, sep, file):
    tiptop = True
    filename = filename.strip('"')

    # is a separator selected
    if separator == "Select an Option":
        sep["fg"] = "red"
        tiptop = False
    else:
        sep["fg"] = "black"

    # has a file been entered
    if not filename:
        tiptop = False
        file["fg"] = "red"
    else:
        file["fg"] = "black"

    # has a subject been entered
    if not subject:
        tiptop = False
        sub["fg"] = "red"
    else:
        sub["fg"] = "black"

    # does the text file exist
    fName = filename.split(".")[0]
    try:
        test = open(f"{fName}.txt", "r")
        test.close()
    except FileNotFoundError:
        file["fg"] = "red"
        tiptop = False
    else:
        file["fg"] = "black"

    # does the json file exist
    rawName = fName.split("\\")[-1].split(".")[0].lower()
    if os.path.exists(f"subjects/{subject}.json"):
        if subject:
            with open(f"subjects/{subject}.json", "r") as find:
                search = json.load(find)
                exists = False
                for i in search:
                    if i == rawName:
                        tkinter.Label(frame, text=f"A topic with that name already exists under {subject}",
                                      fg="red").place(x=0, y=380, width=500)
                        tiptop = False
                        exists = True
                if not exists:
                    tkinter.Label(frame, text="", fg="red").place(x=0, y=380, width=500)
        else:
            tiptop = False

    if tiptop:
        add(frame, subject, rawName, filename, separator)


def add(frame, subject, topic, path, separator):
    with open(path, "r") as pull:
        full = pull.readlines()
        questions = [i.split(separator)[0].strip() for i in full]
        answers = [i.split(separator)[1].strip() for i in full]
    info = {}
    for q, a in zip(questions, answers):
        info[q] = a
    print(info)
    if not os.path.exists(f"subjects/{subject}.json"):
        with open(f"subjects/{subject}.json", "w") as create:
            json.dump({}, create)
    with open(f"subjects/{subject}.json", "r") as get:
        current = json.load(get)
    current[topic] = info
    try:
        with open(f"subjects/{subject}.json", "w") as send:
            json.dump(current, send)
    except Exception:
        tkinter.Label(frame, text="Error adding set", fg="red").place(x=0, y=450, width=500)
    else:
        tkinter.Label(frame, text="Set added successfully", fg="green").place(x=0, y=450, width=500)


# REMOVE ===============================================================================================================
def remove_menu(frame):
    clear(frame)

    tkinter.Label(frame, text="Remove a Set", font=("Helvetica", 20, "bold")).pack()
    returnButton = tkinter.Button(frame, text="Menu", command=lambda: menu(frame))
    returnButton.place(x=10, y=470, width=50, height=25)

    options = ["Select an option"]
    for subject in os.listdir("subjects"):
        if subject.split(".")[1] == "json":
            options.append(subject.split(".")[0].title())

    topicLabel = tkinter.Label(frame, text="Select the topic you want to delete", font=("Helvetica", 12, "bold"))
    topicLabel.place(x=0, y=250, width=500)
    topicSelect = ttk.Combobox(frame, values=["Select an Option"], state="disabled", width=51)
    topicSelect.current(0)
    topicSelect.place(x=85, y=280)

    subjectLabel = tkinter.Label(frame, text="Select the subject to delete from", font=("Helvetica", 12, "bold"))
    subjectLabel.place(x=0, y=120, width=500)
    subjectSelect = ttk.Combobox(frame, values=options, width=30, state="readonly")
    subjectSelect.current(0)
    subjectSelect.place(x=85, y=150)

    subButton = tkinter.Button(frame, text="Select", command=lambda: remove_check(subjectSelect.get(), topicSelect))
    subButton.place(x=315, y=150, height=22, width=100)

    submitButton = tkinter.Button(frame, text="Delete", font=("Helvetica", 15),
                                  command=lambda: delete(frame, subjectSelect.get().lower(), topicSelect.get()))
    submitButton.place(x=150, y=320, width=200, height=40)

    tkinter.Label(frame, text="Alternatively, open the folder and edit the JSON file").place(x=0, y=400, width=500)
    fileButton = tkinter.Button(frame, text="Open Folder", font=("Helvetica", 15),
                                command=lambda: subprocess.Popen('explorer "subjects"'))
    fileButton.place(x=175, y=430, width=150, height=40)


def remove_check(value, box):
    if value != "Select an option":
        box["state"] = "readonly"
        topics = ["Select an option", "All of it"]
        with open(f"subjects/{value}.json", "r") as topicList:
            data = json.load(topicList)
            for topic in data:
                topics.append(topic)
        box["values"] = topics
    else:
        box['state'] = "disabled"
        box["values"] = ["Select an Option"]
        box.current(0)


def delete(frame, subject, topic):
    print()

    if topic == "All of it":
        if tkinter.messagebox.askyesno("Warning", f"Do you want to delete {subject}?"):
            try:
                os.remove(f"subjects/{subject}.json")
            except FileNotFoundError:
                tkinter.Label(frame, text="This subject doesn't exist", fg="red").place(x=0, y=370, width=500)
            else:
                tkinter.Label(frame, text="Subject deleted successfully", fg="green").place(x=0, y=370, width=500)
    else:
        if tkinter.messagebox.askyesno("Warning", f"Do you want to delete {topic}?"):
            try:
                with open(f"subjects/{subject}.json", "r") as retrieve:
                    data = json.load(retrieve)
                del data[topic]
                with open(f"subjects/{subject}.json", "w") as update:
                    json.dump(data, update)
            except KeyError:
                tkinter.Label(frame, text="This topic doesn't exist", fg="red").place(x=0, y=370, width=500)
            else:
                tkinter.Label(frame, text="Topic deleted successfully", fg="green").place(x=0, y=370, width=500)


# MAIN =================================================================================================================
splashRoot = tkinter.Tk()
splashRoot.geometry(f"200x200")
splashRoot.title("")
nerd = tkinter.PhotoImage(file="assets/nerd.png")
tkinter.Label(splashRoot, image=nerd).pack()

splashRoot.after(500, lambda: main(splashRoot))


def main(splash):
    splash.destroy()
    root = tkinter.Tk()
    root.iconbitmap("assets/nerd.ico")
    root.title("Academic Weaponiser")
    root.geometry("500x500")
    root.resizable(False, False)
    menu(root)


tkinter.mainloop()

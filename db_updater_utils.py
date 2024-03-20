import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os


def add_menu(app):
    menubar = tk.Menu(app)
    app.config(menu=menubar)

    menu1 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", underline=0, menu=menu1)
    menu1.add_separator()
    menu1.add_command(label="Open your mind", underline=1, command=None)
    menu1.add_separator()

    def close_app():
        app.destroy()

    menu1.add_command(label="Exit", underline=1, command=close_app)


def add_name_widget(top_frame):
    # define label
    name_title = tk.Label(top_frame, text=" Your Name:", width=10, anchor= "center" )
    name_title.pack({"side": "top"})

    # define entry box
    name = tk.Entry(top_frame, fg="yellow", background="medium blue", width=23 )
    name.pack({"side": "top"})
       
    return name


def add_research_area(app, top_frame):

    research_area_title = tk.Label(top_frame, text="Area of research:", width=15, anchor= "center" )
    research_area_title.pack({"side": "top"})

    research_area = ["Cell biology", "Molecular Biology", "Epigenetics", "Bioinformatics", "Immunology", "Genetics"]

    main_area_of_interest = ttk.Combobox(app,  values=research_area, width=20)
    main_area_of_interest.pack({"side": "top"})

    return main_area_of_interest


def add_cancer_types_list(app):
   
    list_box_title = tk.Label(app, text="Cancer types: ", width=15, anchor= "center" )
    list_box_title.pack({"side": "top"})
   
    list_box = tk.Listbox(app, selectmode=tk.MULTIPLE, background="seagreen1", width=23, height=5)
    cancer_types = ['Breast cancer', 'DCIS', 'Colorectal cancer', 'Glioblastoma', 'Melanoma', 
                    'Ovarian cancer', 'Cervical Cancer', 'HGSC', 'Bone Cancer', 'Ewing Sarcoma', 
                    'Lymphoma', 'Leukemia', 'Lung Cancer', 'Liver Cancer', 'Testicular Cancer']
    
    for val in cancer_types:
        list_box.insert(tk.END, val)
    list_box.pack()

    return list_box


def add_checkboxes(app):
    checkboxes = tk.Frame(app)
    checkboxes.pack()
    subjects = []
    checkboxes = tk.LabelFrame(app, text="Subjects of interest: ", width=15, height=20)
    checkboxes.pack({"side": "top"})
   
    subjects_names = ["Mass spectrometry", "Proteomics", "Single cell", "Intra-tumor heterogeneity", 
                      "Tumour heterogeneity", "Tumour enviorment", "Multi-omics", "Spatial proteomics", 
                     "Computational", "High-throughput", "Precision medicine", 
                    "Prognostic oncology", "Immunotherapy", "Proteogenomics"]

    for subjects_name in subjects_names:
        subjects_var = tk.BooleanVar()
        subjects.append(subjects_var)
        checkbox = tk.Checkbutton(checkboxes, text=subjects_name, variable=subjects_var, relief="groove", background="seagreen2", anchor = 'w' )
        checkbox.pack(side="top", fill="both", expand=2)
       
    return subjects, subjects_names


def add_email_widget(app):
    email_title = tk.Label(app, text="E-mail:", width=5, anchor= "w", height=1 )
    email_title.pack({"side": "top"})

    email = tk.Entry(app, fg="black", background="lemon chiffon", width=60 )
    email.pack({"side": "top"})
    return email


def generate_output_window_text(name, main_area_of_interest, current_selected_list_box, current_selected_subjects, email):
    text = ""
    text += "Name: {}\n".format(name.get())
    
    text += "Research area: {}\n".format(main_area_of_interest.get())    
    
    text += "Cancer type: "
    text += current_selected_list_box
    text += "\n"

    text += "Subjects of interest: "
    text += current_selected_subjects
    text += "\n"

    text += "E-mail: {}\n".format(email.get())

    return text


def submit_preferences(app, name, main_area_of_interest, list_box, subjects, subjects_names, email, output_window):
    
    # summarize list_box and subjects
    selected = list_box.curselection()  # returns a tuple
    current_selected_list_box = ', '.join([list_box.get(idx) for idx in selected])

    current_selected_subjects = []
    for ix in range(len(subjects)):
        if subjects[ix].get():
            current_selected_subjects.append(subjects_names[ix])
    current_selected_subjects = ', '.join(current_selected_subjects)
    

    # generate summary text
    text = generate_output_window_text(name, main_area_of_interest, current_selected_list_box, current_selected_subjects, email)

    # popup window
    resp = messagebox.askquestion(title="Save preferences to database", message=f"Save the following areas of interest?\n\n{text}")

    if resp == 'yes':
        # print to output_window
        output_window['state'] = 'normal'  
        output_window.insert('end', f"{text}\n--------\n")
        output_window['state'] = 'disabled'  
        output_window.see('end')  
        app.update()

        # save to DB
        if not os.path.exists('data/looper_db.csv'):
            db_table= pd.DataFrame(columns=['Name','Email','Area of research','Cancer type','Selected subjects'])
        else:
            db_table = pd.read_csv('data/looper_db.csv')

        db_table.loc[len(db_table.index)] = [name.get(), email.get() , main_area_of_interest.get(), current_selected_list_box, current_selected_subjects]  
        db_table.to_csv('data/looper_db.csv',index=False)




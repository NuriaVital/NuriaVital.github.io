import tkinter as tk
import db_updater_utils

def setup_main_frame():
    app = tk.Tk()
    app.title('Looper. Kepps you in the loop.')
    app.geometry("700x800")

    db_updater_utils.add_menu(app)

    top_frame = tk.Frame(app)
    top_frame.pack(side="top")

    name = db_updater_utils.add_name_widget(top_frame)
    main_area_of_interest = db_updater_utils.add_research_area(app, top_frame)
    list_box = db_updater_utils.add_cancer_types_list(app)
    subjects, subjects_names = db_updater_utils.add_checkboxes(app)
    email = db_updater_utils.add_email_widget(app)

    output_frame = tk.Frame(app)
    output_frame.pack()
    output_window = tk.Text(output_frame, state='disabled', background="royalblue1", width=70, height=10)
    output_window.pack()
    buttons = tk.Frame(app)
    buttons.pack()
    
    action_button = tk.Button(buttons, text="Submit", command=lambda: db_updater_utils.submit_preferences(app, name, main_area_of_interest, list_box, subjects, subjects_names, email,output_window))
    action_button.pack()

    app.mainloop()


if __name__ == "__main__":
    setup_main_frame()
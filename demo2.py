import customtkinter as ctk

from CTK_Alert.components import CTkAlert, CTkBanner, CTkNotification

ctk.set_appearance_mode("dark")
text_temp = "Hello World!sdfsdf\nHello World!\nHello World!\nHello World!\nHello World!\nHello World!\nHello World!"
len_txt = 200 + len(text_temp.split("\n")) * 10


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")

        self.button1 = ctk.CTkButton(self, text="alert", command=self.alert)
        self.button1.pack(padx=20, pady=20)

        self.button2 = ctk.CTkButton(self, text="banner", command=self.banner)
        self.button2.pack(padx=20, pady=20)

        self.button3 = ctk.CTkButton(self, text="notification", command=self.notification)
        self.button3.pack(padx=20, pady=20)

    def alert(self):
        my_alert = CTkAlert(state="info", body_text=text_temp, btn1="Ok", height=len_txt)
        answer = my_alert.get()  # get answer
        print(answer)

    def banner(self):
        my_banner = CTkBanner(self, state="info", title="Title",
                              btn1="Action 1", btn2="Action 2", side="right_bottom")
        answer = my_banner.get()  # get answer
        print(answer)

    def notification(self):
        CTkNotification(self, state="info", message="message", side="right_bottom")


if __name__ == '__main__':
    app = App()
    app.mainloop()

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


root = ctk.CTk()
root.title("CvGenerator - Brox")
root.geometry("1100x550")
root.resizable(False, False)
font = ("Helvetica", 12)
fontbold = ("Helvetica", 12, "bold")
avatar_image_path = None

heading_style = ParagraphStyle(
    name='Heading1',
    fontName='Helvetica-Bold',
    fontSize=18,
    textColor=HexColor('#0033A0'),
    spaceAfter=12,
    alignment=1
)

body_style = ParagraphStyle(
    name='Body',
    fontName='Helvetica',
    fontSize=12,
    textColor=HexColor('#333333'),
    spaceAfter=6,
)

def wrap_text(pdf, text, x, y, max_width, font_name='fontMed', font_size=10):
    pdf.setFont(font_name, font_size)
    wrapped_text = []
    
    while text:
        for i in range(len(text), 0, -1):
            if pdf.stringWidth(text[:i], font_name, font_size) <= max_width:
                wrapped_text.append(text[:i])
                text = text[i:].strip()
                break
    
    for line in wrapped_text:
        pdf.drawString(x, y, line)
        y -= font_size + 2
    
    return y

def generateCV(fName, lName, Email, Pnum, Location, Role, Education, Skills, Language, Profile, Work, Experience, Work2, Experince2, Color):

    pdfmetrics.registerFont(TTFont('fontBolde', 'Jost-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('fontMed', 'Jost-Medium.ttf'))

    firstName = fName.get()
    lastName = lName.get()
    email = Email.get()
    phoneNumber = Pnum.get()
    location = Location.get()
    mainrole = Role.get()
    education = Education.get()
    skilling = Skills.get()
    languages = Language.get()
    profiledesc = Profile.get()
    working1 = Work.get()
    experiencing1 = Experience.get()
    working2 = Work2.get()
    experiencing2 = Experince2.get()
    colorcode = Color.get()

    if colorcode == "":
        colorcode = "#002D4A"

    skill_list = [skill.strip() for skill in skilling.split('.') if skill.strip()]
    language_list = [lang.strip() for lang in languages.split('.') if lang.strip()]

    if all([firstName, lastName, email, phoneNumber, location, mainrole, education, skilling, languages, profiledesc, working1, experiencing1, colorcode]):

        pdf_filename = f"{firstName}_{lastName}_CV.pdf"
        pdf = canvas.Canvas(pdf_filename, pagesize=A4)

        pdf.setFillColor(HexColor(colorcode))
        pdf.rect(0, 0, 200, A4[1], stroke=0, fill=1)

        if avatar_image_path:
            print(f"Avatar image path: {avatar_image_path}")
            pdf.drawImage(avatar_image_path, 40, 715, width=1.5*inch, height=1.5*inch)


        pdf.setFont('fontBolde', 14)
        pdf.setFillColor(HexColor('#FFFFFF'))
        pdf.drawString(30, 690, "CONTACT")
        pdf.setStrokeColor("#ffffff")
        pdf.setLineWidth(1)
        pdf.line(30, 680, 160, 680)

        pdf.setFont('fontMed', 10)  
        pdf.drawString(30, 665, f"Phone : {phoneNumber}")
        pdf.drawString(30, 650, f"Email : {email}")
        pdf.drawString(30, 635, f"Location : {location}")
        pdf.drawString(30, 620, f"Website : www.{firstName}.com")

        pdf.setFont('fontBolde', 14)
        pdf.drawString(30, 570, "EDUCATION")
        pdf.setStrokeColor("#ffffff")
        pdf.line(30, 560, 160, 560)

        wrap_text(pdf, education, 30, 540, max_width=130)

        pdf.setFont('fontBolde', 12)
        pdf.drawString(30, 500, "SKILLS")
        pdf.setStrokeColor("#ffffff")
        pdf.line(30, 490, 160, 490)

        pdf.setFont('fontMed', 10)
        y_pos = 475
        for skill in skill_list:
            pdf.drawString(30, y_pos, f"{skill}")
            y_pos -= 20

        pdf.setFont('fontBolde', 12)
        pdf.drawString(30, y_pos - 40, "LANGUAGES")
        pdf.setStrokeColor("#ffffff")
        pdf.line(30, y_pos - 50, 160, y_pos - 50)

        pdf.setFont('fontMed', 10)
        y_pos -= 65
        for lang in language_list:
            pdf.drawString(30, y_pos, f"{lang}")
            y_pos -= 20


        pdf.setFont('fontBolde', 12)
        pdf.setFillColor(HexColor(colorcode))
        pdf.drawString(240, 690, "PROFILE")

        pdf.setStrokeColor(colorcode)
        pdf.setLineWidth(1)
        pdf.line(240, 680, 560, 680)
        pdf.setFillColor(HexColor('#333333'))
        y_profile = wrap_text(pdf, profiledesc, 240, 660, max_width=310)

        y_work_experience = y_profile - 40

        pdf.setFont('fontBolde', 12)
        pdf.setFillColor(HexColor(colorcode))
        pdf.drawString(240, y_work_experience, "WORK EXPERIENCE")
        pdf.setStrokeColor(colorcode)
        pdf.line(240, y_work_experience - 10, 560, y_work_experience - 10)

        pdf.setFont('fontBolde', 12)
        y_work_experience -= 30
        pdf.drawString(240, y_work_experience, f"First Work : {working1}")
        pdf.line(240, y_work_experience - 2, 290, y_work_experience - 2)

        pdf.setFont('fontMed', 10)
        y_work_experience = wrap_text(pdf, f"Experience: {experiencing1}", 240, y_work_experience - 15, max_width=310)

        pdf.setFont('fontBolde', 12)
        y_work_experience -= 30
        pdf.drawString(240, y_work_experience, f"Second Work : {working2}")
        pdf.line(240, y_work_experience - 2, 290, y_work_experience - 2)

        pdf.setFont('fontMed', 10)
        y_work_experience = wrap_text(pdf, f"Experience: {experiencing2}", 240, y_work_experience - 15, max_width=310)


        pdf.setFont('fontBolde', 30)
        pdf.setFillColor(HexColor('#5D5D5D'))
        pdf.drawString(260, 780, f"{firstName}")

        pdf.setFont('fontMed', 30)
        pdf.setFillColor(HexColor(colorcode))
        pdf.drawString(395, 780, f"{lastName}")

        pdf.setFont('fontMed', 15)
        pdf.setFillColor(HexColor(colorcode))
        pdf.drawString(260, 760, f"{mainrole}")

        pdf.setStrokeColor(colorcode)
        pdf.setLineWidth(2)
        pdf.line(260, 750, 300, 750)

        pdf.save()

        print(f"CV successfully generated as {pdf_filename}")
        messagebox.showinfo("Success", "CV Generated Successfully!")
    else:
        messagebox.showerror("Error", "Please fill all the information")

def uploadAvatar():
    global avatar_image_path

    avatar_image_path = filedialog.askopenfilename(
        title="Select Avatar Image", 
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if avatar_image_path:
        avatar_image = Image.open(avatar_image_path)
        
        avatar_image = avatar_image.resize((150, 150))
        
        avatar_tk_image = ImageTk.PhotoImage(avatar_image)
        
        avatar_label = ctk.CTkLabel(root, image=avatar_tk_image, text="")
        avatar_label.image = avatar_tk_image
        avatar_label.place(x=910, y=50)

def quit_program():
    root.destroy()

def createTheWindow():

    ##------------------Entry's And Labels
    ctk.CTkLabel(root, text="Your First Name", font=fontbold).place(x=30, y=20)
    fName_entry = ctk.CTkEntry(root, font=font)
    fName_entry.place(x=30, y=50)

    ctk.CTkLabel(root, text="Your Last Name", font=fontbold).place(x=30, y=90)
    lName_entry = ctk.CTkEntry(root, font=font)
    lName_entry.place(x=30, y=120)

    ctk.CTkLabel(root, text="Your Email", font=fontbold).place(x=30, y=160)
    Email_entry = ctk.CTkEntry(root, font=font)
    Email_entry.place(x=30, y=190)

    ctk.CTkLabel(root, text="Your Phone number", font=fontbold).place(x=30, y=230)
    phoneNumber_entry = ctk.CTkEntry(root, font=font)
    phoneNumber_entry.place(x=30, y=260)

    ctk.CTkLabel(root, text="Your Location", font=fontbold).place(x=30, y=300)
    Location_entry = ctk.CTkEntry(root, font=font)
    Location_entry.place(x=30, y=330)

    ctk.CTkLabel(root, text="Your Main Role", font=fontbold).place(x=30, y=370)
    Role_entry = ctk.CTkEntry(root, font=font)
    Role_entry.place(x=30, y=400)

    ctk.CTkLabel(root, text="Your Education", font=fontbold).place(x=200, y=20)
    Edu_entry = ctk.CTkEntry(root, font=font, width=300, height=50, justify="left")
    Edu_entry.place(x=200, y=50)

    ctk.CTkLabel(root, text="Your Skills (put ( . ) after every skill)", font=fontbold).place(x=200, y=110)
    Skill_entry = ctk.CTkEntry(root, font=font, width=300, height=50, justify="left")
    Skill_entry.place(x=200, y=140)

    ctk.CTkLabel(root, text="Your Languages (put ( . ) after every language)", font=fontbold).place(x=200, y=200)
    Lange_Entry = ctk.CTkEntry(root, font=font, width=300, height=50, justify="left")
    Lange_Entry.place(x=200, y=230)

    ctk.CTkLabel(root, text="Your Profile", font=fontbold).place(x=200, y=290)
    Profile_Entry = ctk.CTkEntry(root, font=font, width=300, height=108, justify="left")
    Profile_Entry.place(x=200, y=320)

    ctk.CTkLabel(root, text="You Work - 1 (Add Date, Ex: SoftWareEnginner 2016 - 2020)", font=fontbold).place(x=530, y=20)
    Work_Entry = ctk.CTkEntry(root, font=font, width=340, height=30)
    Work_Entry.place(x=530, y=50)

    ctk.CTkLabel(root, text="The Experience - 1", font=fontbold).place(x=530, y=90)
    Experience_Entry = ctk.CTkEntry(root, font=font, height=108, width=340)
    Experience_Entry.place(x=530, y=120)

    ctk.CTkLabel(root, text="You Work - 2 (Optional)", font=fontbold).place(x=530, y=245)
    Work_Entry2 = ctk.CTkEntry(root, font=font, width=340, height=30)
    Work_Entry2.place(x=530, y=275)

    ctk.CTkLabel(root, text="The Experience - 2 (Optional)", font=fontbold).place(x=530, y=316)
    Experience_Entry2 = ctk.CTkEntry(root, font=font, height=80, width=340)
    Experience_Entry2.place(x=530, y=347)

    ctk.CTkLabel(root, text="Enter ColorCode", font=fontbold).place(x=910, y=220)
    Color_Entry = ctk.CTkEntry(root, font=font)
    Color_Entry.place(x=910, y=250)


    ##------------------AvatarPics
    ctk.CTkLabel(root, text="Avatar", font=fontbold, height=150, width=150, bg_color="#23457a").place(x=910, y=50)



    ##------------------Buttons
    ButtonSend = ctk.CTkButton(root, text="Generate now!", font=("Helvetica", 16, "bold"), width=200, height=50, 
    command=lambda: generateCV(fName_entry, lName_entry, Email_entry, phoneNumber_entry, Location_entry, Role_entry, Edu_entry, Skill_entry, Lange_Entry, Profile_Entry, Work_Entry, Experience_Entry,Work_Entry2,Experience_Entry2, Color_Entry))
    ButtonSend.place(x=30, y=480)

    picButton = ctk.CTkButton(root, text="Upload Avatar", font=("Helvetica", 16, "bold"), width=200, height=50, 
    command=lambda: uploadAvatar())
    picButton.place(x=280, y=480)

    quitButton = ctk.CTkButton(root, text="Exit", font=("Helvetica", 16, "bold"), width=200, height=50, fg_color="#cf1b3f", hover_color="#a1122e",
    command= quit_program)
    quitButton.place(x=865, y=480)

createTheWindow()

root.mainloop()

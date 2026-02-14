import customtkinter as ctk
import oracledb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_CONFIG = {
    "user": "system",
    "password": "parolaAiaPuternic4",
    "dsn": "localhost:1521/xe"
}


class EventApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Gestiune Bilete Evenimente - Proiect BDD 2025")
        self.geometry("1300x850")

        # Configurare Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="MENIU PROIECT", font=("Arial", 22, "bold")).pack(pady=30)

        # Butoane Sidebar
        ctk.CTkButton(self.sidebar, text="Acasă / Reset", fg_color="transparent", border_width=1, command=self.show_welcome).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Vânzări pe Oraș (C4)", command=self.setup_report_1_ui).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Sold Out Status (C6)", command=self.run_report_2).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Utilizatori Loiali (C7)", command=self.run_report_3).pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="").pack(pady=20)  # Spacer

        ctk.CTkButton(self.sidebar, text="CUMPĂRĂ BILET", fg_color="#2b7339", hover_color="#1e5228",
                      command=self.setup_purchase_ui).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="Stoc Bilete Disponibile", command=self.run_remaining_tickets_report).pack(pady=10, padx=20, fill="x")

        # Zona Centrală
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.header_label = ctk.CTkLabel(self.main_frame, text="Bun venit în aplicația de Gestiune Evenimente",
                                         font=("Arial", 24, "bold"))
        self.header_label.pack(pady=20)

        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def get_conn(self):
        return oracledb.connect(**DB_CONFIG)

    def show_welcome(self):
        self.clear_content()
        self.header_label.configure(text="Sistem de Gestiune Baze de Date")
        info_txt = ("Aplicație realizată în Python cu backend Oracle SQL.\n\n"
                    "Cerințe îndeplinite:\n"
                    "• Minim 7 tabele relaționale\n"
                    "• Rapoarte complexe (Complexitate 4, 6, 7)\n"
                    "• Grafice generate din proceduri stocate\n"
                    "• Fără cod SQL direct în Python")
        ctk.CTkLabel(self.content_area, text=info_txt, font=("Arial", 16), justify="left").pack(pady=50)

    # --- RAPORT 1: VÂNZĂRI PE ORAȘ ---
    def setup_report_1_ui(self):
        self.clear_content()
        self.header_label.configure(text="Analiză Vânzări pe Oraș (Complexitate 4+)")

        # Luăm orașele din bază via procedură
        orase = []
        try:
            conn = self.get_conn()
            c = conn.cursor()
            out_c = conn.cursor()
            c.callproc("sp_get_distinct_cities", [out_c])
            orase = [row[0] for row in out_c]
            conn.close()
        except Exception as e:
            print(e)

        if not orase:
            ctk.CTkLabel(self.content_area, text="Nu s-au găsit date.").pack()
            return

        ctk.CTkLabel(self.content_area, text="Selectați orașul pentru raport:").pack(pady=5)
        self.city_picker = ctk.CTkComboBox(self.content_area, values=orase, width=250)
        self.city_picker.pack(pady=10)

        ctk.CTkButton(self.content_area, text="Generează Raport Grafic", command=lambda: self.run_report_1_exec(self.city_picker.get())).pack(pady=10)
        self.chart_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True)

    def run_report_1_exec(self, oras):
        for w in self.chart_container.winfo_children(): w.destroy()
        try:
            conn = self.get_conn()
            c = conn.cursor()
            out_c = conn.cursor()
            c.callproc("sp_raport_vanzari_oras", [oras, out_c])

            labels, values = [], []
            for row in out_c:
                labels.append(row[0])
                values.append(float(row[1]))

            if labels:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(labels, values, color='#1f77b4')
                ax.set_title(f"Venituri în {oras} pe Categorii")
                canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)
            else:
                ctk.CTkLabel(self.chart_container, text="Fără încasări în acest oraș.").pack()
            conn.close()
        except Exception as e:
            print(e)

    # --- RAPORT 2: SOLD OUT (C6) ---
    def run_report_2(self):
        self.clear_content()
        self.header_label.configure(text="Raport Evenimente Sold-Out (Complexitate 6+)")
        try:
            conn = self.get_conn()
            c = conn.cursor()
            out_c = conn.cursor()
            c.callproc("sp_raport_organizatori_soldout", [out_c])

            labels, sizes = [], []
            for row in out_c:
                labels.append(row[1])
                sizes.append(row[2])

            if labels:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
                ax.set_title("Distribuție Bilete - Evenimente Sold Out")
                canvas = FigureCanvasTkAgg(fig, master=self.content_area)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)
            else:
                ctk.CTkLabel(self.content_area,
                             text="Niciun eveniment nu este momentan Sold-Out.\nFolosiți meniul 'Cumpără Bilet' pentru a epuiza stocul.",
                             font=("Arial", 14)).pack(pady=50)
            conn.close()
        except Exception as e:
            print(e)

    # --- RAPORT 3: USERI LOIALI (C7) ---
    def run_report_3(self):
        self.clear_content()
        self.header_label.configure(text="Utilizatori Loiali - Minim 3 Categorii (Complexitate 7+)")
        try:
            conn = self.get_conn()
            c = conn.cursor()
            out_c = conn.cursor()
            c.callproc("sp_raport_utilizatori_loiali", [out_c])

            txt_box = ctk.CTkTextbox(self.content_area, width=800, height=400, font=("Courier New", 14))
            txt_box.pack(pady=20)
            txt_box.insert("0.0", f"{'NUME UTILIZATOR':<25} | {'EMAIL':<30} | {'CAT.':<5} | {'TOTAL':<10}\n")
            txt_box.insert("end", "-" * 80 + "\n")

            found = False
            for row in out_c:
                found = True
                line = f"{row[0]:<25} | {row[1]:<30} | {row[2]:<5} | {row[3]:<10} RON\n"
                txt_box.insert("end", line)

            if not found:
                txt_box.insert("end", "\nNu există utilizatori care să îndeplinească criteriile.")
            conn.close()
        except Exception as e:
            print(e)

    # --- FORMULAR CUMPĂRARE DINAMIC ---
    def setup_purchase_ui(self):
        self.clear_content()
        self.header_label.configure(text="Modul de Achiziție Bilete", text_color="white")

        bilete_data = {}
        users_data = {}
        try:
            conn = self.get_conn()
            c = conn.cursor()

            # Incarcam biletele
            out_b = conn.cursor()
            c.callproc("sp_get_tickets_lookup", [out_b])
            for row in out_b: bilete_data[row[1]] = row[0]

            # Incarcam utilizatorii
            out_u = conn.cursor()
            c.callproc("sp_get_users_lookup", [out_u])
            for row in out_u: users_data[row[1]] = row[0]

            conn.close()
        except Exception as e:
            print(f"Eroare incarcare date: {e}")

        form = ctk.CTkFrame(self.content_area)
        form.pack(pady=20, padx=20, fill="x")

        # Dropdown Bilet
        ctk.CTkLabel(form, text="Alege Biletul:").grid(row=0, column=0, padx=10, pady=10)
        self.ticket_combo = ctk.CTkComboBox(form, values=list(bilete_data.keys()), width=450)
        self.ticket_combo.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown Utilizator
        ctk.CTkLabel(form, text="Cumpărător:").grid(row=1, column=0, padx=10, pady=10)
        self.user_combo = ctk.CTkComboBox(form, values=list(users_data.keys()), width=450)
        self.user_combo.grid(row=1, column=1, padx=10, pady=10)

        # Cantitate
        ctk.CTkLabel(form, text="Cantitate:").grid(row=2, column=0, padx=10, pady=10)
        self.qty_spin = ctk.CTkEntry(form, placeholder_text="Ex: 5")
        self.qty_spin.grid(row=2, column=1, padx=10, pady=10)

        # FIX: Trimitem ambele dictionare catre functia de executie
        btn_buy = ctk.CTkButton(self.content_area, text="Finalizează Comanda", fg_color="#2b7339", command=lambda: self.exec_purchase(bilete_data, users_data))
        btn_buy.pack(pady=20)


    def exec_purchase(self, t_lookup, u_lookup):
        try:
            bilet_info = self.ticket_combo.get()
            user_info = self.user_combo.get()

            bilet_id = t_lookup[bilet_info]
            user_id = u_lookup[user_info]

            # Extragem pretul (e intre paranteze in textul din dropdown)
            pret = float(bilet_info.split('(')[1].split(' ')[0])
            cantitate = int(self.qty_spin.get())

            conn = self.get_conn()
            c = conn.cursor()
            c.callproc("sp_cumpara_bilet", [user_id, bilet_id, cantitate, pret])
            conn.close()

            self.header_label.configure(text="Comandă realizată cu succes!", text_color="#4ade80")
            self.clear_content()

        except oracledb.DatabaseError as e:
            error_obj, = e.args
            if error_obj.code == 20001:  # Codul nostru de Sold Out
                self.header_label.configure(text=f"{error_obj.message}", text_color="#fbbf24")
            else:
                self.header_label.configure(text=f"Eroare DB: {error_obj.message}", text_color="#f87171")
        except Exception as e:
            self.header_label.configure(text=f"Eroare: {str(e)}", text_color="#f87171")


    def run_remaining_tickets_report(self):
        self.clear_content()
        self.header_label.configure(text="Disponibilitate Bilete pe Orașe", text_color="white")
        try:
            conn = self.get_conn()
            c = conn.cursor()
            out_c = conn.cursor()

            # Apelăm noua procedură
            c.callproc("sp_get_remaining_tickets", [out_c])

            txt_box = ctk.CTkTextbox(self.content_area, width=900, height=450, font=("Courier New", 13))
            txt_box.pack(pady=20, padx=10)

            # Header tabel
            header = f"{'ORAȘ':<15} | {'EVENIMENT':<30} | {'TIP':<12} | {'PREȚ':<8} | {'DISPONIBIL':<10}\n"
            txt_box.insert("0.0", header)
            txt_box.insert("end", "-" * 85 + "\n")

            for row in out_c:
                # row[0]=Oras, row[1]=Titlu, row[2]=NumeTip, row[3]=Pret, row[4]=BileteRamase
                line = f"{row[0]:<15} | {row[1]:<30} | {row[2]:<12} | {row[3]:>3} RON | {row[4]:>7} buc.\n"

                # Marcam cu rosu daca stocul e critic (sub 10 bilete)
                if row[4] <= 0:
                    txt_box.insert("end", line.replace(str(row[4]), "SOLD OUT"))
                else:
                    txt_box.insert("end", line)

            conn.close()
        except Exception as e:
            self.header_label.configure(text=f"Eroare: {e}", text_color="red")


if __name__ == "__main__":
    app = EventApp()
    app.mainloop()
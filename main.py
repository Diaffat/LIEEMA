import email
import streamlit as st
import time,datetime
import pandas as pd
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu
# Data Viz Pkgs
import plotly.express as px 
import pyodbc,base64
HTML_BANNER = """
    <div style="background-color:#7B6F;padding:1000px,1px,1px,1px;border-radius:15px">
    <h1 style="color:white;text-align:center;"> Ligue Islamique des Elèves et Etudiants du Mali(LIEEMA-Ségou)  </h1>
    <h2 style="color:white;text-align:center;">﴿وَاعْتَصِمُوا بِحَبْلِ اللهِ جَمِيعًا وَلاَ تَفَرَّقُوا﴾ [آل عمران: 103</h2>
    </div>#464e5f
    """#7B6F
connection = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-PTQ7CTJ\SQLEXPRESS;'
    r'DATABASE=lieema;'
    r'Trusted_Connection=yes;') 
cursor = connection.cursor()
def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
def insert_data(NOM,PRENOM,CONTACT,SECTION,EMAIL,DATE_ADHESION,NIVEAU,ETAT_MATRIMONIAL,GENRE,COMITE,POSTE,INFO,timestampe):
    DB_table_name = 'akhawat'
    insert_sql = "insert into " + DB_table_name  + """
    values (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    rec_values = (NOM,PRENOM,CONTACT,SECTION,EMAIL,DATE_ADHESION,NIVEAU,ETAT_MATRIMONIAL,GENRE,COMITE,POSTE,INFO,timestampe)
    cursor.execute(insert_sql, rec_values)
    connection.commit()
choose = option_menu("LIEEMA-SEGOU",["Home","Enregistrement","Rapport"],
    icons=['house','file','graph-up'],
    menu_icon = "list", default_index=0,
    styles={
        "container": {"padding": "5!important", "background-color": ""},
        "icon": {"color": "green", "font-size": "18px"}, 
        "nav-link": {"font-size": "10px", "text-align": "left", "margin":"5px", "--hover-color": ""},
        "nav-link-selected": {"background-color": " #7B6F"},#164e5f
    },orientation = "horizontal"
    )
def main():

    if choose == "Home":
        stc.html(HTML_BANNER)
        st.subheader("j'ai pensé au une description de la lieema ou une publicité des prochaines activités")

    if choose == "Enregistrement":
        menu=["Nouveau","Mettre à jour ","Supprimer","A propos"]
        choice= st.sidebar.selectbox("Accueil",menu)
        if choice=="Nouveau":
            st.subheader("Veuillez entrer les informations sur le militant")
            #layout
            col1 ,col2,col4=st.columns(3)
            with col4 :
                Poste=st.text_input("Poste occupée")
            with col1 :
                task_name =st.text_input("Nom")
            with col2 :
                task_fname =st.text_input("Prénom")
            cole,coe,coee=st.columns(3)
            with cole:
                contact = st.text_input("Numéro de téléphone")
            with coe:
                sect=["Ségou","San","Tominian"]
                secti=st.selectbox("Section",sect)
            with coee :
                emaili=st.text_input("Email")
            coll1,col3,coll2 ,coll3=st.columns(4)
            with coll1 :
                task_date =st.date_input("Date d'adhesion")
            with col3:
                niveau= st.text_input("Classe ou niveau")
            with coll2 :
                val=["Marié(e)","Célibataire"]
                task_cp =st.selectbox("Etat Matrimonial",val)
            with coll3:
                sex=["Homme","Femme"]
                sexe= st.selectbox("Genre",sex)
            col,co=st.columns(2)
            with col :
                nomComite =st.text_area("Nom du comité rattaché à la section")
            with co :
                task_info =st.text_area("Autres Informations sur le militant")
            if st.button("Enregistrer"):
                st.success("Militant(e)"+" "+task_name+" "+"a été enregistré(e) avec succès")
                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)
                insert_data(task_name,task_fname,str(contact),secti,emaili,task_date,str(niveau),task_cp,sexe,nomComite,Poste,task_info,timestamp)
                st.balloons() 
        elif choice == "Mettre à jour":
            st.subheader("Mets à jour")
        elif choice =="Supprimer":
            st.subheader("Supprime")
        elif choice=="A propos":
            st.subheader("A propos")
    if choose== "Rapport":
        st.success('BIENVENUE DANS LA SECTION ADMIN')
        st.sidebar.subheader('**Veuillez entrer le nom et le mot de passe!**')

        ad_user = st.text_input("Nom d'utilisateur")
        ad_password = st.text_input("Mot de passe", type='password')
        if st.button('Go'):
            if ad_user == 'mami' and ad_password == '123':
                st.success("Bienvenue")
                # Display Data
                cursor.execute('''SELECT*FROM akhawat''')
                data = cursor.fetchall()
                st.header("**Nos données👨‍💻**")
                df = pd.read_sql_query('''SELECT*FROM akhawat''',connection)
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'LIEEMA_SEGOU.xlsx','telecharger le rapport'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from akhawat;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                labels = plot_data.GENRE.unique()
                print(labels)
                values = plot_data.GENRE.value_counts()
                print(values)
                st.subheader("📈 **Pie-Chart pour Genre**")
                fig = px.pie(df, values=values, names=labels, title='Pourcentage en fonction du genre')
                st.plotly_chart(fig)

                ### Pie section
                labels = plot_data.SECTION.unique()
                values = plot_data.SECTION.value_counts()
                st.subheader("📈 ** Pie-Chart pour section👨‍💻 **")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 section👨‍💻")
                st.plotly_chart(fig)
                ### Pie etat matrimonial
                labels = plot_data.ETAT_MATRIMONIAL.unique()
                values = plot_data.ETAT_MATRIMONIAL.value_counts()
                st.subheader("📈 ** Pie-Chart pour état matrimonial👨‍💻 **")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 etat 👨‍💻")
                st.plotly_chart(fig)


            else:
                st.error("Wrong ID & Password Provided")








if __name__ == '__main__':
   main()

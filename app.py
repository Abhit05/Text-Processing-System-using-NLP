
from future.builtins import next
#@author: amaurya
import streamlit as st
import pandas as pd
import os
import csv
import re
import logging
import optparse
import dedupe
from unidecode import unidecode
import base64
import spacy
import numpy as np


st.title('End Users Script')

def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",["Endusers Identification", "Show instructions"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Deduplication".')
    elif app_mode == "Endusers Identification":
        #readme_text.empty()
        #st.sidebar.success('To get instruction select a radio box from below.')
        #st.title("Deduplications")
        nlp_ner()


def file_chooser():
    file_bytes = st.file_uploader("Upload a file", type=("csv","xlsx",".xls"))
    if file_bytes is not None:
        with st.spinner('Wait for it...'):
            data = pd.read_excel(file_bytes)
            st.success('File uploaded succesful!!')
        #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
        #st.write('You selected `%s`' % filename)
    else:
        data=pd.DataFrame()
        #st.error('Unable to Load the selected file.Please choose another!!')
    return data
def test_code():
    """def file_chooser_settings():
        file_bytes = st.file_uploader("Upload a settings file", type=(""))
        if file_bytes is not None:
            with st.spinner('Wait for it...'):
                data = pd.read_excel(file_bytes)
                st.success('File uploaded succesful!!')
            #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
            #st.write('You selected `%s`' % filename)
        else:
            data=pd.DataFrame()
            #st.error('Unable to Load the selected file.Please choose another!!')
        return data

    def file_chooser_training():
        file_bytes = st.file_uploader("Upload a Training file", type=(""))
        if file_bytes is not None:
            with st.spinner('Wait for it...'):
                data = pd.read_excel(file_bytes)
                st.success('File uploaded succesful!!')
            #st.write("File selected from Folder: ", os.path.abspath("../file_bytes"))
            #st.write('You selected `%s`' % filename)
        else:
            data=pd.DataFrame()
            #st.error('Unable to Load the selected file.Please choose another!!')
        return data"""

def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """
    try : # python 2/3 string differences
        column = column.decode('utf8')
    except AttributeError:
        pass
    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    # If data is missing, indicate that by setting the value to `None`
    if not column:
        column = None
    return column

def readData(filename,id_col):
    """
    Read in our data from a CSV file and create a dictionary of records,
    where the key is a unique record ID and each value is dict
    """
    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            print(clean_row)
            row_id = int(row[id_col])
            data_d[row_id] = dict(clean_row)
    return data_d

def trans(x):
    return unidecode(str(x))


def nlp_ner():
    data=pd.DataFrame()
    st.write("Choose a File")
    data=file_chooser()
    st.subheader("Source Data")
    if st.checkbox("Show Source Data"):
        st.write("The Sample Data is as follows:")
        st.write(data.head())
    msg1=("Total number of records : " + str(len(data)))
    st.info(msg1)
    cols_for_identification = st.selectbox('Select column to use for EUI', data.columns)
    country_columns = st.selectbox('Select Country column to use', data.columns)
    tags=st.multiselect("Select a Model to use use :",["Large","Medium","Small"])
    if st.button("Start EUI"):
        with st.spinner('Processing File...'):
            data=spacy_models(data,cols_for_identification,country_columns)
            st.success('Completed! **You can download the file using the below Link :)**')
        st.balloons()
        #if output_name is not None:
        #    csv = out.to_csv(index=False)
            #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
        #else:
        #    output_name="Default"
        #    csv = out.to_csv(index=False)
            #csv = out.to_excel("Output_"+str(date.today())+"_"+output_name,index=False)
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download Output File</a> (right-click and save as &lt;some_name&gt;.csv)'
        st.markdown(href, unsafe_allow_html=True)
            #output_name=("Output_",datetime.datetime.today())
    else:
        st.markdown("> ** Click on Start webscraping Button to Start the processing ** ")

def spacy_models(data,column_as,country_col):
    nlp = spacy.load('en_core_web_md')
    data.fillna('',inplace=True)
    data['Orginal_Name']=data[column_as].copy()
    data[column_as]=data[column_as].replace(',',' ', regex=True)
    data[column_as]=data[column_as].apply(lambda x:str(x).replace("(",""))
    data[column_as]=data[column_as].apply(lambda x:str(x).replace(")",""))
    data[column_as]=data[column_as].replace(':',' ', regex=True)
    data[column_as]=data[column_as].replace('/',' ', regex=True)
    data[column_as].fillna('x_x',inplace=True)
    spec_chars = '''#()–,-\"@+_/:;?*'''
    for char in spec_chars:
        data[column_as] = data[column_as].str.replace(char, ' ')
        data[column_as] = data[column_as].str.strip()
    x='facility sro sp.zo.o. STATIONERY SOC VYSKUMNY SA SASU ELECTRICAL: C.B. TOWERS AGRARPRODUKTE FACTORY ASSISTENCIALS solar APPLIED TEKNIKOA STUDIO S.L.U S.L.L. INSTIT PHARMAECUTICAL N.V. FABRICATION WHOLESALERS WOODWORKS EQUIP MATERIALS PROPERTIES ACS UNIV. SYS WIRELESS EXPERTS GRAPHICS RESTORATIONS PROJEKT P.P.H.U. SICHERHEITSTECHNI ELEC GESELLSCHAFT RESTAURANT S.COOP Kulissenmanufaktur SAGLIK SANAYI  Kulissen manufaktur SCIENTIFIC AB SNC CONSTRUCTORS MATERIAL CLEANING GLEANERS ACADEMIE SVCS DEVELOPMENT LAB HSPTL COMM CONTRACT THERAPEUTICS TECHNO INNOVATIVE LABORATORY EMPLOYEE MORTGAGE DEPOT SUPPL SPRL BLVD TECHNOLOGI INSTITUTE RENTALS INNOVATION ORG AUTOMATION CONNECTIONS MORTGAGE SUPPLIES SYSTE SERVICING RECYCLING WRECKERS HOPITAL LABS CARPENTERS COMUNICACIONES INVESTMENTS S.R.L. BLDG TECHICAL INTERNATIO SRVCS SPECIALISTS TECHNOLO COMMUNITIES KFT. PHARMACEUTICAL SOLUSI COMMUNCATIONS SYSTEMES GESMBH PETROLEUM TEKNO TEKNOLOGI FOUNDATION S.P.A. COMPUTACENTER USTAV PHCY CLNC MEDS REHAB FABRICATORS FINISHING WOODWORKING PLUMBING CLEANERS CEMETERIES ACCESSORIES. INSULATION MOTORWORKS MECHANICAL RESTORATION FURNITURE SAEKERHETSTEKNIK STEUERUNGSTECHNIK AUTHORITY SPECIALTIES COOPERATIVA PHARMA S.R.O SP.Z.O.O. MOTORCYCLES CONTRACTING FARMS CONFECTIONERS SPECIALTY DAIRY ARCHITECTS CLINICAL PHARMACY PRODUCTION S.A.U. OFFICES S.A.S. AMUSEMENTS INSTRUMENTS PLC INSTITUTO TECNOLOGICO MEDICAL SPOL.S.R.O. ELECTRIQUE SECURITE ENR. TEKNIK TEMIZLIK MEDIKAL PRINTING SAG.HIZ.TIC.LTD.ST HIZ.LTD.STI. SAGLIGI HIZM. AS. DENTAL TICARET SANAYI SAN.TIC.LTD.STI HIZ.LTD.STI. HIZM.VE SAN.TIC SAN.TIC.LTD.ST SAN. DENIZCILIK HIZMETLERI MERKEZI HIRDAVAT TARIM INC. URETIMI INFORMATIONSTECHNOLO INFORMATIONSVERARBEITUNG EKOSISTEM PRODUKSIYON SKOLE AUTO AVIATION AUTOMOBILES CLNIC TIRES WHEELS AUTOMOBILE MOTORS ROOFING INDUSTRIEL EQUIPEMENTS ENTREPRISE LTEE LTEE. ENTREPRISES MECANIQUE EQUIPEMENT EMPLOYES AUTOBODY OPERATIONS HEATING CLINICS WHOLESALE LLC. CONTRACTORS DIAGNOSTICS TECHNOL COMPANIES PARTNERS AGENCY CO., L.P. ASSOCIATION FNDATION ALLSTATE PHARMACEUTICALS Enterprises Informatika PLT PLT. P/L CORPORATE INITIATIVES GMB INDUSTRIES Electronics PVT.LTD CONSULTANTS universitet APPLIANCES CO.LTD CO.,LTD spolka THE FAMILY M.B.H. e.k. e.k., Stationary METAL INDUSTRIELLES COPORATION S.A.R.L. ELECTRIC SERVIC PROTECTION INSPECTION telcom MAINTENANCE s.h cv S.C.P s.c. LTD.STI. TECHMIK LTD.S SAGL.HIZ.SAN.TIC.LTD.STI SDAD.COOP.LTDA. PHARMACIE SERVICES Elektronik FARM BUREAU Departementenes CTR AFFAIRS CMHC Financial Financials Mgmt BV EPP CO.UK A.S S.A L.L.P. as NV OY ag DMCC norway sp.k. P.P.U.H. P.P.E Ikt S.P.A LTD. e.u. (PC) PC Manucfaturi homes SERVIZI S.C.R.L. LIMITADA TECNOLOGICA CNTR kommune KOMMUN technic TECNICA HQ LP BVBA Teknologisk d.d. BCBS call ENGINEERING cap storage itsk tele teleplan INDUSTRIE technologique technowledge Sverige DOO BING INTERNATIONAN LLP kompyuternye trading KAISER AUSTRALIA Inc. Prisma MOBILTEL DATA SP. SOHAR Verizon ZONE CENTROS L.L.C. BOULANGER ENTERPRISE HILL SECURITY CARE S.P. CV. SHI PRIMA SURYA PT. AMERICAN GLOBAL MARKIT PAPER STOCK ISD ingram SP NORMAN CENTRALPOINT CENTRAL CENTRALE TECNOLOGIA JBHIFI HIFI CONSULTING shop ATEA DUSTIN solution SOLUTIONS. EQUIPMENT. INFORMATI Furnishing Furnishings Department MEDICALLY BANK BEAU COMPUTEK COMPUTACION COMPTOIRE ELECT PRODUCTS CREDITS CREDIT INTL INT\'L COMMUNITY CO UNION PUBLIC UTILITY INSURANCE DEPARTMENT state TRUST COMPUTRONSA DIST Bhd E.I.R.L. WAREHOUSE S.A.R.L A.S. COM ZRT. HOSPITALS CRANE COMPUTING REPAIRS INNOVATIONS DISTRIBUTORS MACHINES BUSINESS APPLE TECHNOLOGIES PTE.LTD. LTD.,PART. Co.,Ltd Corp. COMPONENTS COMP. Computer COMP ACCESSORIES ComputerS DIGITAL ADVANTAGE MEDIA RETAIL WORLD DIRECT DRUGS EIRL BILGISAYAR LDLC Co.,Ltd. s.p. B.V. BEST EXPERT DISTRIBUTION Ltda. HOLDING SpA COMERCIO shopify SERVICOS S.A.S S.E. S.A. CENTRE Komplett technologie health sistem s.l. sl UNIVERSITE MEDICINA MANUFACTURE APARTMENTS BUILDERS STORES SAL V.O.F. VOF GGMBH solutions comerciales soluciones tecnologicas komputer komputama MARKET MARKETs MARKT Compuoriente genetech D.O.O. LOGISTICS INFORMATICA informatique solution technocare chemtech informationstechnik intertechnology technosante technologique sarl s.r.o. spol industriservice center A/S MBH GMBH S.L.U. LTD inc. LIMITED INC LLC SERVICE MANAGEMENT MANUFACTURING GMBH/GMB COUNTY CONTROL CONSTRUCTIO CONSTRUCTION CONSTRUCTION. INDUSTRIAL B.V.B.A. ASSSOCIATI CONSULTANCY LIMITED. LDA LDA. AUTO BODY OFFICE COMPANY WORK SYSTEM BHD. HEALTHCARE LLLP DEPT. NETWORKS LABORATORIES SYSTEMS INFOTECH TELECOM TECH technology information genetech INDUSTRY SARL SRL SAS S.L S.R.L B.V KFT S.A.S Z.O.O ZOO CO. DENTISTRY ELECTRICAL GOVERNMENT SOLUTION CLINIC INTERNATIONAL GROUP DESIGN ASSOCIATES ASSOC SUPPLY SALE AUTOMOTIVE LTD, WELDING RAILINGS INDUSTR ECLECTIC TRUCKING INCORPORATED EQUPMENT EQUIPMENT CORPORATION CORP HOSP SCHOOL schools ACADEMY COLLEGE DETAIL UNIVERSITY AKCYJNA ARMY DEFENCE CARE HOSPITAL SPORTS SPECIALITIES SIGNS RESOURCES REPAIR TRANSPORT OPERATION CITY EQUIPMENT DEPT MACHINERY ENERGY COMMUNICATION COMMUNICATIONS COMM. DISPENSERS TECHSERVICES COMMERCIAL ELECTR DCMS SOLUTION PACKAGING SYS. SPA STORE GLOBAL PROCESSING UTILITIES FHU F.H.U NORMAN pty ltd office salz aps Officeworks works JB JB-HiFi'
    x=x.lower()
    #x=x.split(' ')
    #pd.DataFrame({'Keywords':x}).to_excel(r'C:\Users\amaurya\Documents\emails\sukanaya\Keywords_main_scoring.xlsx',index=False)
    #can be added anh LITTLE
    x=x.split(' ')
    x.append('sp. z o.o.')
    x.append('s. r. o.')
    x.append('Sp. Z O.O.')
    x.append('Cong ty')
    x.append('Pte LTD')
    x.append('Sdn Bhd')
    x.append('S. R. L.')
    x.append('D O O')
    x.append('SPOL. S R.O.')
    x.append('S R.O.')
    x.append('SPOL.S.')
    x.append('S. R. O')
    x.append('SPOL.S R.O.')
    x.append('SAN A S')
    x.append('A S')
    x.append('WELLS FARGO')
    x.append('UC DAVIS')
    x.append('CAPITAL ONE')
    x.append('NORTHROP GRUMMAN')
    x.append('ELECTRONIC ARTS')
    x.append('GEORGIA PACIFIC')
    x.append('RUTLEDGE AV')
    x.append('JPMORGAN CHASE')
    x.append('SP.Z O.O..SP.K')
    x.append('S.C.')
    L=['GOOD GUYS','HI FI','SP RICHARDS','HI-FI','GM KG','JP MORGAN CHASE','L3 HARRIS','SOCIÉTÉ INTERNE','NORGE AS','CZ A.S.','ATTN','ATTN:','sa','MDM','MEYER','RENTAL','sp. z o.o. sp.k.','L P']
    y_comp='IBM MICROSOFT UNIV GOOGLE SCIENCES AMAZON MILLS WALMART AMAZON.COM SLU ASCENSION STAPLES ORACLE CONTINENTAL VMWARE NISSAN WHITLOCK CENTURYLINK'
    y_comp=y_comp.split(' ')
    x.extend(L)
    x.extend(y_comp)
    creden='DDS DMD MD DR RDH DPC PA-C PHD LCPL Professional Dr. D.D.S D.M.D MUDR MUDR. DNP DVM DPM MPH CNP CRNA'
    creden=creden.split(' ')
    creden.append('D D S')
    creden.append('D M D')
    creden.append('D P C')
    data['Keywords Check']='not_sure'
    data['Credential Check']='not_sure'
    xval=[]
    check_cred=[]
    for i in data[column_as]:
        i=str(i).lower()
        if any((' ' + ext.lower() + ' ') in (' ' + i + ' ') for ext in x):
            xval.append('ORG')
        else:
            xval.append('Check')
        if any((' ' + ext.lower() + ' ') in (' ' + i + ' ') for ext in creden):
            check_cred.append('credentials')
            for ext in x:
                if (' '+ext.lower()+' ') in (' ' + i + ' '):
                    print(ext)
        else:
            check_cred.append('Check')
    data['Keywords Check']=xval
    data['Credential Check']=check_cred
    og_data=data[column_as].tolist()
    a=[]
    tags=[]
    for indexes,row in data.iterrows():
        val=row[column_as]
        #print(val)
        if val=='nan' or len(str(val))<=1:
            a.append("No Tag")
        else:
            doc = nlp(str(val))
            i_names={}
            cell_tag=[]
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                i_names[val[int(ent.start_char):int(ent.end_char)]]=(ent.label_)
                cell_tag.append(ent.label_)
            #print("-----------------------------------")
            a.append(i_names)
            tags.append(cell_tag)

    final_df=pd.DataFrame([og_data,a,tags]).transpose()
    final_df=final_df.astype(str)
    final_df=final_df.rename(columns={0: "REPORTED_NAME", 1: "Identified TAG",2:"Tags"})
    final_df["Identified TAG"]= final_df["Identified TAG"].replace('{}', "")
    final_df["Tags"]= final_df["Tags"].replace('[]', " ")

    data['Identified TAG']=final_df["Identified TAG"]
    data['Tags']=final_df["Tags"]
    data['Keywords Check_og']=data['Keywords Check'].copy()
    data['Keywords Check'].replace('Check',np.NaN,inplace=True)
    data['Tags'].fillna('Empty',inplace=True)
    data['Tags'].replace(' ','Empty',inplace=True)
    data['org']=''

    org_list=[]
    for i in data['Tags']:
        #print(i)
        if 'ORG' in i:
            org_list.append('ORG')
        elif ('ORG' not in i)and('PERSON' in i) :
            org_list.append('PERSON')
        else:
            org_list.append('')
    data['org']=org_list
    data['Keywords Check'].fillna(data.org,inplace=True)
    data['Keywords Check'].replace('','Check',inplace=True)
    #################### Model 2##############
    nlp_2 = spacy.load('en_core_web_sm')
    nlp_3 = spacy.load('en_core_web_lg')
    data_check=data[(data['Keywords Check']=='Check')]
    data.drop(data.loc[data['Keywords Check']=='Check'].index, inplace=True)
    a_2_sm=[]
    tags_2_sm=[]
    for indexes,row in data_check.iterrows():
        val=row[column_as]
        #print(val)
        if val=='nan' or len(str(val))<=1:
            a_2_sm.append("No Tag")
        else:
            doc = nlp_2(str(val))
            i_names={}
            cell_tag=[]
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                i_names[val[int(ent.start_char):int(ent.end_char)]]=(ent.label_)
                cell_tag.append(ent.label_)
            #print("-----------------------------------")
            a_2_sm.append(i_names)
            tags_2_sm.append(cell_tag)

    final_df=pd.DataFrame([og_data,a_2_sm,tags_2_sm]).transpose()
    final_df=final_df.astype(str)
    final_df=final_df.rename(columns={0: "REPORTED_NAME", 1: "Identified TAG",2:"Tags"})
    final_df["Identified TAG"]= final_df["Identified TAG"].replace('{}', "")
    final_df["Tags"]= final_df["Tags"].replace('[]', " ")
    data_check['Identified TAG']=final_df["Identified TAG"]
    data_check['Tags']=final_df["Tags"]
    data_check['Keywords Check_og']=data_check['Keywords Check'].copy()
    data_check['Keywords Check'].replace('Check',np.NaN,inplace=True)
    data_check['Tags'].fillna('Empty',inplace=True)
    data_check['Tags'].replace(' ','Empty',inplace=True)
    data_check['org']=''

    org_list=[]
    for i in data_check['Tags']:
        #print(i)
        if 'ORG' in i:
            org_list.append('ORG')
        elif ('ORG' not in i)and('PERSON' in i) :
            org_list.append('PERSON')
        else:
            org_list.append('')


    data_check['org']=org_list
    data_check['Keywords Check'].fillna(data_check.org,inplace=True)
    data_check['Keywords Check'].replace('','Check',inplace=True)
    ######################################## Model 3 ##############################
    data_check2=data_check[(data_check['Keywords Check']=='Check')]
    data_check.drop(data_check.loc[data_check['Keywords Check']=='Check'].index, inplace=True)
    a_3_sm=[]
    tags_3_sm=[]
    for indexes,row in data_check2.iterrows():
        val=row[column_as]
        #print(val)
        if val=='nan' or len(str(val))<=1:
            a_3_sm.append("No Tag")
        else:
            doc = nlp_3(str(val))
            i_names={}
            cell_tag=[]
            for ent in doc.ents:
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                i_names[val[int(ent.start_char):int(ent.end_char)]]=(ent.label_)
                cell_tag.append(ent.label_)
            #print("-----------------------------------")
            a_3_sm.append(i_names)
            tags_3_sm.append(cell_tag)

    final_df=pd.DataFrame([og_data,a_3_sm,tags_3_sm]).transpose()
    final_df=final_df.astype(str)
    final_df=final_df.rename(columns={0: "REPORTED_NAME", 1: "Identified TAG",2:"Tags"})
    final_df["Identified TAG"]= final_df["Identified TAG"].replace('{}', "")
    final_df["Tags"]= final_df["Tags"].replace('[]', " ")
    data_check2['Identified TAG']=final_df["Identified TAG"]
    data_check2['Tags']=final_df["Tags"]
    data_check2['Keywords Check_og']=data_check2['Keywords Check'].copy()
    data_check2['Keywords Check'].replace('Check',np.NaN,inplace=True)
    data_check2['Tags'].fillna('Empty',inplace=True)
    data_check2['Tags'].replace(' ','Empty',inplace=True)
    data_check2['org']=''

    org_list=[]
    for i in data_check2['Tags']:
        #print(i)
        if 'ORG' in i:
            org_list.append('ORG')
        elif ('ORG' not in i)and('PERSON' in i) :
            org_list.append('PERSON')
        else:
            org_list.append('')


    data_check2['org']=org_list
    data_check2['Keywords Check'].fillna(data_check2.org,inplace=True)
    data_check2['Keywords Check'].replace('','Check',inplace=True)

    ################################ data combination#####################################
    #data_check2=data_check[(data_check['Keywords Check']=='Check')]
    data_check2.drop(data_check2.loc[data_check2['Keywords Check']=='Check'].index, inplace=True)
    data=pd.concat([data,data_check,data_check2],axis=0)

    print('Run Successful')
    ###############################################################################
    data.fillna('',inplace=True)
    data.replace('None','',inplace=True)
    data=data.astype(str)
    data[column_as]=data[column_as].replace('x_x', " ")
    data['Credential Check']=data['Credential Check'].replace('Check',' ')
    ###############################
    #data.to_excel(output_file_path+'\\End User_Main_OUTPUT.xlsx',index=False)
    ##############################
    ##
    #data['Derived_Country'].value_counts()
    #country_col='Derived_Country'
    sample_data=data[data[country_col]=='CA']
    #import numpy as np
    sample_data['abc']=sample_data[column_as].str.split(' ').str.len()
    sample_data['Comments']=np.where(sample_data['abc']!=2, 'Valid', '2 Words')
    sample_data.drop(columns=['abc'],inplace=True)
    #sample_data.to_excel(output_file_path+'\\Canada_records.xlsx',index=False)
    sample_data2=data[data[country_col]!='CA']
    #sample_data2.to_excel(output_file_path+'\\Other_records.xlsx',index=False)
    return data
if __name__ == "__main__":
    main()

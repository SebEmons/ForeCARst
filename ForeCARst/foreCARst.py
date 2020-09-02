from flask import Flask, render_template,request 
from datetime import date
import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/Landing.html')
def Landing():
    return render_template('Landing.html')

@app.route('/Intro.html')
def Intro():
    return render_template('Intro.html')

@app.route('/NewCar.html')
def my_form():
    return render_template('NewCar.html')

@app.route('/NewCar.html', methods=['GET','POST'])
def my_form_post():
    if request.method == 'POST':
        Marke = request.form['Marke']
        Modell = request.form['Modell']
        Erstzulassung = request.form['Erstzulassung']
        Kilometerstand = request.form['Kilometerstand']
        Motor = request.form['Motor']
        Hubraum = request.form['Hubraum']
        Verbrauch = request.form['Verbrauch']
        Versicherungskosten = request.form['Versicherungskosten']
        Steuern = request.form['Steuern']


        a = (pd.to_datetime(Erstzulassung)).date() #Datum Erstzulassung
        b = date.today() #Heutiges Datum
        c = (b-a).days #Anzahl zugelassener Tage
        d = float(Kilometerstand) #Kilometerstand in km
        e = d/c #Durchschnittliche Laufleistung km/Tag  
        f = float(Versicherungskosten) #Versicherungskosten €/Monat
        g = float(Steuern) #Steuern €/Jahr
        h = float(Verbrauch) #Durchschnittlicher Verbrauch l/100 km
    
    
        if Motor == "Benzin":
            i = 1.31 # Durchschnittliche Kosten Benzin € / l
        else:
            i = 1.168 # Durchschnittliche Kosten Benzin € / l
            
        j = f + (g/12) + (h*e*365/12/100*i) # Kosten pro Monat
        
        Fixkosten = str(round((f+g/12)))+ ' €/Monat'# Steuern und Versicherung pro Monat
        Treibstoff = str(round((h*e*365/12/100*i))) + ' €/Monat' # Treibstoff pro Monat
        LaufendeKosten = str(round(j)) + ' €/Monat'# Steuern, Versicherung und Treibstoff pro Monat
        
        def Intervallrechnung(km, years):
            if km > 0:
                if km > d:
                    l = (1-((d/km) % 1)) * km # Verbleibende Zeit Inspektion in km
                else:
                    l = ((d/km) % 1) * km # Verbleibende Zeit Inspektion in km
                m = l / e # Verbleibende Zeit Inspektion in Tagen (Umrechnung nach Inspektion in km)
            if years > 0:
                if c < (years*365):
                    o = (1 - (((c/365) / years) % 1)) * years * 365 # Verbleibende Zeit Inspektion in Tagen
                else:
                    o = (((c/365) / years) % 1) * years * 365 # Verbleibende Zeit Inspektion in Tagen
                p = o * e # Verbleibende Zeit Inspektion in km (Umrechnung nach Inspektion in Tagen)
            global q
            global r
            if km > 0 and years > 0:
                if m < o:
                    q = int(l) # Inspektion in km
                    r = int(m) # Inspektion in Tagen
                else:
                    q = int(p) # Inspektion in km
                    r = int(o) # Inspektion in Tagen
            if km > 0 and years == 0:
                q = int(l) # Inspektion in km
                r = int(m) # Inspektion in Tagen
            if km == 0 and years > 0:
                q = int(p) # Inspektion in km
                r = int(o) # Inspektion in Tagen
                
        Intervallrechnung(30000, 2) #Inspektion
        
        Intervallrechnung(0,2) #Bremsflüssigkeit
        bi = q
        bj = r
        
        Intervallrechnung(0,2) #Kühlflüssigkeit
        bn = q
        bo = r
        
        Intervallrechnung(30000,2) #Motoröl
        bx = q
        by = r
        
        Intervallrechnung(30000,2) #Getriebeöl
        bae = q
        baf = r
             
        Intervallrechnung(50000,0) #Bremsbeläge
        baj = q
        bak = r
        
        Intervallrechnung(150000,0) #Bremsscheiben
        bao = q
        bap = r
        
        Intervallrechnung(0,6) #Reifen
        bat = q
        bau = r
        
        Intervallrechnung(0,0.5) #Reifenwechsel
        bay = q
        baz = r
        
        Intervallrechnung(150000,0) #Kupplung
        bbd = q
        bbe = r
        
        Intervallrechnung(100000,0) #Zahnriemen
        bbi = q
        bbj = r
        
        Intervallrechnung(30000,2) #Luftfilter
        bbq = q
        bbr = r
        
        Intervallrechnung(15000,1) #Innenraumfilter
        y = q
        z = r
        
        Intervallrechnung(100000,0) #Stoßdämpfer
        bbx = q
        bby = r
        
        Intervallrechnung(100000,5) #Auspuffanlage
        bcc = q
        bcd = r
        
        Intervallrechnung(0,7) #Batterie
        bch = q
        bci = r
        
        # HU (komplexer, weil erst 3 Jahre, dann 2 Jahre)
        if c < (3*365):
            ba = 3
            bb = (1 - (((c/365)/ba) % 1)) * ba * 365
            bc = bb * e
        if c < (5*365):
            ba = 2
            bb = (1- ((((c-3*365)/365)/ba) % 1)) * ba * 365
            bc = bb * e
        else:
            ba = 2
            bb = ((((c-3*365)/365)/ba) % 1) * ba * 365
            bc = bb * e
        bd = int(bc) # in km
        be = int(bb) # in Tagen
     
        
        # Tabelle, sortiert nach Fälligkeit
        
        df = pd.DataFrame({ 
                  'Leistung': ['Inspektion','HU','Bremsflüssigkeit','Kühlflüssigkeit','Motoröl','Getriebeöl','Bremsbeläge','Bremsscheiben','Reifen','Reifenwechsel','Kupplung','Zahnriemen', 'Luftfilter','Innenraumfilter', 'Stoßdämpfer/Achslager/Querlenker', 'Auspuffanlage','Batterie','Zusätzliche Ausgaben'], 
                  'km': [q,bd,bi,bn,bx,bae,baj,bao,bat,bay,bbd,bbi,bbq,y,bbx,bcc,bch,0],
                  'Tage': [r,be,bj,bo,by,baf,bak,bap,bau,baz,bbe,bbj,bbr,z,bby,bcd,bci,0],
                  '€': [300,110,40,10,100,90,60,180,350,50,2000,300,30,10,260,240,100,0]}).set_index('Leistung')
        
        df = df.sort_values(by = 'km', ascending=True)
        
        df1Monat = df.where((df['Tage']<= (1*(365/12)))).dropna()
        df1 = df1Monat['€'].sum(axis=0)
        
        df2Monat = df.where((df['Tage']<= (2*(365/12)))).dropna()
        df2 = df2Monat['€'].sum(axis=0)
        
        df3Monat = df.where((df['Tage']<= (3*(365/12)))).dropna()
        df3 = df3Monat['€'].sum(axis=0)
        
        df4Monat = df.where((df['Tage']<= (4*(365/12)))).dropna()
        df4 = df4Monat['€'].sum(axis=0)
        
        df5Monat = df.where((df['Tage']<= (5*(365/12)))).dropna()
        df5 = df5Monat['€'].sum(axis=0)
        
        df6Monat = df.where((df['Tage']<= (6*(365/12)))).dropna()
        df6 = df6Monat['€'].sum(axis=0)
        
        df7Monat = df.where((df['Tage']<= (7*(365/12)))).dropna()
        df7 = df7Monat['€'].sum(axis=0)
        
        df8Monat = df.where((df['Tage']<= (8*(365/12)))).dropna()
        df8 = df8Monat['€'].sum(axis=0)
        
        df9Monat = df.where((df['Tage']<= (9*(365/12)))).dropna()
        df9 = df9Monat['€'].sum(axis=0)
        
        df10Monat = df.where((df['Tage']<= (10*(365/12)))).dropna()
        df10 = df10Monat['€'].sum(axis=0)
        
        df11Monat = df.where((df['Tage']<= (11*(365/12)))).dropna()
        df11 = df11Monat['€'].sum(axis=0)
        
        df12Monat = df.where((df['Tage']<= (12*(365/12)))).dropna()
        df12 = df12Monat['€'].sum(axis=0)
        
        df24Monat = df.where((df['Tage']<= (24*(365/12)))).dropna()
        df24 = df24Monat['€'].sum(axis=0)
        
        dfZeit = pd.DataFrame({
            'Kostensumme':[df1, (df2-df1),(df3-df2),(df4-df3),(df5-df4),(df6-df5),(df7-df6),(df8-df7),(df9-df8),(df10-df9),(df11-df10),(df12-df11)],
            'Zeit':[b, b + datetime.timedelta(365/12), b + datetime.timedelta(365/12*2),b + datetime.timedelta(365/12*3),b + datetime.timedelta(365/12*4),b + datetime.timedelta(365/12*5),b + datetime.timedelta(365/12*6),b + datetime.timedelta(365/12*7),b + datetime.timedelta(365/12*8),b + datetime.timedelta(365/12*9),b + datetime.timedelta(365/12*10),b + datetime.timedelta(365/12*11)]})
        
        dfZeit['Zeit'] = pd.to_datetime(dfZeit['Zeit'])
        dfZeit['Zeit'] = dfZeit['Zeit'].dt.strftime('%m/%Y')
        
        dfplot = dfZeit[['Kostensumme','Zeit']].set_index('Zeit')
        zzz=dfplot.plot(kind="bar", color="darkred").get_figure()
        zzz.savefig('static/testneu.png', bbox_inches = "tight")

        dfbasicinformation = pd.DataFrame({
            'Leistung':['Marke','Modell','Erstzulassung', 'Kilometerstand', 'Motor', 'Hubraum','Verbrauch','Versicherungskosten','Steuern'],
            'Wert':[Marke,Modell,Erstzulassung,Kilometerstand,Motor,Hubraum,Verbrauch, Versicherungskosten,Steuern]}).set_index('Leistung')
        
        Datei3 = request.form['Datei3']
        Dateiname3 = r'static/' + Datei3 + '.csv'
        dfbasicinformation.to_csv(Dateiname3)
                        
    return render_template('Costs.html', Marke = Marke, Modell = Modell, Erstzulassung = Erstzulassung, Kilometerstand = Kilometerstand, Motor = Motor, Hubraum = Hubraum, Verbrauch = Verbrauch, Versicherungskosten = Versicherungskosten, Steuern = Steuern, Kosten1Monat = str(df1) + ' €', Kosten6Monate = str(df6) + ' €', Kosten12Monate = str(df12) + ' €', Kosten24Monate = str(df24) + ' €', tables=[df.to_html(classes='data', header="true")],Fixkosten = Fixkosten, Treibstoff = Treibstoff, LaufendeKosten = LaufendeKosten)
    
@app.route('/Oldcar.html')
def my_upload():
    return render_template('Oldcar.html')

@app.route('/Oldcar.html', methods=['GET','POST'])
def my_upload_post():
    if request.method == 'POST':
        
        Dateiname = r'static/' + request.form['Datei'] + '.csv' #Pfad alter Datei
        Dateiname2 = r'static/' + request.form['Datei2'] + '.csv' #Pfad neuer Datei
        Dateinametank = r'static/' + request.form['Datei'] + 'tank' + '.csv' #Pfad alter Datei Tankdaten
        Dateiname2tank = r'static/' + request.form['Datei2'] + 'tank' + '.csv' #Pfad neuer Datei Tankdaten
        
        TankenKilometerstand = float(request.form['TankenKilometerstand'])
        TankenDatum = request.form['TankenDatum']
        TankenLiter = float(request.form['TankenLiter'])
        TankenKosten = float(request.form['TankenKosten'])
        
        altdaten = pd.read_csv(Dateiname).set_index('Leistung')
        
        Marke = altdaten['Wert']['Marke']
        Modell = altdaten['Wert']['Modell']
        Erstzulassung = altdaten['Wert']['Erstzulassung']
        Kilometerstand = altdaten['Wert']['Kilometerstand']
        Motor = altdaten['Wert']['Motor']
        Hubraum = altdaten['Wert']['Hubraum']
        Verbrauch = altdaten['Wert']['Verbrauch']
        Versicherungskosten = altdaten['Wert']['Versicherungskosten']
        Steuern = altdaten['Wert']['Steuern']

        a = (pd.to_datetime(Erstzulassung)).date()
        b = (pd.to_datetime(TankenDatum)).date() # Tankdatum
        c = (b-a).days # Anzahl der zugelassenen Tage
        d = TankenKilometerstand
        e = d/c # Berechnung durchschnittliche Laufleistung km / Tag
        f = float(Versicherungskosten) # Versicherungskosten € / Monat
        g = float(Steuern) # Steuern € / Jahr
        h = float(Verbrauch)
        h = h*(float(Kilometerstand)/d) + (TankenLiter/(TankenKilometerstand-float(Kilometerstand))*100)*((TankenKilometerstand-float(Kilometerstand))/d)  # Durchschnittlicher Verbrauch l / 100 km
         
        from pathlib import Path

        fileName = Dateinametank
        fileObj = Path(fileName)
        

        if fileObj.is_file():
            altdatentanken = pd.read_csv(Dateinametank).set_index('Monate')
            
            Jan1 = altdatentanken['Kosten']['Januar']
            Feb1 = altdatentanken['Kosten']['Februar']
            März1 = altdatentanken['Kosten']['März']
            April1 = altdatentanken['Kosten']['April']
            Mai1 = altdatentanken['Kosten']['Mai']
            Juni1 = altdatentanken['Kosten']['Juni']
            Juli1 = altdatentanken['Kosten']['Juli']
            Aug1 = altdatentanken['Kosten']['August']
            Sept1 = altdatentanken['Kosten']['September']
            Okt1 = altdatentanken['Kosten']['Oktober']
            Nov1 = altdatentanken['Kosten']['November']
            Dez1 = altdatentanken['Kosten']['Dezember']
        else:
            Jan1 = 0
            Feb1 = 0
            März1 = 0
            April1 = 0 
            Mai1 = 0
            Juni1 = 0
            Juli1 = 0 
            Aug1 = 0
            Sept1 = 0 
            Okt1 = 0
            Nov1 = 0 
            Dez1 = 0
       
        #Monat des Tankvorgangs bestimmen
        Tankmonat = b.month
         
        if Tankmonat==1:
                Jan1=Jan1+TankenKosten
        if Tankmonat==2:
                Feb1=Feb1+TankenKosten
        if Tankmonat==3:
                März1=März1+TankenKosten
        if Tankmonat==4:
                April1=April1+TankenKosten
        if Tankmonat==5:
                Mai1=Mai1+TankenKosten
        if Tankmonat==6:
                Juni1=Juni1+TankenKosten
        if Tankmonat==7:
                Juli1=Juli1+TankenKosten
        if Tankmonat==8:
                Aug1=Aug1+TankenKosten
        if Tankmonat==9:
                Sept1=Sept1+TankenKosten
        if Tankmonat==10:
                Okt1=Okt1+TankenKosten
        if Tankmonat==11:
                Nov1=Nov1+TankenKosten
        if Tankmonat==12:
                Dez1=Dez1+TankenKosten
        # 
        source = pd.DataFrame({'Monate' : ['Januar', 'Februar', 'März','April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'], 
                          'Kosten' : [Jan1, Feb1, März1, April1, Mai1, Juni1, Juli1, Aug1, Sept1, Okt1, Nov1, Dez1]})
        source.set_index('Monate')
        source.to_csv(Dateiname2tank)
                
        dfplottanken = source[['Kosten','Monate']].set_index('Monate')
        tankenzzz=dfplottanken.plot(kind="bar", color="darkblue").get_figure()
        tankenzzz.savefig('static/testtanken.png', bbox_inches = "tight")
    
        Verbrauch = round(h, 1)
        
        if Motor == "Benzin":
            i = 1.31 # Durchschnittliche Kosten Benzin € / l
        else:
            i = 1.168 # Durchschnittliche Kosten Benzin € / l
        
        i = i*(float(Kilometerstand)/d) + (TankenKosten/TankenLiter)*((TankenKilometerstand-float(Kilometerstand))/d)
        print(i)
        
        Kilometerstand = round(float(TankenKilometerstand))
        
        j = f + (g/12) + (h*e*365/12/100*i) # Kosten pro Monat
        
        Fixkosten = str(round((f+g/12)))+ ' €/Monat'# Steuern und Versicherung pro Monat
        Treibstoff = str(round((h*e*365/12/100*i))) + ' €/Monat' # Treibstoff pro Monat
        LaufendeKosten = str(round(j)) + ' €/Monat'# Steuern, Versicherung und Treibstoff pro Monat
        
        def Intervallrechnung(km, years):
            if km > 0:
                if km > d:
                    l = (1-((d/km) % 1)) * km # Verbleibende Zeit Inspektion in km
                else:
                    l = ((d/km) % 1) * km # Verbleibende Zeit Inspektion in km
                m = l / e # Verbleibende Zeit Inspektion in Tagen (Umrechnung nach Inspektion in km)
            if years > 0:
                if c < (years*365):
                    o = (1 - (((c/365) / years) % 1)) * years * 365 # Verbleibende Zeit Inspektion in Tagen
                else:
                    o = (((c/365) / years) % 1) * years * 365 # Verbleibende Zeit Inspektion in Tagen
                p = o * e # Verbleibende Zeit Inspektion in km (Umrechnung nach Inspektion in Tagen)
            global q
            global r
            if km > 0 and years > 0:
                if m < o:
                    q = int(l) # Inspektion in km
                    r = int(m) # Inspektion in Tagen
                else:
                    q = int(p) # Inspektion in km
                    r = int(o) # Inspektion in Tagen
            if km > 0 and years == 0:
                q = int(l) # Inspektion in km
                r = int(m) # Inspektion in Tagen
            if km == 0 and years > 0:
                q = int(p) # Inspektion in km
                r = int(o) # Inspektion in Tagen       
        Intervallrechnung(30000, 2) #Inspektion (Variablen p und q schon in def gegeben)
        Intervallrechnung(0,2) #Bremsflüssigkeit
        bi = q
        bj = r
        Intervallrechnung(0,2) #Kühlflüssigkeit
        bn = q
        bo = r
        Intervallrechnung(30000,2) #Motoröl
        bx = q
        by = r
        Intervallrechnung(30000,2) #Getriebeöl
        bae = q
        baf = r
        Intervallrechnung(50000,0) #Bremsbeläge
        baj = q
        bak = r
        Intervallrechnung(150000,0) #Bremsscheiben
        bao = q
        bap = r
        Intervallrechnung(0,6) #Reifen
        bat = q
        bau = r
        Intervallrechnung(0,0.5) #Reifenwechsel
        bay = q
        baz = r
        Intervallrechnung(150000,0) #Kupplung
        bbd = q
        bbe = r
        Intervallrechnung(100000,0) #Zahnriemen
        bbi = q
        bbj = r
        Intervallrechnung(30000,2) #Luftfilter
        bbq = q
        bbr = r
        Intervallrechnung(15000,1) #Innenraumfilter
        y = q
        z = r
        Intervallrechnung(100000,0) #Stoßdämpfer
        bbx = q
        bby = r
        Intervallrechnung(100000,5) #Auspuffanlage
        bcc = q
        bcd = r
        Intervallrechnung(0,7) #Batterie
        bch = q
        bci = r
        # HU (komplexer, weil erst 3 Jahre, dann 2 Jahre)
        if c < (3*365):
            ba = 3
            bb = (1 - (((c/365)/ba) % 1)) * ba * 365
            bc = bb * e
        if c < (5*365):
            ba = 2
            bb = (1- ((((c-3*365)/365)/ba) % 1)) * ba * 365
            bc = bb * e
        else:
            ba = 2
            bb = ((((c-3*365)/365)/ba) % 1) * ba * 365
            bc = bb * e
        bd = int(bc) # in km
        be = int(bb) # in Tagen
        
        # Tabelle, sortiert nach Fälligkeit
        df = pd.DataFrame({ 
                  'Leistung': ['Inspektion','HU','Bremsflüssigkeit','Kühlflüssigkeit','Motoröl','Getriebeöl','Bremsbeläge','Bremsscheiben','Reifen','Reifenwechsel','Kupplung','Zahnriemen', 'Luftfilter','Innenraumfilter', 'Stoßdämpfer/Achslager/Querlenker', 'Auspuffanlage','Batterie','Zusätzliche Ausgaben'], 
                  'km': [q,bd,bi,bn,bx,bae,baj,bao,bat,bay,bbd,bbi,bbq,y,bbx,bcc,bch,0],
                  'Tage': [r,be,bj,bo,by,baf,bak,bap,bau,baz,bbe,bbj,bbr,z,bby,bcd,bci,0],
                  '€': [300,110,40,10,100,90,60,180,350,50,2000,300,30,10,260,240,100,0]}).set_index('Leistung')
        
        df = df.sort_values(by = 'km', ascending=True)
        
        df1Monat = df.where((df['Tage']<= (1*(365/12)))).dropna()
        df1 = df1Monat['€'].sum(axis=0)
        
        df2Monat = df.where((df['Tage']<= (2*(365/12)))).dropna()
        df2 = df2Monat['€'].sum(axis=0)
        
        df3Monat = df.where((df['Tage']<= (3*(365/12)))).dropna()
        df3 = df3Monat['€'].sum(axis=0)
        
        df4Monat = df.where((df['Tage']<= (4*(365/12)))).dropna()
        df4 = df4Monat['€'].sum(axis=0)
        
        df5Monat = df.where((df['Tage']<= (5*(365/12)))).dropna()
        df5 = df5Monat['€'].sum(axis=0)
        
        df6Monat = df.where((df['Tage']<= (6*(365/12)))).dropna()
        df6 = df6Monat['€'].sum(axis=0)
        
        df7Monat = df.where((df['Tage']<= (7*(365/12)))).dropna()
        df7 = df7Monat['€'].sum(axis=0)
        
        df8Monat = df.where((df['Tage']<= (8*(365/12)))).dropna()
        df8 = df8Monat['€'].sum(axis=0)
        
        df9Monat = df.where((df['Tage']<= (9*(365/12)))).dropna()
        df9 = df9Monat['€'].sum(axis=0)
        
        df10Monat = df.where((df['Tage']<= (10*(365/12)))).dropna()
        df10 = df10Monat['€'].sum(axis=0)
        
        df11Monat = df.where((df['Tage']<= (11*(365/12)))).dropna()
        df11 = df11Monat['€'].sum(axis=0)
        
        df12Monat = df.where((df['Tage']<= (12*(365/12)))).dropna()
        df12 = df12Monat['€'].sum(axis=0)
        
        df24Monat = df.where((df['Tage']<= (24*(365/12)))).dropna()
        df24 = df24Monat['€'].sum(axis=0)
        
        dfZeit = pd.DataFrame({
            'Kostensumme':[df1, (df2-df1),(df3-df2),(df4-df3),(df5-df4),(df6-df5),(df7-df6),(df8-df7),(df9-df8),(df10-df9),(df11-df10),(df12-df11)],
            'Zeit':[b, b + datetime.timedelta(365/12), b + datetime.timedelta(365/12*2),b + datetime.timedelta(365/12*3),b + datetime.timedelta(365/12*4),b + datetime.timedelta(365/12*5),b + datetime.timedelta(365/12*6),b + datetime.timedelta(365/12*7),b + datetime.timedelta(365/12*8),b + datetime.timedelta(365/12*9),b + datetime.timedelta(365/12*10),b + datetime.timedelta(365/12*11)]})
                
        dfZeit['Zeit'] = pd.to_datetime(dfZeit['Zeit'])
        dfZeit['Zeit'] = dfZeit['Zeit'].dt.strftime('%m/%Y')
        
        dfplot = dfZeit[['Kostensumme','Zeit']].set_index('Zeit')
        zzz=dfplot.plot(kind="bar", color="darkred").get_figure()
        zzz.savefig('static/testneu.png', bbox_inches = "tight")

        dfbasicinformation = pd.DataFrame({
            'Leistung':['Marke','Modell','Erstzulassung', 'Kilometerstand', 'Motor', 'Hubraum','Verbrauch','Versicherungskosten','Steuern'],
            'Wert':[Marke,Modell,Erstzulassung,Kilometerstand,Motor,Hubraum,Verbrauch, Versicherungskosten,Steuern]}).set_index('Leistung')

        dfbasicinformation.to_csv(Dateiname2)
                
    return render_template('Costs1.html', Marke = Marke, Modell = Modell, Erstzulassung = Erstzulassung, Kilometerstand = Kilometerstand, Motor = Motor, Hubraum = Hubraum, Verbrauch = Verbrauch, Versicherungskosten = Versicherungskosten, Steuern = Steuern, Kosten1Monat = str(df1) + ' €', Kosten6Monate = str(df6) + ' €', Kosten12Monate = str(df12) + ' €', Kosten24Monate = str(df24) + ' €', tables=[df.to_html(classes='data', header="true")], Fixkosten = Fixkosten, Treibstoff = Treibstoff, LaufendeKosten = LaufendeKosten)


@app.route('/History.html')
def Geschichte():
    return render_template('History.html')





app.run()








import web, sqlite3, os
from web import form

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form( 
    form.Textbox("Altcoin Address",form.notnull), 
    form.Textbox("Bitcoin Address",form.notnull), 
    form.Textbox('Contact',form.notnull))

class index: 
    def GET(self): 
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally       
        return render.formtest(form)

    def POST(self): 
        form = myform() 
        if not form.validates(): 
            return render.formtest(form)
        else:
            conn = sqlite3.connect('sale.db')
            c = conn.cursor()
            
            if not os.path.exists('sale.db'):        
                c.execute("CREATE TABLE sale (Altcoin Address , bitcoin Address, contact)")

            conn = sqlite3.connect('sale.db')
            c = conn.cursor()
            
            c.execute("INSERT INTO sale VALUES (?,?,?)", (form['Altcoin Address'].value, form['Bitcoin Address'].value, form['Contact'].value))  # Insert a row of data
            conn.commit()
            conn.close()
            
            return "Success! Altcoin Address: %s, Bitcoin Address: %s, Contact: %s" % (form['Altcoin Address'].value, form['Bitcoin Address'].value, form['Contact'].value)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
    


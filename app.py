from distutils.log import debug
from fileinput import filename
from flask import *  


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


from tinytag import TinyTag


app = Flask(__name__, static_url_path='/static')  
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_metadata.sqlite3'

allowed_extensions = ['mp3', 'wav']

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Metadata(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    filename =  db.Column(db.String(1000))
    title =  db.Column(db.String(1000))
    filetype =  db.Column(db.String(10))
    genre =  db.Column(db.String(50))
    audio_length = db.Column(db.String(200))
    filesize =  db.Column(db.String(200))

    def __init__(self, filename, title, filetype, genre,audio_length, filesize):
       self.title = title
       self.filename = filename
       self.filetype = filetype
       self.genre = genre
       self.audio_length = audio_length
       self.filesize = filesize
       
class MetadataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metadata
        load_instance = True

    



with app.app_context():
    db.create_all()
    
    
    
    


def allowed_file(filename):
    """ checking file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
           
           



def extract_metadata(filename):
    """    extracting the metadata and 
    save the data to database"""
    audio = TinyTag.get(filename)
    
    filename = filename
    title =  audio.title
    filetype =  "audio"
    genre =  audio.genre
    audio_length =  audio.duration
    filesize =  audio.filesize
    meta_schema = MetadataSchema()

    
    save_data = Metadata(filename, title, filetype, genre,audio_length, filesize)
    db.session.add(save_data)
    db.session.commit()
   
    m = meta_schema.dump(save_data)
    return m
    
    
    
    
    
  
@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST']) 

 
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        if f.filename != '' and allowed_file(f.filename):
            path = "static/" + f.filename
            f.save(path)  
            m = extract_metadata(path)
            
            return render_template("response.html", audio_metadata = m)  
  
if __name__ == '__main__':  
    app.run(debug=True)
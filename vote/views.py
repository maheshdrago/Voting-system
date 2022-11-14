from vote.models import app
from flask import render_template,request,flash,redirect,url_for
from vote.models import *

@app.route("/")
def index():
    ele = Election.query.all()
    return render_template("index.html",ele=ele[0])


@app.route("/details",methods=["GET","POST"])
def details():
    
    parties = Party.query.all()

    return render_template("details.html",parties=parties)

@app.route("/candidate/<int:id>")
def candidate(id):
    candidate = Party.query.filter_by(id=id).first()
    return render_template("candidate.html",candidate=candidate)

@app.route("/process",methods=["POST",'GET'])
def process():
    
    if request.method=="POST":
        vcard = request.form['vcard']
        voters = Voted.query.all()
        users = Users.query.all()
        flag = False

        for i in users:
            if i.voterid==vcard:
                flag = True
        if flag:
            for i in voters:
                if i.voterid==vcard:
                    flash("You already voted....")
                    return redirect(url_for("details"))
            
            v = Voted(voterid=vcard)

            
            db.session.add(v)
            db.session.commit()

            voter_d = request.form['vote']

            party_list = ["Bharatiya Janata Party (BJP)","Congress","YSR Congress Party (YSRCP)"]
            
            index = party_list.index(voter_d)

            party_list_db = Party.query.all()
            
            item = party_list_db[index]

            item.votes = str(int(item.votes)+1)
            db.session.commit()
            
        
            return render_template("voted.html")
        else:
            flash("Voter does not exist")
            return redirect(url_for("details"))
    else:
        return redirect(url_for("details"))

@app.route("/stats")
def stats():


    
    parties = Party.query.all()
    widths = []

    for i in parties:
        widths.append(i.votes*10)
    return render_template("stat.html",parties=parties,widths=widths)
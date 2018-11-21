from flask import render_template,flash,redirect,url_for
from bs4 import BeautifulSoup as bs
from .logp import FileProxy
from .forms import LoginForm
import os, re
from . import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        logDir = form.logpath.data
        if not os.path.isdir(logDir):
            logP._usage()
            return "<p>logpath invalid!</p>"
        else:
            return redirect(url_for('report',logDir=logDir,plat=form.platform_radio.data))
    return render_template('index.html',
                            form = form)

@app.route('/report/<plat>/<logDir>')
def report(logDir,plat):
    filepl = []
    platxml = os.path.join(os.getcwd(), r'app_logp\static', plat +".xml")
    
    with open(platxml) as f:
        tag_filekey_list = bs(f.read()).find('logwrap').findChildren(recursive=False)

    for file in os.listdir(logDir):
        for t in tag_filekey_list:
            if re.search(t.name, file):
                print '-- file {} match {}'.format(file, t.name)
                filepl.append(FileProxy(t.name, os.path.join(logDir, file), platxml))
    return render_template('report.html',
                            title='Report',
                            fileproxylist = filepl)

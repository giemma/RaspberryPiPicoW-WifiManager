import os
import machine


title='TITLE'

def GetCss():
    f = open('/www/style.css', 'r')
    content = f.read()
    f.close()
    return content

def _sub_read_template_file(filename):
    f = open('/www/' + filename +'.html', 'r')
    content = f.read()
    f.close()
    return content

    
class HTMLMANAGER():
    def __init__(self, mainTitle):
        self.title = mainTitle
    
   
    def GetIndexPage(self, infoTitle, networks):
        template = _sub_read_template_file('index')
        template = template.replace('%title%',infoTitle)
        template = template.replace('%options%',networks)
        return template
        
        
    def GetInfoPage(self, infoTitle, version, osversion, hardware):
        template = _sub_read_template_file('info')
        template = template.replace('%title%',infoTitle)
        template = template.replace('%version%', version)
        template = template.replace('%os-version%', osversion)
        template = template.replace('%hardware%', hardware)
        return template
       
    def GetPasswordOkPage(self, infoTitle):
        template = _sub_read_template_file('passwordok')
        template = template.replace('%title%',infoTitle)
        return template
    
    def GetRestartingPage(self, infoTitle):
        template = _sub_read_template_file('restarting')
        template = template.replace('%title%',infoTitle)
        return template
    
    def GetStoppedPage(self, infoTitle):
        template = _sub_read_template_file('stopped')
        template = template.replace('%title%',infoTitle)
        return template
import threading
import traceback

import psutil

import urllib3 as urllib3
import xmltodict
import fichier.var as var
import fichier.design as design
import webbrowser
import os


def getxml():
    try:
        url = var.site + "/PyngOuin/changelog.xml"
        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
        response = http.request('GET', url)

        data = xmltodict.parse(response.data)
        return data
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())
        pass


def recupDerVer():
    try:
        xml = getxml()
        i = 0;
        for val in xml["changelog"]["version"]:
            if i == 0:
                verion2 = val["versio"]
                i += 1
        version1 = verion2.split(".")
        version = version1[0] + version1[1] + version1[2]
        return version
    except:
        pass


def testVersion():
    version = recupDerVer()
    versionlog = var.version.split(".")
    versionlog1 = versionlog[0] + versionlog[1] + versionlog[2]
    message = _('Une mise à jour vers la version ') + str(version) + _(' est disponible. \n Voulez vous la télécharger ?')
    if int(versionlog1) < int(version):
        val = design.question_box(_('Mise à jour'), message)
        if val == True:
            webbrowser.open(var.site + '/PyngOuin/PyngOuin%20Setup.exe')
            for process in (process for process in psutil.process_iter() if
                            process.name() == "OpenHardwareMonitor.exe"):
                process.kill()
            os._exit(0)
    else:
        pass


def main():
    try:
        testVersion()
    except:
        pass

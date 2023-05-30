# -*- coding: utf-8 -*-
# @Time : 12/23/2021 10:44
# @Author : wxy
# @File : SoilTextureCalculator.py
# @Software: PyCharm

'''
https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/survey/?cid=nrcs142p2_054167
'''
def getSand(vcs, cs, ms, fs, vfs):
    vcscs = vcs + cs
    vcscsms = vcs + cs + ms
    fsvfs = fs + vfs
    if vcscs >= 25 and ms < 50 and fs < 50 and vfs < 50:
        texture = 'Coarse Sand'
    elif (vcscsms >= 25 and vcscs < 25 and fs < 50 and vfs < 50) or (ms >= 50 or vcscs >= 25):
        texture = 'Sand'
    elif (fs >= 50 and fs > vfs) or (vcscsms < 25 and vfs < 50):
        texture = 'Fine Sand'
    elif vfs >= 50:
        texture = 'Very Fine Sand'
    else:
        texture = 'Error'
    return texture

def getLoamSand(vcs, cs, ms, fs, vfs):
    vcscs = vcs + cs
    vcscsms = vcs + cs + ms
    fsvfs = fs + vfs
    if vcscs >= 25 and ms < 50 and fs < 50 and vfs < 50:
        texture = 'Loamy Coarse Sand'
    elif vcscsms >= 25 and vcscs < 25 and fs < 50 and vfs < 50:
        texture = 'Loamy Sand'
    elif ms >= 50 and vcscs >= 25:
        texture = 'Loamy Sand'
    elif fs >= 50:
        texture = 'Loamy Fine Sand'
    elif vcscsms < 25 and vfs < 50:
        texture = 'Loamy Fine Sand'
    elif vfs >= 50:
        texture = 'Loamy Very Fine Sand'
    else:
        texture = 'Error'
    return texture

def getSandLoam(vcs, cs, ms, fs, vfs):

    vcscs = vcs + cs
    vcscsms = vcs + cs + ms
    fsvfs = fs + vfs

    if vcscs >= 25 and ms < 50 and fs < 50 and vfs < 50:
        texture = 'Coarse Sandy Loam'
    elif vcscsms >= 30 and vfs >= 30 and vfs < 50:
        texture = 'Coarse Sandy Loam'
    elif vcscsms >= 30 and vcscs < 25 and fs < 30 and vfs < 30:
        texture = 'Sandy Loam'
    elif vcscsms <= 15 and fs < 30 and vfs < 30 and fsvfs < 40:
        texture = 'Sandy Loam'
    elif vcscs >= 25 and ms >= 50:
        texture = 'Sandy Loam'
    elif fs >= 30 and vfs < 30 and vcscs < 25:
        texture = 'Fine Sandy Loam'
    elif vcscsms >= 15 and vcscsms < 30 and vcscs < 25:
        texture = 'Fine Sandy Loam'
    elif fsvfs >= 40 and fs >= vfs and vcscsms <= 15:
        texture = 'Fine Sandy Loam'
    elif vcscs >= 25 and fs >= 50:
        texture = 'Fine Sandy Loam'
    elif vfs >= 30 and vcscsms < 15 and vfs > fs:
        texture = 'Very Fine Sandy Loam'
    elif fsvfs >= 40 and vfs > fs and vcscsms < 15:
        texture = 'Very Fine Sandy Loam'
    elif vcscs >= 25 and vfs >= 50:
        texture = 'Very Fine Sandy Loam'
    elif vcscsms >= 30 and vfs >= 50:
        texture = 'Very Fine Sandy Loam'
    else:
        texture = 'Error'
    return texture

def getTexture(sand, clay, silt, detailsc=False,vcs=None, cs=None, ms=None, fs=None, vfs=None):

    if (silt + 1.5 * clay) < 15:
        if detailsc:
            texture = getSand(vcs, cs, ms, fs, vfs)
        else:
            texture = 'Sand'
    elif (silt + 1.5 * clay >= 15) and (silt + 2 * clay < 30):
        if detailsc:
            texture = getLoamSand(vcs, cs, ms, fs, vfs)
        else:
            texture = 'Loamy Sand'
    elif (clay >= 7 and clay < 20) and (sand > 52) and ((silt + 2 * clay) >= 30) or (clay < 7 and silt < 50 and (silt+2 * clay) >= 30):
        if detailsc:
            texture = getSandLoam(vcs, cs, ms, fs, vfs)
        else:
            texture = 'Sandy Loam'
    elif (clay >= 7 and clay < 27) and (silt >= 28 and silt < 50) and sand <= 52:
        texture = 'Loam'
    elif (silt >= 50 and (clay >= 12 and clay < 27)) or ((silt >= 50 and silt < 80) and clay < 12):
        texture = 'Silty Loam'
    elif silt >= 80 and clay < 12:
        texture = 'Silt'
    elif (clay >= 20 and clay < 35) and silt < 28 and sand > 45:
        texture = 'Sandy Clay Loam'
    elif (clay >= 27 and clay < 40) and (sand > 20 and sand <= 45):
        texture = 'Clay Loam'
    elif (clay >= 27 and clay < 40) and sand <= 20:
        texture = 'Silty Clay Loam'
    elif clay >= 35 and sand > 45:
        texture = 'Sandy Clay'
    elif clay >= 40 and silt >= 40:
        texture = 'Silty Clay'
    elif clay >= 40 and sand <= 45 and silt < 40:
        texture = 'Clay'
    else:
        texture = 'Undefined'
    return texture

def SWCON(texture):
    soil_type = texture[-4:]
    if soil_type=='Clay':
        sw = 0.3
    elif soil_type=='Loam':
        sw = 0.5
    elif soil_type == 'Sand':
        sw = 0.7
    return sw

def get_Salb(texture):
    if texture=='Sand':
        Salb=0.13
    elif texture=='Loamy Sand':
        Salb=0.16
    elif texture=='Sandy Loam':
        Salb=0.13
    elif texture=='Loam':
        Salb=0.13
    elif texture=='Silty Loam':
        Salb=0.14
    elif texture=='Silt':
        Salb=0.14
    elif texture=='Sandy Clay Loam':
        Salb=0.13
    elif texture=='Clay Loam':
        Salb=0.13
    elif texture=='Silty Clay Loam':
        Salb=0.12
    elif texture=='Sandy Clay':
        Salb=0.12
    elif texture=='Silty Clay':
        Salb=0.12
    elif texture=='Clay':
        Salb=0.12
    else:
        Salb = 0.13
    return Salb

def get_CN2b(texture):
    if texture=='Sand':
        CN2b=68
    elif texture=='Heavy Clay':
        CN2b=68
    elif texture=='Loamy Clay':
        CN2b=84
    elif texture=='Loam':
        CN2b=73
    elif texture=='Sandy loam':
        CN2b=68
    elif texture=='Loamy sand':
        CN2b = 73
    elif texture=='Sandy clay':
        CN2b = 68
    elif texture=='Clay loam':
        CN2b = 73
    elif texture=='Sandy clay loam':
        CN2b = 73
    elif texture=='Loamy sand':
        CN2b = 73
    else:
        CN2b = 73
    return CN2b



def get_Diffus(texture):
    soil_type = texture[-4:]
    if soil_type=='Clay':
        DiffusConst = 40
        DiffusSlope = 16
    elif soil_type=='Loam':
        DiffusConst = 88
        DiffusSlope = 35
    elif soil_type == 'Sand':
        DiffusConst = 250
        DiffusSlope = 22
    return DiffusConst,DiffusSlope
import glob

vislist = glob.glob('*[!_t].ms')  # match full ms, not target.ms

for myvis in vislist:

    msmd.open(myvis)
    targetspws = msmd.spwsforintent('OBSERVE_TARGET*')  
    sciencespws = []                                      
    for myspw in targetspws:                               
        if msmd.nchan(myspw)>4:
            sciencespws.append(myspw)
    sciencespws = ','.join(map(str,sciencespws))
    msmd.close()
    
    split(vis=myvis,outputvis=myvis+'.split.cal',spw=sciencespws)

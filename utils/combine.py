import glob
vislist=glob.glob('*.ms.split.cal')

# in CASA
concatvis='calibrated.ms'

rmtables(concatvis)
os.system('rm -rf ' + concatvis + '.flagversions')
concat(vis=vislist,
       #forcesingleephemfield='Uranus', # uncomment this line and insert source name if imaging an ephemeris object
       concatvis=concatvis)

concatvis='calibrated.ms'
sourcevis='calibrated_source.ms'
rmtables(sourcevis)
os.system('rm -rf ' + sourcevis + '.flagversions')
split(vis=concatvis,
  intent='*TARGET*', # split off the target sources
  outputvis=sourcevis,
  datacolumn='data')

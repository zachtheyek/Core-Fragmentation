# split out the data
# width=128 averages all channels together, here we will not perform averaging
listobs('calibrated_source.ms')
fieldname='183640.3-023402'
split(vis='calibrated_source.ms',outputvis='field_43_cont.ms',field=fieldname,datacolumn='data',spw='0,1,2,4,5,6,8,9,10',width=1)


# Make a first-pass image using interactive cleaning
'''
  clean fills results into model column
  clean runs on corrected unless it doesn't exist, then off data
  starts by showing dirty image
  select brightest sources, run ~10 iterations (100 cycles)
'''
tclean(vis='field_43_cont.ms',field=fieldname,spw='0,1,2,3,4,5,6,7,8',imagename='field_43_cont_selfcal0',specmode='mfs',deconvolver='clark',imsize=[500,500],cell=0.25,weighting='briggs',robust=2.0,threshold='0mJy',niter=5000,interactive=True,gridder='standard',savemodel='modelcolumn',usepointing=False)
### Zach: draw circle around bright source, iterate 3-ish times (one at a time-ish) for 10 cycles. Open selfcal0.image to confirm bright source (if nothing there then something wrong).


# Now try selfcal
'''
  gaincal derives solution by comparing data to model (where model comes from clean)
  combine='spw' to get one solution over all spw
  applycal puts result into corrected column
  clean again, go deeper as the data allows
  don't clean all the way down to the noise, it's ok to leave lots of extended emission
  clean out all the brighter compact emission, and some of the brightest extended emission
  clean overrides what is in the model column (which is ok, since each clean iteration improves the result)
'''
gaincal(vis='field_43_cont.ms',spw='0,1,2,3,4,5,6,7,8',caltable='field_43_phase1.cal',field=fieldname,solint='inf',calmode='p',refant='DV11',gaintype='T',combine='spw',minsnr=3.0,minblperant=6)
### Zach: if too many flags (>20% of total), then selfcal wouldn't help much. but, if most flags are in the same spw, e.g. 20% of spw=0, then it's fine.
#plotcal(caltable='field_43_phase1.cal',xaxis='time',yaxis='phase',subplot=331,iteration='antenna',plotrange=[0,0,-180,180],markersize=5,fontsize=10.0,figfile='field_43_selfcal1_phase.png')
applycal(vis='field_43_cont.ms',field=fieldname,gaintable=['field_43_phase1.cal'],interp='linear',spwmap=[0,0,0,3,3,3,6,6,6])
tclean(vis='field_43_cont.ms',field=fieldname,spw='0,1,2,3,4,5,6,7,8',imagename='field_43_cont_selfcal1',specmode='mfs',deconvolver='clark',imsize=[500,500],cell=0.25,weighting='briggs',robust=2.0,threshold='0mJy',niter=5000,interactive=True,gridder='standard',savemodel='modelcolumn',usepointing=False)
### Zach: same thing, more iterations/cycles, run till the faint stuff gets more noticable, then we expand regions. go until noise is about similar to the edge colors of the source.


# Round 2
'''
  if solint is too small, you will get lots of flagged solutions
  applycal will overwrite corrected column (which is ok, because we are improving the corrections)
  clean as deep as possible to get all the flux before amplitude calibration
'''
gaincal(vis='field_43_cont.ms',spw='0,1,2,3,4,5,6,7,8',caltable='field_43_phase2.cal',field=fieldname,solint='30s',calmode='p',refant='DV11',gaintype='T',combine='spw',minsnr=3.0,minblperant=6)
#plotcal(caltable='field_43_phase2.cal',xaxis='time',yaxis='phase',subplot=331,iteration='antenna',plotrange=[0,0,-180,180],markersize=5,fontsize=10.0,figfile='field_43_selfcal2_phase.png')
applycal(vis='field_43_cont.ms',field=fieldname,gaintable=['field_43_phase2.cal'],interp='linear',spwmap=[0,0,0,3,3,3,6,6,6])
tclean(vis='field_43_cont.ms',field=fieldname,spw='0,1,2,3,4,5,6,7,8',imagename='field_43_cont_selfcal2',specmode='mfs',deconvolver='clark',imsize=[500,500],cell=0.25,weighting='briggs',robust=2.0,threshold='0mJy',niter=5000,interactive=True,gridder='standard',savemodel='modelcolumn',usepointing=False)
### Zach: Keep going until surroundings are just as if not brighter than source. Don't be afraid to include noise in region. 



#--------------------- just start with phase self-cal for now, leave this until later ---------------------#

# Amplitude calibration
'''
  you should use solnorm=True
  since you cleaned deep, use previous phase solution to avoid junk
  when you apply the cal, now apply both this amplitude and the previous phase
  check solutions, plot 0-2
'''
gaincal(vis='hbc722_selfcal.ms',caltable='amplitude.cal',gaintable='phase2.cal',field='HBC722',solint='240s',calmode='ap',refant='DV12',gaintype='G',combine='spw',spwmap=[0,0,0,0],solnorm=True)
applycal(vis='hbc722_selfcal.ms',field='HBC722',gaintable=['amplitude.cal','phase2.cal'],interp='linear',spwmap=[[0,0,0,0],[0,0,0,0]])
plotcal(caltable='amplitude.cal',xaxis='time',yaxis='amp',subplot=331,iteration='antenna',plotrange=[0,0,0,2],markersize=5,fontsize=10.0,figfile='selfcal1_amplitude.png')
clean(vis='hbc722_selfcal.ms',imagename='hbc722_selfcal3',mode='mfs',psfmode='clark',imsize=[300,300],cell=0.2,weighting='briggs',robust=2.0,threshold='0mJy',interactive=True,usescratch=True,mask='hbc722_selfcal2.mask')
clean(vis='hbc722_selfcal.ms',imagename='hbc722_selfcal3_nterms2',nterms=2,mode='mfs',psfmode='clark',imsize=[300,300],cell=0.2,weighting='briggs',robust=2.0,threshold='0mJy',interactive=True,usescratch=True,mask='hbc722_selfcal2.mask')

exportfits(imagename='hbc722_selfcal2.image',fitsimage='hbc722_selfcal2.fits',overwrite=True)
exportfits(imagename='hbc722_selfcal3.image',fitsimage='hbc722_selfcal3.fits',overwrite=True)
exportfits(imagename='hbc722_selfcal3_nterms2.image.tt0',fitsimage='hbc722_selfcal3_nterms2_image.fits',overwrite=True)
exportfits(imagename='hbc722_selfcal3_nterms2.image.alpha',fitsimage='hbc722_selfcal3_nterms2_alpha.fits',overwrite=True)
exportfits(imagename='hbc722_selfcal3_nterms2.image.alpha.error',fitsimage='hbc722_selfcal3_nterms2_dalpha.fits',overwrite=True)

clean(vis='hbc722_selfcal.ms',imagename='hbc722_selfcal3_rm2',mode='mfs',psfmode='clark',imsize=[600,600],cell=0.1,weighting='briggs',robust=-2.0,threshold='0mJy',interactive=True,usescratch=True,mask='hbc722_selfcal2.mask')
exportfits(imagename='hbc722_selfcal3_rm2.image',fitsimage='hbc722_selfcal3_rm2.fits',overwrite=True)


clean(vis='hbc722_selfcal.ms',imagename='hbc722_selfcal3_224',spw='0',mode='mfs',psfmode='clark',imsize=[300,300],cell=0.2,weighting='briggs',robust=2.0,threshold='0mJy',interactive=False,niter=10000,usescratch=True,mask='hbc722_selfcal2.mask')
clean(vis='hbc722_selfcal.ms',imagename='hbc722_selfcal3_242',spw='3',mode='mfs',psfmode='clark',imsize=[300,300],cell=0.2,weighting='briggs',robust=2.0,threshold='0mJy',interactive=False,niter=10000,usescratch=True,mask='hbc722_selfcal2.mask')

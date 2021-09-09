msmd.open('calibrated_source.ms')
sourcelist=msmd.fieldnames()
msmd.done()

for source in sourcelist:
    tclean(vis='calibrated_source.ms',field=source,spw='0,1,2,4,5,6,8,9,10',imagename='continuum/'+source,specmode='mfs',deconvolver='clark',imsize=[300,300],cell=0.25,weighting='briggs',niter=0,robust=2.0,threshold='0.1mJy',interactive=False,gridder='standard')

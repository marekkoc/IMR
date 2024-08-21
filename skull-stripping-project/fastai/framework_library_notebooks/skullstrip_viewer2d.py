#!/usr/bin/env python
"""
(C) MMIV
ML group

MK & ASL & AL

C: 2018.12.01
M: 2020.08.19

ver: 0.03

based on:
    /media/marek/data2T/Dropbox/p1ext4_P/no_work/skullstrip/cody/cody_local/skullstrip_viewer2d/skullstrip-viewer2d.py
"""
#from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import MultiCursor


class MaskViewer(object):
    def __init__(self, im1, im2, im3, cmap, dim = 2, title='Image', **kw):


        asp = kw.get('aspect', 1)
        self.fig, self.axs  = plt.subplots(1,4,sharex=True, sharey=True, figsize=(10,6))
        self.fig.subplots_adjust(left=0.2, bottom=0.2)

        self.ax1, self.ax2, self.ax3, self.ax4 = self.axs

        plt.suptitle('Use scroll to navigate')

        self.cmap = cmap
        self.dim = dim
        self.aspect = asp

        self.X1 = im1 / im1.max()
        self.X2 = im2
        self.X3 = im3

        self.rows, self.cols, self.slices = self.X1.shape
        self.x20 = np.zeros((self.cols, self.slices, 3))
        self.x30 = np.zeros((self.cols, self.slices, 3))
        self.x40 = np.zeros((self.cols, self.slices, 3))
        self.x21 = np.zeros((self.rows, self.slices, 3))
        self.x31 = np.zeros((self.rows, self.slices, 3))
        self.x41 = np.zeros((self.rows, self.slices, 3))
        self.x22 = np.zeros((self.rows, self.cols, 3))
        self.x32 = np.zeros((self.rows, self.cols, 3))
        self.x42 = np.zeros((self.rows, self.cols, 3))


        X = [self.X1, self.X2, self.X3]
        #_ = [print(x.shape) for x in X]

        self.suptitle = title
        self.title1 = 'Image'
        self.title2 = 'FLS'
        self.title3 = 'Prediction'
        self.title4 = 'FSL & Prediction'

        self.ax1.set_title(self.title1)
        self.ax2.set_title(self.title2)
        self.ax3.set_title(self.title3)
        self.ax4.set_title(self.title4)

        mn1, mx1 = self.X1.min(), self.X1.max()
        mn2, mx2 = self.X2.min(), self.X2.max()
        mn3, mx3 = self.X3.min(), self.X3.max()

#        av = (mn + mx) / 2
#        txt = "min={:.2f}, av={:.2f}, max={:.2f}, dtype={}, shape={}".format(mn, av, mx, self.X1.dtype, self.X1.shape)
#        self.fig.text(0.05,0.03, txt)

        slidercolor = 'lightgoldenrodyellow'
        slideraxes = self.fig.add_axes([0.25, 0.1, 0.65, 0.05], facecolor=slidercolor)

#        asp = list(self.nii.header['pixdim'][1:4])
#        arows, acols, aslices = asp
        if dim == 0:
            self.rot = True
            self.ind = self.rows//2
            self.im1 = self.ax1.imshow(self.X1[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.im2 = self.ax2.imshow(self.X2[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.im3 = self.ax3.imshow(self.X3[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.im4 = self.ax4.imshow(self.X1[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.slider = Slider(slideraxes, 'Slice.', 0, self.rows-1, valinit=self.ind, valfmt='%i')
        elif dim == 1:
            #self.aspect = (arows * self.rows) / (aslices * self.slices)

            self.rot = True
            self.ind = self.cols//2
            self.im1 = self.ax1.imshow(self.X1[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.im2 = self.ax2.imshow(self.X2[self.ind, :, :], vmin=mn2, vmax=mx2)
            self.im3 = self.ax3.imshow(self.X3[self.ind, :, :], vmin=mn3, vmax=mx3)
            self.im4 = self.ax4.imshow(self.X1[self.ind, :, :], vmin=mn3, vmax=mx3)
            self.slider = Slider(slideraxes, 'Slice.', 0, self.cols-1, valinit=self.ind, valfmt='%i')
        elif dim == 2:
            #self.aspect = (arows * self.rows) / (acols * self.cols)
            self.rot = False
            self.ind = self.slices//2
            self.im1 = self.ax1.imshow(self.X1[self.ind, :, :], vmin=mn1, vmax=mx1)
            self.im2 = self.ax2.imshow(self.X2[self.ind, :, :], vmin=mn2, vmax=mx2)
            self.im3 = self.ax3.imshow(self.X3[self.ind, :, :], vmin=mn3, vmax=mx3)
            self.im4 = self.ax4.imshow(self.X1[self.ind, :, :], vmin=mn3, vmax=mx3)
            self.slider = Slider(slideraxes, 'Slice.', 0, self.slices-1, valinit=self.ind, valfmt='%i')

        _ = [a.set_aspect(self.aspect) for a in self.axs]
        _ = [a.axis('off') for a in self.axs]
        _ = [i.set_cmap(self.cmap) for i in [self.im1, self.im2, self.im3]]

        self.slider.on_changed(self.update_slider)

        self.update()
        self.cursor = MultiCursor(self.fig.canvas,
                            (self.ax1, self.ax2, self.ax3, self.ax4),
                            color='g', lw=1, horizOn=True, vertOn=True)
        self.cursor.visible = False

        self.fig.canvas.mpl_connect('key_press_event', self.onKeyButtonPress)
        self.fig.canvas.mpl_connect('scroll_event', self.onscroll)
        plt.tight_layout()

        plt.show()

    def onKeyButtonPress(self, event):
        if event.key == 'c':
            self.cursor.visible = not self.cursor.visible
        self.fig.canvas.draw()


    def onscroll(self, event):
        #print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.slider.set_val(self.ind)
        self.update()

    def update_slider(self, val):
        self.ind = int(val);
        self.update()

    def update(self):
#        if self.rot:
#            self.im.set_data(self.X1[:, :, self.ind].T)
#        else:
#            self.im.set_data(self.X1[:, :, self.ind])
        if self.dim == 0:
            self.x20[:,:,0] = self.X2[self.ind, :, :]
            self.x20[:,:,1] = self.X1[self.ind, :, :]
            self.x20[:,:,2] = self.X1[self.ind, :, :]

            self.x30[:,:,0] = self.X1[self.ind, :, :]
            self.x30[:,:,1] = self.X1[self.ind, :, :]
            self.x30[:,:,2] = self.X3[self.ind, :, :]

            self.x40[:,:,0] = self.X2[self.ind, :, :]
            self.x40[:,:,1] = self.X1[self.ind, :, :]
            self.x40[:,:,2] = self.X3[self.ind, :, :]

            if self.rot:
                self.im1.set_data(np.rot90(self.X1[self.ind, :, :], 1))
                self.im2.set_data(np.rot90(self.x20, 1))
                self.im3.set_data(np.rot90(self.x30, 1))
                self.im4.set_data(np.rot90(self.x40, 1))
            else:
                self.im1.set_data(self.X1[self.ind, :, :])
                self.im2.set_data(np.rot90(self.x20, 1))
                self.im3.set_data(np.rot90(self.x30, 1))
                self.im4.set_data(np.rot90(self.x40, 1))
        elif self.dim == 1:
            self.x21[:, :, 0] = self.X2[:, self.ind, :]
            self.x21[:, :, 1] = self.X1[:, self.ind, :]
            self.x21[:, :, 2] = self.X1[:, self.ind, :]

            self.x31[:, :, 0] = self.X1[:, self.ind, :]
            self.x31[:, :, 1] = self.X1[:, self.ind, :]
            self.x31[:, :, 2] = self.X3[:, self.ind, :]

            self.x41[:, :, 0] = self.X2[:, self.ind, :]
            self.x41[:, :, 1] = self.X1[:, self.ind, :]
            self.x41[:, :, 2] = self.X3[:, self.ind, :]

            if self.rot:
                self.im1.set_data(np.rot90(self.X1[:, self.ind, :], 1))
                self.im2.set_data(np.rot90(self.x21, 1))
                self.im3.set_data(np.rot90(self.x31, 1))
                self.im4.set_data(np.rot90(self.x41, 1))
            else:
                self.im1.set_data(self.X1[:, self.ind, :])
                self.im2.set_data(self.x21)
                self.im3.set_data(self.x31)
                self.im4.set_data(self.x41)
        elif self.dim == 2:
            self.x22[:,:,0] = self.X2[:, :, self.ind]
            self.x22[:,:,1] = self.X1[:, :, self.ind]
            self.x22[:,:,2] = self.X1[:, :, self.ind]

            self.x32[:,:,0] = self.X1[:, :, self.ind]
            self.x32[:,:,1] = self.X1[:, :, self.ind]
            self.x32[:,:,2] = self.X3[:, :, self.ind]

            self.x42[:,:,0] = self.X2[:, :, self.ind]
            self.x42[:,:,1] = self.X1[:, :, self.ind]
            self.x42[:,:,2] = self.X3[:, :, self.ind]

            if self.rot:
                self.im1.set_data(self.X1[:, :, self.ind].T)
                self.im2.set_data(self.x22.T)
                self.im3.set_data(self.x32.T)
                self.im4.set_data(self.x42.T)
            else:
                self.im1.set_data(self.X1[:, :, self.ind])
                self.im2.set_data(self.x22)
                self.im3.set_data(self.x32)
                self.im4.set_data(self.x42)

        plt.suptitle('%s - slice %s' % (self.suptitle, self.ind))

        self.fig.canvas.draw()
        #self.im2.axes.figure.canvas.draw()
        #self.im3.axes.figure.canvas.draw()



if __name__ =='__main__':

    import nibabel as nib
    from pathlib import Path

    main_Path = Path('.')

    t1FolderPath = main_Path / 'data_T1'
    fslMaskFolderPath = main_Path / 'data_FSL_mask'
    niftyNetMaskFolderPath = main_Path / 'data_NiftyNet_mask'

    t1Name = 'T1_biascorr.nii.gz'
    fslName = 'T1_biascorr_brain_mask.nii.gz'
    niftynetName = 'window_seg_IXI081-Guys-0855-T1.anat__niftynet_out.nii.gz'

    t1Path = t1FolderPath / t1Name
    fslPath = fslMaskFolderPath / fslName
    niftynetPath = niftyNetMaskFolderPath / niftynetName

    t1Nii = nib.load(t1Path)
    fslNii = nib.load(fslPath)
    niftyNii = nib.load(niftynetPath)

    x1 = t1Nii.get_fdata()
    x2 = fslNii.get_fdata()
    x3 = niftyNii.get_fdata()

    cmap = 'gray'
    tracker = IndexTracker(x1, x2, x3, cmap, dim = 2, title='Tu powinna byc nazwa pacjenta')


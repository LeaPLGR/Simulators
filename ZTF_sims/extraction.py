import numpy as np
import warnings
import pandas as pd 
warnings.filterwarnings('ignore')
import sep


class Extraction:
    
    """
    
    Parameter:
        
        path: 'string'

    """
    
#################################################

 
    def __init__(self, path ):
        
        self.path = path
        self.ID = np.load(self.path)['ztf_ID'].tolist()
        self.TS = np.load(self.path, allow_pickle = True)['ztf_time_series_images'].tolist()
        
        
        
#################################################

    def make_catalog(self, images, lvl=3):
        
        bkg = sep.Background(images)
        catalog = sep.extract(images, lvl, err=bkg.globalrms)
        if len(catalog)!=0:
            return catalog, bkg
        else: 
            while lvl>0:
                lvl = lvl-1
                catalog = sep.extract(images, lvl, err=bkg.globalrms)
                if len(catalog)!=0:
                    return catalog, bkg
        
        
#################################################

    def make_dataframe(self, cube_images):
        
        list_bkg = []
        f = 0
        F=0
        for i in range(len(cube_images)):
            
            catalog = self.make_catalog(cube_images[i])[0]
            bkg = self.make_catalog(cube_images[i])[1]
            
            if i == 0:
                f = pd.DataFrame(catalog)
                
            else:
                F = pd.DataFrame(catalog)
                f = pd.concat([f, F], ignore_index=True)
            
            list_bkg.append(bkg.globalrms)
                    
        return f, list_bkg

###################################################

    def select(self):
        data = []
        background = []

        for i in range(len(self.TS)):
            if len(self.TS[i])!=0:                      # some TS lists were empty so I supprim them
                a = self.make_dataframe(self.TS[i])
                data.append(a[0])
                background.append(a[1])
        
            else:
                print('{} was empty'.format(self.ID[i]))
                del(self.ID[i])
        
        return data, background
    
######################################################
        
    def mask_center(self, data):
        
        
        mask = (data['x'] >= 23.4) & (data['x'] <= 25.5)
        data = data[mask]
        mask2 = (data['y'] >= 23.4) & (data['y'] <= 25.5)
        
        return data[mask2]
        
######################################################

    def take_center(self):
        
    
        data = self.select()[0]
        data_center = [self.mask_center(data[i]) for i in range(len(data))]
    
        return data_center
        
######################################################


    def take_position(self):
        
        data_center = self.take_center()
        new = [i[['x', 'y']] for i in data_center]
            
        return new

######################################################

    def take_flux(self):
        
        data_center = self.take_center()
        flux = [i[['cflux']] for i in data_center]
        
        return flux


        
        
E = Extraction('data/ZTF_data/ZTF_data_1.npz')

        



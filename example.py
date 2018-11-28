import E2SIFP
import numpy as np
from PIL import Image
def func(ui):
    image = np.array(Image.open(ui.openImgUrl))
    image = image.dot([0.07, 0.72, 0.21])
    ui.setOutputImag(image)
    
if __name__=='__main__':
    ui = E2SIFP.mainUi('Image Conv Gray')
    ui.setFunc(func)
    ui.setFuncPara(ui)
    ui.show()
    
import cv2
import os
def match(element):
    return bool(element[len(element)-3:len(element)] == 'png' )
path = os.getcwd()+'/images/'
images = [i for i in os.listdir(path)]
images = list(filter(match,images))
#print(images)
for i in images:
    print(i)
    image = cv2.imread(path + i)
    image = cv2.resize(image,(8,8))
    cv2.imshow(i,image)
    cv2.waitKey(0) 
cv2.destroyAllWindows()        
print("voilà")

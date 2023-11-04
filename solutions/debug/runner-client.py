from ModuleConnect import connectGetTrackingObjects
import cv2

def main():
    con = connectGetTrackingObjects(host='localhost')
    while True:
        img = con.getImage()
        cv2.imshow('Image', img)
        match cv2.waitKey(1):
            case 27: break

if __name__ == '__main__':
    main()

# khadas
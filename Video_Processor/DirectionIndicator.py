import cv2

def message_generator(frame, bounding_box, relative_area): 
    minArea = 0.05
    maxArea = 0.25

    
    posx, posy = bounding_box[0] -230 + bounding_box[2]//2 , bounding_box[1] - 25
    if posx <0:
        posx =0
    elif posx > frame.shape[1]-460:
        posx = frame.shape[1]-460
    if posy <0:
        posy=0
    pos = (posx, posy)
        
    needsPrint = True

    if relative_area > maxArea:
        text = "Move away from the camera!"
    elif relative_area < minArea:
        text = "Move closer to the camera!"
    else: 
        needsPrint = False

    if needsPrint:
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame
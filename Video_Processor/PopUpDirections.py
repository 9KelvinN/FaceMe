import cv2
color = (0,255,255)
thickness = 5

def addDirection (frame, xDifference, yDifference, min_x = 0.25, min_y = 0.25):
    frame_height, frame_width = int(frame.shape[0]), int(frame.shape[1])
    arrowLength, initialPad = 30, 5

    #Add NE Arrow
    if (xDifference >0 and yDifference<0):
        scalar = (decimalOffset(xDifference, min_x) + decimalOffset(yDifference, min_y)) / 2
        arrowLength = int(arrowLength * (1 + scalar))
        start= (initialPad, frame_height - initialPad)
        end = (start[0] + arrowLength, start[1] - arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add NW Arrow
    elif (xDifference<0 and yDifference<0):
        scalar = (decimalOffset(xDifference, min_x) + decimalOffset(yDifference, min_y)) / 2
        arrowLength = int(arrowLength * (1 + scalar))
        start= (frame_width - initialPad , frame_height - initialPad)
        end = (start[0] - arrowLength, start[1] - arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add SE Arrow
    elif (xDifference >0 and yDifference>0):
        scalar = (decimalOffset(xDifference, min_x) + decimalOffset(yDifference, min_y)) / 2
        arrowLength = int(arrowLength * (1 + scalar))
        start= (initialPad, initialPad)
        end = (start[0] + arrowLength, start[1] + arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add SW Arrow
    elif (xDifference <0 and yDifference>0):
        scalar = (decimalOffset(xDifference, min_x) + decimalOffset(yDifference, min_y)) / 2
        arrowLength = int(arrowLength * (1 + scalar))
        start= (frame_width - initialPad, initialPad)
        end = (start[0] - arrowLength, start[1] + arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add N Arrow
    elif (xDifference ==0 and yDifference<0):
        scalar = decimalOffset(yDifference, min_y)
        arrowLength = int(arrowLength * (1 + scalar))
        start= (frame_width // 2, frame_height - initialPad)
        end = (start[0], start[1] - arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add E Arrow
    elif (xDifference >0 and yDifference==0):
        scalar = decimalOffset(xDifference, min_x)
        arrowLength = int(arrowLength * (1 + scalar))
        start= (initialPad, frame_height // 2)
        end = (start[0] + arrowLength, start[1])
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add S Arrow
    elif (xDifference==0 and yDifference>0):
        scalar = decimalOffset(yDifference, min_y)
        arrowLength = int(arrowLength * (1 + scalar))
        start= (frame_width // 2, initialPad)
        end = (start[0], start[1] + arrowLength)
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)
    #Add W Arrow
    elif (xDifference <0 and yDifference==0):
        scalar = decimalOffset(xDifference, min_x)
        arrowLength = int(arrowLength * (1 + scalar))
        start= (frame_width - initialPad, frame_height//2)
        end = (start[0] - arrowLength, start[1])
        frame = cv2.arrowedLine(frame, start, end, 
                                (0, 255 * (1 - scalar), 255), 
                                int(thickness * (1 + scalar)), tipLength = 0.5)

def decimalOffset(difference, min_offset):
    return (abs(difference) - min_offset) / (1 - min_offset)     
    
        

import cv2
import base64
from google.cloud import vision
import time 

client = vision.ImageAnnotatorClient.from_service_account_file("path to api key")

def get_face_coordinates(frame): 
    global client
    content = cv2.imencode('.jpg', frame)[1].tostring()
    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    face_coordinates = []
    try:
        for face in faces:
            vertices = [frame.shape[1], frame.shape[0], 0, 0]
            for vertex in face.bounding_poly.vertices: 
                x, y = vertex.x, vertex.y
                vertices[0] = min(vertices[0], x)
                vertices[1] = min(vertices[1], y)
                vertices[2] = max(vertices[2], x)
                vertices[3] = max(vertices[3], y)
            bounding_box = (vertices[0], vertices[1], vertices[2] - vertices[0], vertices[3] - vertices[1])
            face_coordinates.append(bounding_box)
    except Exception as e: 
        pass
    return face_coordinates

if __name__ == "__main__": 
    start = time.time()
    image = cv2.imread("TestImage.jpg")
    coordinates = get_face_coordinates(image)
    end = time.time()
    print("Got " + str(coordinates) + " in " + str(end - start))

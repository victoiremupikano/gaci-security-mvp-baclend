import cv2
from simple_facerec import SimpleFacerec

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("../media/Images/Datasource/")

# une fonction qui prend en parametre l'url de l'appareil qui stream la video
def throw_acknowledgement(url, key):
    cap = cv2.VideoCapture(0)
    # utilisation de la video streamer en reseau
    # url_vid_stream = url
    # cap.open(url_vid_stream)

    while True:
        ret, frame = cap.read()

        # Detection des faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        cv2.imshow("Frame", frame)
        
        # verification de correspondance
        # val de retour
        results = ""
        if len(face_names) == 0 :
            results = 'Pas des correspondance trouvé...'
            print('Pas des correspondance trouvé...')
            
        else:
            results = 'Correspondance trouvé...'
            print('Correspondance trouvé...')
        key = cv2.waitKey(1)
        # on arret le streaming en appuyant sur 27
        if key == "q":
            break
        
        return results

    cap.release()
    cv2.destroyAllWindows()
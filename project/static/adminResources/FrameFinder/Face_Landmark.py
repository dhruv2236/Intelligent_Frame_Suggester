import math
import os
from glob import glob

import cv2
import dlib
from imutils import face_utils
from werkzeug.utils import secure_filename


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# This method is used to get third point in line of x1,x2 and y1,y2
# It will return y for x in the parameter
def linear_point(x1, x2, y1, y2, y):
    if (x2 - x1) != 0:
        m = (y2 - y1) / (x2 - x1)
    else:
        m = 0
    # slope is m and c is  ax + by+c =0
    # getting c by putting one cordinate
    c = y1 - (m * x1)

    if m != 0:
        try:
            x = int((y - c) / m)
        except Exception as err:
            print(err)
            x = 0
    else:
        x = x2
    return x


def getIntersectionPoint(m1, m2, c1, c2, x):
    if (m2 - m1) != 0:
        x = int(round((c1 - c2) / (m2 - m1), 0))
    else:
        x = x
    y = (m2 * x) + (c2)
    y = int(round(y, 0))
    return x, y


def drawFaceSketch(img):
    img.save(os.path.join('project/static/adminResources/outputImage/' + secure_filename(img.filename)))

    response = {
        'Shape': '',
        'Note': 'No image',
        'Status': False
    }

    if allowed_file(img.filename):
        print('Valid image')
    else:
        response['Note'] = 'File type must be in jpg, png or jpeg format'
        return response

    # initialize dlib's face detector (HOG-based) and then create
    detector = dlib.get_frontal_face_detector()

    # the facial landmark predictor
    predictor = dlib.shape_predictor(r"project/static/adminResources/FrameFinder/Face_Shape_Landmark.dat")

    face_shape = ""
    image = cv2.imread(os.path.join('project/static/adminResources/outputImage/' + secure_filename(img.filename)))
    # image = imutils.resize(image, width=512)

    h, w, c = image.shape
    print('Image Size {} X {}'.format(w, h))

    if abs(h - w) < 5:
        print('Valid Size')
    elif w < 512:
        response['Note'] = 'Image size is too small'
        return response
    else:
        response['Note'] = 'Height and width of an image must be same'
        print('Height and width of an image must be same')
        print('Handle the Image Size using Resize Function')

        # return response

    image = cv2.resize(image, (512, 512), cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print('Image Shape', gray.shape)
    # detect faces in the grayscale image
    rects = detector(gray, 1)

    if len(rects) > 1:
        response['Note'] = 'There must be only one person in the image'
        return response
    elif len(rects) == 0:
        response['Note'] = 'Cannot recognize the face'
        return response
    # loop over the face detections
    for (i, rect) in enumerate(rects):

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        my_shape = []
        h, w, c = image.shape

        count = 0
        for (x, y) in shape:
            my_shape.append([x, y])
            cv2.circle(image, (x, y), 2, (255, 25, 180), -1)

            # cv2.putText(image, "{}".format(count), (x - 2, y - 2),
            #  			cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            # cv2.putText(image1, "{}".format(count), (x - 2, y - 2),
            # 			cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
            count += 1

        # nose length
        # get forehead points on line by using line equation

        s27 = shape[27].ravel()
        s57 = shape[57].ravel()
        # cv2.line(image, (s1[0], s1[1]), (s2[0], s2[1]), (0, 255, 0), 2)
        x = math.sqrt(math.pow(s27[0] - s57[0], 2) + math.pow(s27[1] - s57[1], 2))

        # to get point on forehead
        x = int(x)
        y = s27[1] - x

        x1 = s27[0]
        y1 = s27[1]
        x2 = s57[0]
        y2 = s57[1]

        x = linear_point(x1, x2, y1, y2, y)

        cv2.circle(image, (x, y), 3, (153, 102, 51), -1)

        # print('Forehead point:', x, y)
        f_x = x
        f_y = y

        s22 = shape[22].ravel()
        x1 = s22[0]
        y1 = s22[0]

        s52 = shape[52].ravel()
        x2 = s52[0]
        y2 = s52[1]

        x = linear_point(x1, x2, y1, y2, y)

        # cv2.circle(image, (x, y), 3, (15, 0, 255), -1)
        # print('Forehead point 2:', x, y)
        f2_x = x
        f2_y = y

        s8 = shape[8].ravel()
        x2 = s8[0]
        y2 = s8[1]
        face_length = round(math.sqrt(math.pow(f_x - x2, 2) + math.pow(f_y - y2, 2)), 0)

        s16 = shape[16].ravel()
        x1 = s16[0]
        y1 = s16[1]

        # cv2.line(image, (f_x, f_y), (s2[0], s2[1]), (20, 130, 70), 2)
        # print('Face Length',face_length)
        # print('Face Width',face_width)

        s0 = shape[0].ravel()
        x1 = s0[0]
        y1 = s0[1]

        s16 = shape[16].ravel()
        x2 = s16[0]
        y2 = s16[1]

        slope_w = (y2 - y1) / (x2 - x1)
        face_width = round(math.sqrt(math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2)), 0)

        face_center_x = int((x1 + x2) / 2)
        face_center_y = int((y1 + y2) / 2)

        # cv2.line(image, (s1[0], s1[1]), (s2[0], s2[1]), (91, 238, 197), 1)
        cv2.line(image, (x1, y1), (x2, y2), (0, 48, 125), 1)

        s3 = shape[8].ravel()
        x3 = s3[0]
        y3 = s3[1]

        if (face_center_x - x3) != 0:
            slope_l = (face_center_y - y3) / (face_center_x - x3)
        else:
            slope_l = 0
        tan_a = slope_w
        tan_b = slope_l

        tan_angle = (tan_a - tan_b) / (1 + (tan_a * tan_b))

        angle = math.atan(tan_angle)
        angle = math.degrees(angle)
        angle = 90 - angle
        # print('angle', angle)

        # distance from center of eyeline to point 8 to draw an ellipse
        face_half_length = round(math.sqrt(math.pow(face_center_y - y3, 2) + math.pow(x3 - face_center_x, 2)), 0)
        cv2.circle(image, (face_center_x, face_center_y), 3, (255, 255, 0), -1)

        # ellipse made by face height,width, face center(x,y)---start

        cv2.ellipse(img=image, center=(face_center_x, face_center_y), axes=(int(face_width / 2), int(face_half_length)),
                    angle=angle, startAngle=0, endAngle=360, color=(0, 200, 0), thickness=1)

        # ellipse made by face height,width, face center(x,y)----end
        F1_feature = face_half_length
        Eye_line = face_width
        print('Eyeline', face_width)

        s1 = shape[8].ravel()
        x1 = s1[0]
        y1 = s1[1]

        # face_length = round(math.sqrt(math.pow(f_y - y1, 2) + math.pow(x1 - f_x, 2)), 0)

        print('face length', face_length)

        cv2.line(image, (x1, y1), (f_x, f_y), (0, 48, 125), 1)
        face_diff = face_length - face_width

        print('face length - face width', face_diff)

        # forehead_cordinates will be adding nose size + upper lip to 27 point
        # s1 = shape[28].ravel()
        # cv2.ellipse(image, (s1[0], s1[1]), (int(face_width/2), int(face_length/2)), 0, 0, 360, (0, 255, 255), 1)

        # nose length + till upper lip to calculate forehead

        # point 2 on forehead

        for i in range(16):
            s1 = shape[i].ravel()
            s2 = shape[i + 1].ravel()
        # cv2.line(image1, (s1[0], s1[1]), (s2[0], s2[1]), (170, 145, 128), 1)
        # cv2.line(image1, (s1[0], s1[1]), (s2[0], s2[1]), (102, 153, 255), 2)

        # for chin points----start-------------->

        # point=5
        # for points in range(5,12,1):
        # 	print(point, shape[points].ravel())
        # 	s1 = shape[points].ravel()
        # 	x1 = s1[0]
        # 	y1 = s1[1]
        # 	cv2.putText(image1, "{}".format(points), (x1 - 2, y1 - 2),
        # 				cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        #
        # 	point = point + 1

        # for chin points---- end -------------->

        temp = 0
        votes_oval = 0
        votes_square = 0
        votes_circle = 0
        dist3_0 = 0
        temp_0 = 0
        dist7_0 = 0

        cordinate_gap_x = 0
        cordinate_gap_y = 0
        range_4 = 0

        for i in range(7, -1, -1):

            s1 = shape[i].ravel()
            x1 = int(s1[0])
            y1 = int(s1[1])

            # print('cordinate of {} is {} and {}'.format(i,x1,y1))
            temp = temp + 2

            s2 = shape[i + temp].ravel()
            x2 = int(s2[0])
            y2 = int(s2[1])

            if (i == 0):
                i = 0
            # s3 =
            else:
                shape[i - 1].ravel()
                s3 = shape[0].ravel()
                x3 = int(s3[0])
                y3 = int(s3[1])
                cordinate_gap_x = (100 / x1) * (x1 - x3)
                cordinate_gap_y = (100 / y1) * (y1 - y3)
            # if(i==5):

            # print('cordinate of {} is {} and {}'.format(i-1, x3, y3))

            dist = round(math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)), 0)
            # print("Distance Between {} and {} is {}".format(i, i+temp, dist))

            # print("Distance Between {} and {} is {}".format(s1, s2, dist))

            # print('Decrease between {} and {} is x -> {} % and y -> {} %'
            #  	  .format(i, 0,round(cordinate_gap_x,0),round(cordinate_gap_y,0)))

            if (i == 7):

                dist7_0 = dist
                t_hold = 49
                if (dist > t_hold):
                    votes_square = votes_square + 1
                else:
                    votes_oval = votes_oval + 1
            if (i == 6):
                t_hold = 93
                if (dist > t_hold):
                    votes_square = votes_square + 1
                else:
                    votes_oval = votes_oval + 1
            if (i == 5):

                t_hold = 121
                if (dist > t_hold):
                    votes_square = votes_square + 1
                else:
                    votes_oval = votes_oval + 1
            if (i == 4):
                s8 = shape[8].ravel()
                x8 = int(s8[0])
                y8 = int(s8[1])

                range_4 = y8 - y1

                if (range_4 > 47):
                    votes_oval = votes_oval + 1
                else:
                    votes_square = votes_square + 1

                t_hold = 148
                if (dist >= t_hold):
                    votes_square = votes_square + 1
                else:
                    votes_oval = votes_oval + 1
            if (i == 3):
                dist3_0 = dist
            if (i == 0):
                temp_0 = dist
            if (votes_square > votes_oval):
                face_shape = 'Square'
            else:
                face_shape = 'Oval'

        dist3_0 = temp_0 - dist3_0
        dist7_0 = temp_0 - dist7_0

        # print('distance between 4-1 is {}'.format(dist3_0))
        # print('distance between 8-1 is {}'.format(dist7_0))
        # print('dist 1-4 + dist 1-8 is {}'.format(dist7_0+dist3_0))
        # print("range 4-8 is", range_4)

        if (face_shape is 'Square'):
            if (face_diff > 60 and range_4 > 45):
                face_shape = 'Square'
            else:
                face_shape = 'Circle'
        print('Prediction is', face_shape)
        print()
    # to draw line over eyebrows---------start---------------------

    # for i in range(17,21):
    # 	s1 = shape[i].ravel()
    # 	s2 = shape[i + 1].ravel()
    # 	cv2.line(image, (s1[0], s1[1]), (s2[0], s2[1]), (255, 255, 255), 2)
    # 	# cv2.line(image1, (s1[0], s1[1]), (s2[0], s2[1]), (255, 255, 255), 2)
    #
    #
    # for i in range(22,26):
    # 	s1 = shape[i].ravel()
    # 	s2 = shape[i + 1].ravel()
    # 	cv2.line(image, (s1[0], s1[1]), (s2[0], s2[1]), (255, 255, 255), 2)
    # 	# cv2.line(image1, (s1[0], s1[1]), (s2[0], s2[1]), (255, 255, 255), 2)
    #

    # to draw a line over eye-brows ----End---

    # show the output image with the face detections + facial landmarks
    # print('Prediction is',face_shape)

    cv2.putText(image, "Shape: {}".format(face_shape), (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 130, 20), 2)
    # cv2.imshow("Output", image)
    # cv2.waitKey(0)
    # cv2.imshow("Output", image1)
    # cv2.waitKey(0)

    if (face_shape != ""):
        response['Note'] = ''
        response['Status'] = True
        response['Shape'] = face_shape

    # cv2.imwrite('testing' +  '\\' +img_name, image)
    print(response)

    return response

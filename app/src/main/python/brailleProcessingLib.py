from collections import Counter  # counter
from skimage import io  # library to read images
import matplotlib.pyplot as plt  # library to show image to user
import numpy as np  # used to process image to arrays
import imutils  # basic image processing
import cv2  # advanced for image processing
import re  # regex


FILEPATH = "/storage/emulated/0/DCIM/Braille/test.jpg"
# test for alphabet translation / iter = 0 (test.jpg)
# test for gaussian blur on nemmeth example / iter >= 3 (test2.jpg)


# -----------------------FUNCTIONS------------------------- #


def run():
    return translate(letters)


def get_image(FILEPATH, iter=2, width=None):
    image = io.imread(FILEPATH)  # reads the url and opens the temporary image to user

    if width:
        image = imutils.resize(image, width)  # resized the image per the restricted width

    # image processing
    accumEdged = np.zeros(image.shape[:2], dtype="uint8")
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image to black and white
    blurred = cv2.GaussianBlur(grey, (5, 5), 0)  # blur to remove some of the noise
    edged = cv2.Canny(blurred, 75, 200)  # get edges(converts image to easy detectable dots)
    cv2.bitwise_or(accumEdged, edged)
    ctrs = imutils.grab_contours(cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))  # get contours(increases accuracy)

    # ensure that at least one contour was found to know an image can be processed
    if len(ctrs) > 0:  # sort the contours according to their size in descending order
        ctrs = sorted(ctrs, key=cv2.contourArea, reverse=True)

        for c in ctrs:  # loop over the sorted contours
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # approximate the contour

            # if our approximated contour has four points, then we can assume we have found the image
            if len(approx) == 4:
                break
    paper = image.copy()  # creates a copy of the processed image

    # apply Otsu's threshold method to binary the image
    thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)

    # erode and dilate to remove some of the unnecessary detail
    thresh = cv2.erode(thresh, kernel, iterations=iter)
    thresh = cv2.dilate(thresh, kernel, iterations=iter)

    # find contours in the threshold's image
    ctrs = imutils.grab_contours(
        cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))

    return image, ctrs, paper, grey, edged, thresh


def get_diameter():  # shows the area of interest for the computer
    boundingBoxes = [list(cv2.boundingRect(c)) for c in ctrs]
    c = Counter([i[2] for i in boundingBoxes])
    mode = c.most_common(1)[0][0]
    if mode > 1:
        diam = mode
    else:
        diam = c.most_common(2)[1][0]
    return diam


def get_circles():  # shows the area of interest for the computer
    questionCtrs = []
    for c in ctrs:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if diam * 0.8 <= w <= diam * 1.2 and 0.8 <= ar <= 1.2:  # region should be sufficiently wide, tall, and have an aspect ratio approximately equal to 1
            questionCtrs.append(c)
    return questionCtrs


def sort_contours(ctrs):
    BB = [list(cv2.boundingRect(c)) for c in ctrs]
    tol = 0.7 * diam  # choose tolerance for x, y coordinates of the bounding boxes to be binned together

    def sort(i):  # change x and y coordinates of bounding boxes to their corresponding bins
        S = sorted(BB, key=lambda x: x[i])
        s = [b[i] for b in S]
        m = s[0]

        for b in S:
            if m - tol < b[i] < m or m < b[i] < m + tol:
                b[i] = m
            elif b[i] > m + diam:
                for e in s[s.index(m):]:
                    if e > m + diam:
                        m = e
                        break
        return sorted(set(s))

    # lists of of x and y coordinates
    xs = sort(0)
    ys = sort(1)

    (ctrs, BB) = zip(*sorted(zip(ctrs, BB), key=lambda b: b[1][1] * len(image) + b[1][0]))
    # return the list of sorted contours and bounding boxes
    return ctrs, BB, xs, ys


def draw_contours(questionCtrs):
    color = (0, 255, 0)
    i = 0
    for q in range(len(questionCtrs)):
        cv2.drawContours(paper, questionCtrs[q], -1, color, 3)
        cv2.putText(paper, str(i), (boundingBoxes[q][0] + boundingBoxes[q][2] // 2,
                                    boundingBoxes[q][1] + boundingBoxes[q][3] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        i += 1


def get_spacing():
    def spacing(x):
        space = []
        coor = [b[x] for b in boundingBoxes]
        for i in range(len(coor) - 1):
            c = coor[i + 1] - coor[i]
            if c > diam // 2: space.append(c)
        return sorted(list(set(space)))

    spacingX = spacing(0)
    spacingY = spacing(1)

    # smallest x-separation (between two adjacent dots in a letter)
    min(spacingX)

    d1 = spacingX[0]
    d2 = 0
    d3 = 0

    for x in spacingX:
        if d2 == 0 and x > d1 * 1.3:
            d2 = x
        if d2 > 0 and x > d2 * 1.3:
            d3 = x
            break

    linesV = []
    prev = 0  # outside

    linesV.append(min(xs) - (d2 - diam) / 2)

    for i in range(1, len(xs)):
        diff = xs[i] - xs[i - 1]
        if i == 1 and d2 * 0.9 < diff:
            linesV.append(min(xs) - d2 - diam / 2)
            prev = 1
        if d1 * 0.8 < diff < d1 * 1.2:
            linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
            prev = 1
        elif d2 * 0.8 < diff < d2 * 1.1:
            linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
            prev = 0
        elif d3 * 0.9 < diff < d3 * 1.1:
            if prev == 1:
                linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
                linesV.append(xs[i - 1] + d2 + diam + (d1 - diam) / 2)
            else:
                linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
                linesV.append(xs[i - 1] + d1 + diam + (d2 - diam) / 2)
        elif d3 * 1.1 < diff:
            if prev == 1:
                linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
                linesV.append(xs[i - 1] + d2 + diam + (d1 - diam) / 2)
                linesV.append(xs[i - 1] + d3 + diam + (d2 - diam) / 2)
                prev = 0
            else:
                linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
                linesV.append(xs[i - 1] + d1 + diam + (d2 - diam) / 2)
                linesV.append(xs[i - 1] + d1 + d2 + diam + (d1 - diam) / 2)
                linesV.append(xs[i - 1] + d1 + d3 + diam + (d2 - diam) / 2)
                prev = 1

    linesV.append(max(xs) + diam * 1.5)
    if len(linesV) % 2 == 0:
        linesV.append(max(xs) + d2 + diam)

    return linesV, d1, d2, d3, spacingX, spacingY


def get_letters(showID=False):
    minYD = 0
    Bxs = list(boundingBoxes)
    Bxs.append((100000, 0))

    dots = [[]]
    for y in sorted(list(set(spacingY))):
        if y > 1.3 * diam:
            minYD = y * 1.5
            break

    # get lines of dots
    for b in range(len(Bxs) - 1):
        if Bxs[b][0] < Bxs[b + 1][0]:
            if showID:
                dots[-1].append((b, Bxs[b][0:2]))
            else:
                dots[-1].append(Bxs[b][0])
        else:
            if abs(Bxs[b + 1][1] - Bxs[b][1]) < minYD:
                if showID:
                    dots[-1].append((b, Bxs[b][0:2]))
                else:
                    dots[-1].append(Bxs[b][0])
                dots.append([])
            else:
                if showID:
                    dots[-1].append((b, Bxs[b][0:2]))
                else:
                    dots[-1].append(Bxs[b][0])
                dots.append([])
                if len(dots) % 3 == 0 and not dots[-1]:
                    dots.append([])

    letters = []

    for r in range(len(dots)):
        if not dots[r]:
            letters.append([0 for _ in range(len(linesV) - 1)])
            continue

        else:
            letters.append([])
            c = 0
            i = 0
            while i < len(linesV) - 1:
                if c < len(dots[r]):
                    if linesV[i] < dots[r][c] < linesV[i + 1]:
                        letters[-1].append(1)
                        c += 1
                    else:
                        letters[-1].append(0)
                else:
                    letters[-1].append(0)
                i += 1

    for x in range(len(letters)):
        if x % 3 == 0: print()
        print(letters[x])
    print()

    return letters


def translate(letters):
    alpha = {'a': '1', 'b': '13', 'c': '12', 'd': '124', 'e': '14',
             'f': '123', 'g': '1234', 'h': '134', 'i': '23', 'j': '234',
             'k': '15', 'l': '135', 'm': '125', 'n': '1245', 'o': '145',
             'p': '1235', 'q': '12345', 'r': '1345', 's': '235', 't': '2345',
             'u': '156', 'v': '1356', 'w': '2346', 'x': '1256', 'y': '12456',
             'z': '1456',
             # special characters
             '#': '2456', ',': '3', '.': '346',
             '\"': '356', '^': '26', ':': '34', '\'': '5'}

    nums = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0'}  # 2x2 braille letters

    braille = {v: k for k, v in alpha.items()}
    letters = np.array([np.array(x) for x in letters])
    ans = ''

    # printFig()              #test for gaussian blur (test2.jpg)

    for r in range(0, len(letters), 3):
        for c in range(0, len(letters[0]), 2):
            f = letters[r:r + 3, c:c + 2].flatten()
            f = ''.join([str(i + 1) for i, d in enumerate(f) if d == 1])
            if f == '6': f = '26'
            if not f:
                if ans[-1] != ' ': ans += ' '
            elif f in braille.keys():
                ans += braille[f]
            else:
                ans += '?'
        if ans[-1] != ' ': ans += ' '

    def replace_nums(m):  # replace numbers
        return nums.get(m.group('key'), m.group(0))

    ans = re.sub('#(?P<key>[a-zA-Z])', replace_nums, ans)

    def capitalize(m):  # capitalize
        return m.group(0).upper()[1]

    ans = re.sub('\^(?P<key>[a-zA-Z])', capitalize, ans)

    return ans


def printFig():  # shows the image processing steps
    fig, axarr = plt.subplots(4, 2)
    fig.suptitle('Image Processing')
    axarr[0, 0].imshow(image)  # original image
    axarr[0, 0].set_title("Original Image")
    axarr[0, 0].axis('off')

    axarr[0, 1].imshow(gray)  # greyscale image
    axarr[0, 1].set_title("Greyscale")
    axarr[0, 1].axis('off')

    axarr[1, 0].imshow(edged)  # checks for areas of interest
    axarr[1, 0].set_title("Edging")
    axarr[1, 0].axis('off')

    axarr[1, 1].set_title("Contours")  # shows the contours of the alignments
    axarr[1, 1].imshow(image)
    for x in linesV:
        axarr[1, 1].axvline(x)
    axarr[1, 1].axis('off')

    axarr[2, 0].imshow(paper)  # counts the dots in an array
    axarr[2, 0].set_title("Sorting Array")
    axarr[2, 0].axis('off')

    axarr[2, 1].imshow(thresh)  # adds blur to remove unnecessary noise
    axarr[2, 1].set_title("Gaussian Blurring")
    axarr[2, 1].axis('off')
    plt.show()

    axarr[3, 0].imshow(image)  # for comparison
    axarr[3, 0].set_title("Original Image")
    axarr[3, 0].axis('off')
    plt.show()

    io.imshow(thresh)
    plt.title('Final Image')
    plt.axis('off')
    plt.show()


# -----------------------MAIN------------------------- #


image, ctrs, paper, gray, edged, thresh = get_image(FILEPATH, iter=0, width=1500)  # processes image

diam = get_diameter()  # shows the area of interest for the computer
dotCtrs = get_circles()

questionCtrs, boundingBoxes, xs, ys = sort_contours(dotCtrs)  # counts dot array
draw_contours(questionCtrs)  # contours image

linesV, d1, d2, d3, spacingX, spacingY = get_spacing()  # gets spacing lines
letters = get_letters()  # translates braille

print(translate(letters))  # print the translated braille
printFig()  # prints the image processing steps

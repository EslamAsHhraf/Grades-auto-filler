<div align="center">
<a href="" rel="noopener">
  
  ![Grade Autofiller](https://t3.ftcdn.net/jpg/00/33/15/36/240_F_33153607_eYe0x5YRdY2BQYcco5eDkfP9SWABvqtQ.jpg)
</div>

<h2 align="center">Grade Autofiller</h2>

## Table of Contents

  * [About](#about)
  * [Bubble Sheet](#bubble-sheet)
  * [Grades Sheet](#grade-sheet)
  * [Paper Extraction Explanation](#warping)
  * [Digits Detection Explanation](#algorithm-explanation)
  * [Installation](#installation)
  * [Running](#running)
  * [Contributors](#contributors)


## <a name="about"></a> About


> **Grade Autofiller** is an assistant to TAs and Professors in our department (Computer Department). It should provide an easy way to fill the grades electronically, and it should be able to correct MCQ bubble sheet exams automatically.


<div align="center">

![image](./Bubble%20Sheet%20Module/readme%20imgs/flowchart.png)

</div>

# <a name="bubble-sheet"></a> Bubble Sheet

## How the bubble sheet corrector works
> List of steps we take to process the input sheet and get our results


#### 1. Extract the paper from the image.

<table>
<tr>
<td>
<img src="./Bubble%20Sheet%20Module/readme%20imgs/withID.jpg" height=500>
</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/paper.jpg" height=500>

</td>
</tr>
</table>


#### 2. Convert the RGB image to gray scale image

<table>
<tr>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/gray.jpg" height=500>

</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0.jpeg" height=500>

</td>
</tr>
</table>


#### 3. Convert the image to binary image using local thresholding
<table>
<tr>
<td>
<img src="./Bubble%20Sheet%20Module/readme%20imgs/thres.jpg" height=500>
</td>
<td>
<img src="./Bubble%20Sheet%20Module/readme%20imgs/thres.jpeg" height=500>
</td>
</tr>
</table>

#### 4. Extract the ID box from the paper and erase it
<table>
<tr>
<td>
<img src="./Bubble%20Sheet%20Module/readme%20imgs/id%20box.jpg" height=200>

</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/paperwithoutbox.jpg" height=500>

</td>
</tr>
</table>

#### 5. Erode the image to get rid of false chosen bubbles
<table>
<tr>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0eroded.jpg" height=500>
</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0eroded.jpeg" height=500>

</td>
</tr>
</table>

#### 6. Detect the external contours an draw them on the original image

<table>
<tr>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0exconts.jpg" height=500>

</td>
<td>
<img src="./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0exconts.jpeg" height=500>

</td>
</tr>
</table>

#### 7. Calculate the bounding rectangle of the contours and get its coordinates, width and height and calculate aspect ratio

#### 8. Calculate the contour perimeter

#### 9. Approximate each contour to polygon
#### 10. Calculate each contour area

#### 11. Filter the contours so if the aspect ratio ∈ [0.8,1.2], the number of contour vertices is greater than 4, the contour area is greater than 30 (threshold to ignore small circles or contours) and the contour is a closed one then it will be considered as a bubble

#### 12. Collect all contours areas in array and calculate the average area (the mean of areas should be very close to the bubbles area because the most frequent contours are the bubbles contours).

#### 13. Another filter to the output contours that resulted from the first filter by check if the area of each contour is within 30% error with the average contour area then bubbles contours are only residual contours
<table>
<tr>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/bubbles.jpg" height=500>

</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/bubbles.jpeg" height=500>

</td>
</tr>
</table>

#### 14. Sort the contours from top to bottom

#### 15. Calculate the number of choices and the number of question in each row by using x and y coordinates of each bubble (bubbles belong to the same question are colored with the same color).

<table>
<tr>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/withIDquestions.jpg" height=500>

</td>
<td>

<img src="./Bubble%20Sheet%20Module/readme%20imgs/withIDquestions.jpeg" height=500>

</td>
</tr>
</table>

#### 16. Iterate over each row and sort the contours from left to right.

#### 17. Iterate over each question and calculate the number of pixels in each bubble that equal to one.

#### 18. Check if the student select more than one choice or no choice the answer will be X but if the student select only one choice so the answer will be the character of the choice (A, B, C, etc.).

#### 19. Calculate the number of rows and map the result array to the real dat

<hr>

# <a name="grade-sheet"></a> Grades Sheet

## How the Grades Sheet is processed
> List of steps taken to process the Grades Sheet

#### 1. Paper Extraction and Image Warping

#### 2. Table and Cells Detection

#### 3. ID Detection
> 2 Methods were used: &emsp; 
> * OCR
> * Classifiers

#### 4. Handwritten Digits Detection

#### 5. Signs Detection
> 6 different signs

# <a name="warping"></a> Warping & Paper Extraction

#### 1. Applied Canny Edge Detector followed by Dilation to connect broken edges
  
#### 2. Extracted Contours, then extracted the largest based on area (the paper contour)
  
#### 3. Measured width and height of the contour (using the 4 corners)
 
#### 4. Calculated coordinates for the new points (warped), and transformed the original points to these coordinates.
  
# <a name="algorithm-explanation"></a> Digits Detection
> Data Acquisition and Model Training for Digits Detection (Digital and Handwritten)

* [Used Dataset](https://www.kaggle.com/competitions/digit-recognizer)

#### The main idea is to train different models then use a polling system to collectively increase the accuracy of the system — beyond the accuracy of each on their own.

#### Not much Pre-Processing was needed for the handwritten digits, just a noise reduction filter.





## <a name="installation"></a> Installation

1. **_Clone the repository_**

```sh
$ git clone https://github.com/AdhamAliAbdelAal/Grades-autofiller.git
```
2. **_Navigate to repository directory_**
```sh
$ cd '.\Bubble Sheet Module\'
```


## <a name="running"></a> Running

1. **_Put you input files inside testCases folder_**
2. **_Your answers will be found in Results folder_**

3. **_Running_**
```sh
python main.py
```

## <a name="contributors"></a> Contributing

> Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.


#### Contributors
<table>
  <tr>
    <td align="center"><a href="https://github.com/AdhamAliAbdelAal"><img src="https://avatars.githubusercontent.com/u/83884426?v=4" width="150px;" alt=""/><br /><sub><b>Adham Ali</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/MennaTalhHossamAlden"><img src="https://avatars.githubusercontent.com/u/76497207?v=4" width="150px;" alt=""/><br /><sub><b>Menatalh Hossamalden</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/EslamAsHhraf"><img src="https://avatars.githubusercontent.com/u/71986226?v=4" width="150px;" alt=""/><br /><sub><b>Eslam Ashraf</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/MohamedWw"><img src="https://avatars.githubusercontent.com/u/64079821?v=4" width="150px;" alt=""/><br /><sub><b>Mohamed Walid</b></sub></a><br /></td>
     
  </tr>
 </table>

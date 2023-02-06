<div align= >

# <img align=center width=75px height=75px src="https://media4.giphy.com/media/S3vkOnyeiqqUjGOc9S/giphy.webp?cid=ecf05e47bcr7g2gaapy8yofnt3etgvfg5ync8azjyq09fqz6&rid=giphy.webp&ct=s"> Grade Autofiller


</div>
<div align="center">
   <img align="center"  width="525px" src="https://res.cloudinary.com/teepublic/image/private/s--Zi78NcGO--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1630566782/production/designs/24055931_0.jpg" alt="logo">


   
</div>
<br>

## <img align= center width=50px height=50px src="https://thumbs.gfycat.com/HeftyDescriptiveChimneyswift-size_restricted.gif"> Table of Contents

- <a href ="#about"> 📙 About</a>
- <a href ="#started"> 💻 Get Started</a>
- <a href ="#modules"> 🌎 Modules</a>
  -  <a href="#grade-sheet">  Grade Sheet </a>
  -  <a href="#bubble-sheet">  Bubble Sheet </a>
- <a href ="#contributors"> ✨ Contributors</a>
- <a href ="#license"> 🔒 License</a>
<hr style="background-color: #4b4c60"></hr>


## <a id="about"></a> About


> **Grade Autofiller** is an assistant to TAs and Professors in our department (Computer Department). It should provide an easy way to fill the grades electronically, and it should be able to correct MCQ bubble sheet exams automatically.


<div align="center">

![image](./readme%20imgs/flowchart.png)

</div>



<hr style="background-color: #4b4c60"></hr>

## <img  align= center width=50px height=50px src="https://c.tenor.com/HgX89Yku5V4AAAAi/to-the-moon.gif"> Get Started <a id = "started"></a>

<ol>
<li>Clone the repository

<br>

```sh
$ git clone https://github.com/AdhamAliAbdelAal/Grades-autofiller.git
```

</li>
<li>

You can use and choose module from this file

```sh
$ cd './Code/GUI.py'
```
</li>


</ol>
<hr style="background-color: #4b4c60"></hr>

# <a id="bubble-sheet"></a> Bubble Sheet

## How the bubble sheet corrector works
> List of steps we take to process the input sheet and get our results


#### 1. Extract the paper from the image.

<table>
<tr>
<td>
<img src="./readme%20imgs/withID.jpg" height=250>
</td>
<td>

<img src="./readme%20imgs/paper.jpg" height=250>

</td>
</tr>
</table>


#### 2. Convert the RGB image to gray scale image

<table>
<tr>
<td>

<img src="./readme%20imgs/gray.jpg" height=250>

</td>
<td>

<img src="./readme%20imgs/CameraFour0.jpeg" height=250>

</td>
</tr>
</table>


#### 3. Convert the image to binary image using local thresholding
<table>
<tr>
<td>
<img src="./readme%20imgs/thres.jpg" height=250>
</td>
<td>
<img src="./readme%20imgs/thres.jpeg" height=250>
</td>
</tr>
</table>

#### 4. Extract the ID box from the paper and erase it
<table>
<tr>
<td>
<img src="./readme%20imgs/id%20box.jpg" height=100>

</td>
<td>

<img src="./readme%20imgs/paperwithoutbox.jpg" height=250>

</td>
</tr>
</table>

#### 5. Erode the image to get rid of false chosen bubbles
<table>
<tr>
<td>

<img src="./readme%20imgs/CameraFour0eroded.jpg" height=250>
</td>
<td>

<img src="./readme%20imgs/CameraFour0eroded.jpeg" height=250>

</td>
</tr>
</table>

#### 6. Detect the external contours an draw them on the original image

<table>
<tr>
<td>

<img src="./readme%20imgs/CameraFour0exconts.jpg" height=250>

</td>
<td>
<img src="./readme%20imgs/CameraFour0exconts.jpeg" height=250>

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

<img src="./readme%20imgs/bubbles.jpg" height=250>

</td>
<td>

<img src="./readme%20imgs/bubbles.jpeg" height=250>

</td>
</tr>
</table>

#### 14. Sort the contours from top to bottom

#### 15. Calculate the number of choices and the number of question in each row by using x and y coordinates of each bubble (bubbles belong to the same question are colored with the same color).

<table>
<tr>
<td>

<img src="./readme%20imgs/withIDquestions.jpg" height=250>

</td>
<td>

<img src="./readme%20imgs/withIDquestions.jpeg" height=250>

</td>
</tr>
</table>

#### 16. Iterate over each row and sort the contours from left to right.

#### 17. Iterate over each question and calculate the number of pixels in each bubble that equal to one.

#### 18. Check if the student select more than one choice or no choice the answer will be X but if the student select only one choice so the answer will be the character of the choice (A, B, C, etc.).

#### 19. Calculate the number of rows and map the result array to the real dat
#### 20. Output will be in excel sheet like this
>  excel sheet name "result Grades sheet"

<table>
<tr>
<td>

<img src="./readme%20imgs/bubblesheet.png" width=150>

</td>
</tr>
</table>

<hr style="background-color: #4b4c60"></hr>

# <a id="grade-sheet"></a> Grades Sheet

## How the Grades Sheet is processed
> List of steps taken to process the Grades Sheet

#### 1. Paper Extraction and Image Warping

<table>
<tr>
<td>

<img src="./readme%20imgs/testcase.jpg" height=250>

</td>
<td>

<img src="./readme%20imgs/warping.jpg" height=200>

</td>
</tr>
</table>

#### 2. Table and Cells Detection
<table>
<tr>
<th>
Horizontal Lines Detect
</th>
<th>
Vertical Lines Detect
</th>
<th>
Intersection Lines Detect
</th>
</tr>
<tr>
<td>

<img src="./readme%20imgs/horizontal_lines_img.jpg" height=200>

</td>
<td>

<img src="./readme%20imgs/verticle_lines_img.jpg" height=200>

</td>
<td>

<img src="./readme%20imgs/img_final_threshold.jpg" height=200>

</td>
</tr>
</table>

#### 3. ID Detection
> 2 Methods were used: &emsp; 
> * OCR
> * Classifiers

<table>
<tr>
<td>

<img src="./readme%20imgs/ID.jpg" width=250>

</td>
</tr>
</table>

#### 4. Handwritten Digits Detection

<table>
<tr>
<td>

<img src="./readme%20imgs/five.jpg" width=250>

</td>
</tr>
</table>

#### 5. Signs Detection
> 6 different signs

<table height="250">
<tr>
<th>
Sign
</th>
<th>
Square
</th>
<th>
Question Mark
</th>
<th>
Check Mark
</th>
<th>
Horizontal Lines
</th>
<th>
Vertical Lines
</th>
<th>
Empty
</th>
</tr>
<tr>
<th>
Image
</th>
<td >

<img src="./readme%20imgs/square.jpg" >

</td>
<td >

<img src="./readme%20imgs/question.jpg" >

</td>
<td>

<img src="./readme%20imgs/check.jpg" >

</td>
<td >

<img src="./readme%20imgs/horizontal-lines.jpg">

</td>
<td >

<img src="./readme%20imgs/vertical-lines.jpg">

</td>
<td>

<img src="./readme%20imgs/empty.jpg">

</td>
</tr>

<tr>
<th>
Output
</th>
<td>
0
</td>
<td>
empty cell with a red background color
</td>
<td>
5
</td>
<td>
 (5 - i) where i is the number of lines
</td>
<td>
 number of lines
</td>
<td>
0
</td>
</tr>
<tr>
</table>


#### 6. Output will be in excel sheet like this
>  excel sheet name "result Grades sheet"

<table>
<tr>
<td>

<img src="./readme%20imgs/excellsheet.png" width=250>

</td>
</tr>
</table>

## <a name="warping"></a> Warping & Paper Extraction

#### 1. Applied Canny Edge Detector followed by Dilation to connect broken edges
  
#### 2. Extracted Contours, then extracted the largest based on area (the paper contour)
  
#### 3. Measured width and height of the contour (using the 4 corners)
 
#### 4. Calculated coordinates for the new points (warped), and transformed the original points to these coordinates.
  
## <a name="algorithm-explanation"></a> Digits Detection
> Data Acquisition and Model Training for Digits Detection (Digital and Handwritten)

* [Used Dataset](https://www.kaggle.com/competitions/digit-recognizer)

#### The main idea is to train different models then use a polling system to collectively increase the accuracy of the system — beyond the accuracy of each on their own.

### Single Digits Detection

#### 1. Not much Pre-Processing was needed for the single handwritten digits, just a noise reduction filter.

#### 2. Computed HoG of each digit picture and passed to the classifiers to determine the output.

### ID Detection

#### 1. Extracted Contours [For Digits], Then Filtered out very small contours [Not Digits]
> Now, we have contours containing single digits or a group of connected digits.

#### 2. Get the Average Width of all contours

#### 3. Divide the each **contour width** by the **average width** [integer Division]; to know how many digits are in each picture

#### 4. If the quotient of the division is less than a certain threshold, then it contains a single digit. Otherwise, divide the contour into a number of smaller contours [each containing a single digit] according to the quotient.

#### 5. Computed HoG of each digit picture and passed to the classifiers to determine the output.




## <a id="contributors"></a> Contributing

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

## 🔒 License <a id ="license"></a>

> **Note**: This software is licensed under MIT License, See [License](https://github.com/AdhamAliAbdelAal/Grades-autofiller/blob/master/LICENSE) for more information ©Mohamed Walid.
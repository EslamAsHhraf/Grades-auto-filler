<div align="center">
<a href="" rel="noopener">
  
  ![Grade Autofiller](https://t3.ftcdn.net/jpg/00/33/15/36/240_F_33153607_eYe0x5YRdY2BQYcco5eDkfP9SWABvqtQ.jpg)
</div>

<h2 align="center">Grade Autofiller</h2>

## About
> **Grade Autofiller** is an assistant to TAs and Professors in our department (Computer Department). It should provide an easy way to fill the grades electronically, and it should be able to correct MCQ bubble sheet exams automatically.


<div align="center">

![image](./Bubble%20Sheet%20Module/readme%20imgs/flowchart.png)

</div>

## How the bubble sheet corrector works
> List of steps we take to process the input sheet and get our results


#### 1. Extract the paper from the image.

<table>
<tr>
<td>

![1  original](./Bubble%20Sheet%20Module/readme%20imgs/withID.jpg)

</td>
<td>

![1  paper](./Bubble%20Sheet%20Module/readme%20imgs/paper.jpg)

</td>
</tr>
</table>


#### 2. Convert the RGB image to gray scale image

<table>
<tr>
<td>

![2  gray scale image](./Bubble%20Sheet%20Module/readme%20imgs/gray.jpg)

</td>
<td>

![1  thres2](./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0.jpeg)

</td>
</tr>
</table>


#### 3. Convert the image to binary image using local thresholding

<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![1  thres1](./Bubble%20Sheet%20Module/readme%20imgs/thres.jpg)

![1  thres2](./Bubble%20Sheet%20Module/readme%20imgs/thres.jpeg)

</div>

#### 4. Extract the ID box from the paper and erase it
<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![ID Box](./Bubble%20Sheet%20Module/readme%20imgs/id%20box.jpg)

![Paper](./Bubble%20Sheet%20Module/readme%20imgs/paperwithoutbox.jpg)

</div>

#### 5. Erode the image to get rid of false chosen bubbles
<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![1](./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0eroded.jpg)

![2](./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0eroded.jpeg)

</div>

#### 6. Detect the external contours an draw them on the original image
<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![1](./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0exconts.jpg)

![1](./Bubble%20Sheet%20Module/readme%20imgs/CameraFour0exconts.jpeg)

</div>

#### 7. Calculate the bounding rectangle of the contours and get its coordinates, width and height and calculate aspect ratio

#### 8. Calculate the contour perimeter

#### 9. Approximate each contour to polygon
#### 10. Calculate each contour area

#### 11. Filter the contours so if the aspect ratio ∈ [0.8,1.2], the number of contour vertices is greater than 4, the contour area is greater than 30 (threshold to ignore small circles or contours) and the contour is a closed one then it will be considered as a bubble

#### 12. Collect all contours areas in array and calculate the average area (the mean of areas should be very close to the bubbles area because the most frequent contours are the bubbles contours).

#### 13. Another filter to the output contours that resulted from the first filter by check if the area of each contour is within 30% error with the average contour area then bubbles contours are only residual contours
<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![1](./Bubble%20Sheet%20Module/readme%20imgs/bubbles.jpg)

![1](./Bubble%20Sheet%20Module/readme%20imgs/bubbles.jpeg)

</div>

#### 14. Sort the contours from top to bottom

#### 15. Calculate the number of choices and the number of question in each row by using x and y coordinates of each bubble (bubbles belong to the same question are colored with the same color).
<div align="center" style="display:flex;flex-wrap:nowrap; justify-content:space-between; align-items:center; gap:10px">

![1](./Bubble%20Sheet%20Module/readme%20imgs/withIDquestions.jpg)

![1](./Bubble%20Sheet%20Module/readme%20imgs/withIDquestions.jpeg)

</div>

#### 16. Iterate over each row and sort the contours from left to right.

#### 17. Iterate over each question and calculate the number of pixels in each bubble that equal to one.

#### 18. Check if the student select more than one choice or no choice the answer will be X but if the student select only one choice so the answer will be the character of the choice (A, B, C, etc.).

#### 19. Calculate the number of rows and map the result array to the real dat


#### Installation

1. **_Clone the repository_**

```sh
$ git clone https://github.com/AdhamAliAbdelAal/Grades-autofiller.git
```
2. **_Navigate to repository directory_**
```sh
$ cd '.\Bubble Sheet Module\'
```


#### Running

1. **_Put you input files inside testCases folder_**
2. **_Your answers will be found in Results folder_**

3. **_Running_**
```sh
python main.py
```

## Contributing

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

#### Licence
[MIT Licence](https://github.com/AbdallahHemdan/Orchestra/blob/master/LICENSE)
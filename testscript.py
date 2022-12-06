counter=0
for (row,i) in enumerate(np.arange(0,len(question_cnts),number_of_columns*number_of_choices)):

    curr_row_cnts,_=imcnts.sort_contours(question_cnts[i:i+number_of_columns*number_of_choices])

    for (qs,k) in enumerate(np.arange(0,len(curr_row_cnts),number_of_choices)):

        curr_ques_cnts=curr_row_cnts[k:k+number_of_choices]
        color1=colors[qs%len(colors)]
        cv2.drawContours(paper,curr_ques_cnts,-1,color1, 1)
        bubbled=None
        for (j,c) in enumerate(curr_ques_cnts):
            mask = np.zeros(thresholded.shape, dtype="uint8")
            #negative one at the last arguement to fill the contours
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask= cv2.bitwise_and(thresholded, mask)
            total= cv2.countNonZero(mask)

            if bubbled is None or total >bubbled[0]:
                bubbled= (total, j)
            color= (0, 0, 255)
    print(f'qestion#{qs+1}: {bubbled[1]}')
    counter+=1
print(counter)
counter=0
cv2.imshow('paper', paper)
cv2.waitKey(0)
paper= four_point_transform(image, paper_contour.reshape(4, 2)) 

{chr(bubbled[1]+ord('A'))}
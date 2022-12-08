xs_set=set()
for cnt in question_cnts:
    (x,y,w,h)=cv2.boundingRect(cnt)
    if(all([ x-i not in xs_set and x+i not in xs_set for i in np.arange(0,5)])):
        xs_set.add(x)
number_of_bubbles=len(xs_set)
xs=np.array(list(sorted(xs_set)))
dist=np.append(xs[1:],xs[-1])-xs
distance_set=set()
for diff in dist:
    if(all([ diff-i not in distance_set and diff+i not in distance_set for i in np.arange(0,5)])):
        distance_set.add(diff)
number_of_changes=len(distance_set)
number_of_columns=(number_of_changes-1)//2+1
number_of_choices=number_of_bubbles//number_of_columns

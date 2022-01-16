f = open('../html/1/input.js', 'w')

f.write('var vidar = [')

for i in range(3):
    f.write("['./top1/{}.mp4', ".format(str(i)))
    f.write("'./top2/{}.mp4', ".format(str(i)))
    f.write("'./top3/{}.mp4'],\n".format(str(i)))
 
f.write(']\n')


f.write('var imgar = [')

for i in range(3):
    f.write("['./top1/{}.jpg', ".format(str(0)))
    f.write("'./top2/{}.jpg', ".format(str(0)))
    f.write("'./top3/{}.jpg'],\n".format(str(0)))
 

f.write(']\n')

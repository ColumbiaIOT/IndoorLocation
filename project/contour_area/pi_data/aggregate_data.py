with open('data.csv','w') as outfile:
    outfile.write('distance(ft),pixels\n')
    for i in range(4,16):
        with open('{}ft.txt'.format(str(i)),'r') as infile:
            outfile.write("{},{}".format(str(i),infile.readline()))
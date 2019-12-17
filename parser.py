import os,re,sys

def cleaning_data(dir):
    x=[]
    for filename in os.listdir(dir):
        if filename.endswith('.xml'):
            if not filename.endswith('.xml'):
                continue
            print("cleaning", filename)
            with open(os.path.join(dir, filename),'r') as f:

                #this regex for cleaning the files from XML entities that resulted from encoding the file  and XML tags
                # cleanfile=re.sub('<Title>(.*?)</Title>|<[^>]+>|(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())
                cleanfile=re.sub('(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())
                with open(os.path.join(dir, filename),'w') as r:
                    r.write(cleanfile)
                titles = re.findall("<Title>(.*?)</Title>", cleanfile)
                x.append(titles)
                flatList = [item for elem in x for item in elem]
                fulxlStr = '\n'.join(flatList)
                with open('newfile.txt', 'w') as t:
                    t.write(fulxlStr)

                # with open('newfile.txt','r') as t ,open('random_query.txt','w')as n:
                #     line = t.readline()
                #     itr = 1
                #     while line:
                #         n.write( str(str(itr) + '  ' + line))
                #         line = t.readline()
                #         itr+=1

                cleanfile2=re.sub("<Title>(.*?)</Title>|<[^>]+>|^a-zA-Z.\d\s","",cleanfile)
                with open(os.path.join(dir, filename),'w') as r:
                    r.write(cleanfile2)
                # clean2=re.sub('[^a-zA-Z.\d\s]',"",open('newfile.txt').read())
                # with open('newfile.txt','w')as final:
                #     final.write(clean2)
        else:print('sorry this directory does not have any xml files')
    print('done...')


if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) < 2:
        print(dir.__doc__)
        sys.exit(1)
    print('cleaning data...')
    cleaning_data()




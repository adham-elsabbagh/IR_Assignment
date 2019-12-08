import os,re,sys

def cleaning_data():
    for filename in os.listdir(dir):
        if filename.endswith('.xml'):
            if not filename.endswith('.xml'):
                continue
            print("cleaning", filename)
            with open(os.path.join(dir, filename),'r') as f:
                #this regex for cleaning the files from XML entities that resulted from encoding the file  and XML tags
                # cleanfile=re.sub('<[^>]+>|(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())
                cleanfile=re.sub('(lt;)|(gt;)|/p[^>]|p[^>]|/code[^>]|^[ \t]+|&(#[xX][0-9a-fA-F]+|#\d+|[lg]t|amp|apos|quot);', "", f.read())
                with open(os.path.join(dir, filename),'w') as r:
                    content = r.write(cleanfile)
        else:print('sorry this directory does not have any xml files')
    print('done...')


if __name__ == '__main__':
    dir = sys.argv[1]
    if len(sys.argv) < 2:
        print(dir.__doc__)
        sys.exit(1)
    print('cleaning data...')
    cleaning_data()




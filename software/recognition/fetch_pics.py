import os, sys

def fetch(path, dest):
    dirs = os.listdir(path)
    count = 0
    lst = ["/0_100.jpg ", "/1_100.jpg ", "/150_100.jpg ",  "/178_100.jpg ", "/r_28_100.jpg ", "/r_200_100.jpg " 
    "/r_218_100.jpg ", "/r_268_100.jpg " , "/73_100.jpg ", "/96_100.jpg "  , "/190_100.jpg ", "/238_100.jpg " 
    "/r_99_100.jpg " , "/r_125_100.jpg "]
    for item in dirs:
        item = '"' + item + '"'
        for name in lst:
            os.system("cp " + path + "/" + item+ name + dest+ "/" + str(count) + ".jpg")
            count +=1

def main():
    path = sys.argv[1]
    dest = sys.argv[2]
    fetch(path, dest)

if __name__ == "__main__":
    # execute only if run as a script
    main()
import uuid,os

def random_filename(filename):
    ext=os.path.splitext(filename)[1]
    new_filename=uuid.uuid4().hex+ext
    return new_filename

def comma_replace(text):
    return text.replace("，",",")

# if __name__=="__main__":
#     print(random_filename("test.s"))

def deal_url_end(url):
    return url if url[-1]=="/" else url+"/"
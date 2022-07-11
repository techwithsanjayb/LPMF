from bs4 import BeautifulSoup
import requests
import re

def crawl_data(url):
  
    try:
      r = requests.get(url)

      print("Status : ", r.status_code)
      if r.status_code == 200:
        
        soup = BeautifulSoup(r.content, "html.parser")

        text_data = soup.get_text()

        sentence_data = []
        # text_data = text_data.replace(".", " ").replace(",", " ").replace(
        #     "’ ", " ").replace("\"", " ").replace("»", " ")
        
        for d in text_data.split("\n"):
            if d.strip() != '':
                sentence_data.append(d.strip())

        word_data = text_data.split()
        
        # filter invvalid words
        filtered_words = []
        
        pattern = re.compile('[a-zA-Z]')
        for i in word_data:
          if re.search(pattern, i):
            # print("Valid String : ", i)
            filtered_words.append(i)
          else:
            # print("Invalid String : ", i)
            pass
        print(filtered_words)
        unique_words = set(filtered_words)

        return {"status": True , "total_words ": len(filtered_words), "total_unique_words ": len(unique_words)}
      else:
        return {"status": False , "message": "The URL doesn't exist"}
    except Exception:
      return {"status": False , "message": "The URL doesn't exist"}
    


if __name__ == '__main__':
  url = 'https://timest-influential-websites/'


  crawled_data = crawl_data(url)
  data = crawled_data
  if data["status"] :
    status,total_words, unique_words = data.values()

    print("total_words = ", total_words)
    print("unique_words = ", unique_words)
  else:
    print(data["message"])
  

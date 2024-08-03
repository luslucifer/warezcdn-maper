import json , requests , re ,random
from multiprocessing import Pool 
from bs4 import BeautifulSoup

vidsrc = 'https://vidsrc.me'# ids/mov_tmdb.txt'
root = 'https://embed.warezcdn.com'
class Main:
    def __init__(self,id:str=None,is_movie=True,threades = 5) -> None:
        self.is_movie = is_movie
        self.id =str(id) if id else None
        # self.is_imdb  = True if re.sub(r'\s+','',self.id).startswith('tt') else False
        self.threades  = threades
        self.preparing()
        self.type = "Movie" if self.is_movie else "tv"
        
    
    def preparing(self): 
        url = f'{vidsrc}/ids/{"mov" if self.is_movie else "tv_imdb"}.txt'
        print(url)
        res  = requests.get(url)
        ids = res.text.splitlines()
        self.ids = ids
    
    def check(self,id:str): 
        # pass
        try :
            url = f'{root}/{"filme" if self.is_movie else  "serie"}/{id}'
            res = requests.get(url)
            soup = BeautifulSoup(res.text,'html.parser')
            title = soup.find('title')
            title_text  = title.text.strip()
            print(title_text)
            if title_text.endswith('Video') == False : 
                print(f'id={id}\n type={self.type} \n exists !!! ')
                return id
            else : 
                print(f'id={id}\n type={self.type} \n  doesnt exists   !!! ')
                return None
        except Exception as err : 
            print(err)
    def main(self) :
        if not self.id :
            self.ids  =  self.ids[1:100]
            print(self.ids)
            with Pool(self.threades) as p : 
                arr = p.map(self.check,self.ids)
            arr = [x for x in arr if x]
            with open(f'ids_{self.type}_{random.randint(1,500)}.json','w') as file :
                json.dump(arr,file,indent=2)
        else : 
            out = self.check(self.id)
            if out : 
                return True 
            else : 
                return False

if __name__ == "__main__" : 
    m = Main()

    print(m.main())


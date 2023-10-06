import time
from app.webscrper import ScrapersPool

def main():
    start = time.time()
    result_list = ScrapersPool('football',3).get_data()
    end = time.time()
    for i in result_list:
        print(i)
    print(f'zakończono w {(end-start)/60} min')
if __name__ == "__main__":
    main()

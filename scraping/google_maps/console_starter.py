import os

number_of_packages = 100
def main():
    for i in range(number_of_packages):
        print("Start of ", i, "th package")
        cmd = 'google_maps_scraper.py'
        os.system(cmd)

if __name__ == "__main__":
    main()

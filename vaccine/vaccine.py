import argparse

def ft_vaccine(url, method, archive):
    print(url, method, archive)
    ## validate url and method

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vaxxxxxxxxxx 💉")
    parser.add_argument('-o', default='./archive.txt', help='Storage file for the data')
    parser.add_argument('-X', default='GET', help='HTTP Method')
    parser.add_argument('URL', help='Target URL')

    args = parser.parse_args()

    ft_vaccine(args.URL, args.X, args.o)

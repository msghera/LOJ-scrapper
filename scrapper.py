import requests, os
from progress.bar import Bar


def connected_to_internet(url='http://www.lightoj.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False


def down(n, single=0):
    # this is the general url requred to access a problem
    url = 'http://www.lightoj.com/volume_showproblem.php?problem=' + str(n) + '&language=english&type=pdf'
    r = requests.get(url)
    # this vol specifies the volume of the problem
    '''
        single is 0 means volume is being downloaded
        single is 1 means a single problem is being downloaded
        single is 2 means all the problems are being downloaded
    '''
    if (single == 0):
        vol = int(n / 100)
        vol = str('Vol' + str(vol))
    elif (single == 1):
        vol = 'ProblemsByID'
    else:
        vol = 'Problems'

    fol = vol + '/' + str(n) + '.pdf'
    if not os.path.exists(vol):
        os.makedirs(vol)

    with open(fol, 'wb') as fd:
        fd.write(r.content)


def downloadbyid():
    n = input('\n\nWhat is the problem id you want to download [1000-1434]: ')
    n = int(n)
    if n > 1434 or n < 1000:
        print('\n\n[ERROR]The id you choose does not exist.')
        main()
    else:
        down(n, 1)
        print('\n\n' + str(n) + ' is Downloaded\n[Will be found in folder "ProblmesByID"]')
        main()


def downloadVol():
    n = input('\n\nWhich volume you would like to download [10/11/12/13/14]: ')
    n = int(n)
    if (n < 10 or n > 14):
        print('\n\nVolume does not exist, please choose between 10 to 14')
        downloadVol()
    else:
        start = n * 100
        end = start + 100
        end = min(end, 1435)

    temp = 0
    if (n == 14):
        temp = 34
    else:
        temp = 100
    bar = Bar('Downloading', max=temp)
    for i in range(start, end):
        down(i, 0)
        bar.next()
    print('\n\nVolume ' + str(n) + ' is downloaded.')
    main()


def downloadAll():
    start = 1000
    end = 1435
    bar = Bar('Downloading', max=435)
    for i in range(start, end):
        down(i, 2)
        bar.next()
    print('\n\nAll problems are downloaded.')
    main()


def main():
    com = input('\n\n!!--Welcome to LightOJ problem statement downloader--!!\n'
                'Download problem by:\n'
                '1. Using problem ID (one at a time)\n'
                '2. A whole volume at a time\n'
                '3. All the 434 problems\n'
                '4. Exit\n'
                'Your responce [1/2/3/4] : ')
    com = int(com)

    if com == 1:
        downloadbyid()
    if com == 2:
        downloadVol()
    if com == 3:
        downloadAll()
    if com == 4:
        pass


if __name__ == '__main__':
    if (connected_to_internet):
        main()
    else:
        print('Internet Connection is required')

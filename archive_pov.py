import owl_cc_getids
import subprocess
import sys


data = owl_cc_getids
downloadAll = True

def download(mode):
    if not mode:
        for x in range(0, data.login.__len__(), 2):
            name = data.login[x]
            cmd = 'python twitchRecorder.py -u ' + name
            subprocess.run(("screen -dmS %s -L -Logfile logs/%s.txt %s" % (name, name, cmd)), shell=True)
    else:
        for x in range(0, data.login.__len__()):
            name = data.login[x]
            cmd = 'python twitchRecorder.py -u ' + name
            subprocess.run(("screen -dmS %s -L -Logfile logs/%s.txt %s" % (name, name, cmd)), shell=True)


def main(argv):
    usage_message = 'usage: python archive_pov.py [options] \n' \
                    '   options: \n' \
                    '       -p, --pov_only      download the 12 player pov streams + mainstream \n' \
                    '       -a, --all           download all streams. 1 mainstream, 12 pov, 12 pov+map'

    if len(argv) > 0:

        if len(argv) == 1:

            if (argv[0] == '-p') or ( argv == '--pov_only'):
                downloadAll = False
                print('Downloading only POV and mainstream')
            elif (argv[0] == '-a') or ( argv == '--all'):
                downloadAll = True
                print('Downloading all streams')
            elif (argv[0] == '-h') or ( argv == '--help'):
                print(usage_message)
                sys.exit()
            else:
                downloadAll = True
                print('No valid mode specified. Downloading all streams.')

        else:
            print('Error: Too many arguments.')
            sys.exit()

    else:
        print('Error: No mode specified.')
        print(usage_message)
        sys.exit()

    download(downloadAll)


if __name__ == "__main__":
    main(sys.argv[1:])


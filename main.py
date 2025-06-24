import yt_dlp

def check_a(url=None):
    o = {
        'quiet' : True,
        'skip_download' : True,
    }
    with yt_dlp.YoutubeDL(o) as ydl:
        i = ydl.extract_info(url, download=False)
        formats_b = i.get('formats:', [])
        best_a = [f for f in formats_b if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
        if best_a:
            best_a = sorted(best_a, key=lambda x: x.get('abr', 0), reverse=True)[0]
            abr = best_a.get('abr', 'desconhecido')
            ext = best_a.get('ext', 'desconhecido')
            print(f"\n Melhor áudio disponível: {abr}Kbps | Formato: {ext}")
        else:
            print("\n Nenhum áudio foi encontrado!")


def check_v(url):
    """Exibe as melhores resoluções de vídeo disponíveis."""
    o = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(o) as ydl:
        i = ydl.extract_info(url, download=False)

        # Pega os formatos de vídeo disponíveis
        formats_b = i.get('formats', [])
        videos = [f for f in formats_b if f.get('vcodec') != 'none']

        if videos:
            print("\nMelhores vídeos disponíveis:")
            for v in videos:
                res = v.get('height', 'Desconhecida')
                formato = v.get('format_id', 'Desconhecido')
                print(f"Resolução: {res}p, Formato: {formato}")
        else:
            print("\nNenhum vídeo encontrado!")


def check_p(url):
    """Exibe os vídeos e áudios disponíveis de uma playlist."""
    opcoes = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'cookie_file': 'cookie.txt',
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'referer': 'https://www.youtube.com/',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=False)

        if 'entries' in info:
            print("\nDetalhes da playlist:")
            for entry in info['entries']:
                print(f"- {entry['title']}")
        else:
            print("Não foi possível obter informações da playlist.")


def baixar_a(url):
    check_a(url)
    confirm = input("Prosseguir com o donwload? (S/N): ")
    if confirm != 's' or confirm != 'S':
        print("O donwload foi cancelado pelo usuário.")
    o = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with yt_dlp.YoutubeDL(o) as ydl:
        ydl.download([url])

def baixar_v(url):
    o = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(o) as ydl:
        print("\nIniciando o download do vídeo...")
        ydl.download([url])
    print("Download concluído!")

def baixar_m(url):
    o = {
        'format': 'bestaudio/best',  # Baixa o melhor áudio disponível
        'outtmpl': '%(title)s.%(ext)s',  # Formato de saída
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Formato MP3
            'preferredquality': '320',  # Qualidade 320kbps
        }],
    }

    with yt_dlp.YoutubeDL(o) as ydl:
        print("\nIniciando o download da música...")
        ydl.download([url])
    print("Download concluído!")


def baixar_plv(url):
    opcoes = {
        'format': 'bestvideo+bestaudio/best',  # Baixa o melhor vídeo e áudio para todos
        'outtmpl': '%(title)s.%(ext)s',  # Formato de saída
        'noplaylist': False,  # Para garantir que é uma playlist e não um único vídeo
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        print("\nIniciando o download da playlist de vídeos...")
        ydl.download([url])
    print("Download concluído!")

def baixar_plm(url):
    o = {
        'format': 'bestaudio/best',  # Baixa o melhor áudio disponível para todos
        'outtmpl': '%(title)s.%(ext)s',  # Formato de saída
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Formato MP3
            'preferredquality': '320',  # Qualidade 320kbps
        }],
        'noplaylist': False,  # Para garantir que é uma playlist e não um único áudio
    }

    with yt_dlp.YoutubeDL(o) as ydl:
        print("\nIniciando o download da playlist de músicas...")
        ydl.download([url])
    print("Download concluído!")




def m():
    while True:
        print(f'''
{"-=" * 35}
RedLoad
{"-=" * 35}
1 - BAIXAR VÍDEO
2 - BAIXAR MÚSICA
3 - BAIXAR MÚLTIPLAS MÚSICAS (PLAYLIST)
4 - BAIXAR MÚLTIPLOS VÍDEOS (PLAYLIST)
0 - SAIR DO PROGAMA
-------------------------------------------
        ''')
        e = int(input("Opção: "))
        if e == 0:
            print("Saindo...")
            break
        elif e == 1:
            url = input("Cole o link do vídeo: ")
            check_v(url)
            confirm = input("Deseja continuar com o download? (s/n): ").lower()
            if confirm == 's':
                baixar_v(url)
        elif e == 2:
            url = input("Cole o link do áudio: ")
            check_a(url)
            confirm = input("Deseja continuar com o download? (s/n): ").lower()
            if confirm == 's':
                baixar_m(url)
        elif e == 3:
            url = input("Cole o link da playlist de vídeos: ")
            check_p(url)
            confirm = input("Deseja continuar com o download? (s/n): ").lower()
            if confirm == 's':
                baixar_plv(url)
        elif e == 4:
            url = input("Cole o link da playlist de músicas: ")
            check_p(url)
            confirm = input("Deseja continuar com o download? (s/n): ").lower()
            if confirm == 's':
                baixar_plm(url)
        else:
            print("Opção inválida! Tente novamente.")

m()

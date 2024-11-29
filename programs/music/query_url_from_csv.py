from programs.music.music import query_musics_url


def query_musics(music_names: list):
    s1 = ''
    s2 = ''

    existing_names, non_existing_names = query_musics_url(music_names)

    if not existing_names.empty:
        s1 = existing_names.to_string(index=False, header=False)
    if len(non_existing_names) > 0:
        s2 = f'没有下面的歌曲：\n{non_existing_names}'
    s = s1 + '\n\n' + s2
    return s


if __name__ == '__main__':
    music_names = [
        '凉凉 - 杨宗纬,张碧晨.mp3',
        '凉凉 - 杨宗纬,张碧晨.flac',
        '突然想起你(Live) - 林宥嘉.mp3',
        '童话镇 - 陈一发儿.flac',
    ]
    print(query_musics(music_names))

from olefile import OleFileIO

filename = 'C:/Users/StevenChalem/congr-test/MyResume.doc'

with OleFileIO(filename) as ole:
    meta = ole.get_metadata()
    
    print('Author:', meta.author)
    print('Title:', meta.title)
    print('Creation date:', meta.create_time)
    print('Last saved by:', meta.last_saved_by)
    print('Last saved time:', meta.last_saved_time)
    print('Number of pages:', meta.num_pages)
    print('Number of words:', meta.num_words)
    print('Number of characters:', meta.num_chars)
    # print('Application name:', meta.appname)
    print('Security:', meta.security)

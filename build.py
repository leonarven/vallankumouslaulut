#!/bin/python3

import json, markdown, os

SOURCE_DIR = "./src/"
OUTPUT_DIR = "./dist/"

markdown.markdown('#Hi')

songs = os.listdir( SOURCE_DIR )

os.popen( 'mkdir -p ' + OUTPUT_DIR )

with open( os.path.join( SOURCE_DIR, 'index.json' )) as f:
    index = json.loads( f.read() )

for song in songs:
        
    source_dir = os.path.join( SOURCE_DIR, song )      
    
    if not os.path.isdir( source_dir ): continue

    html_file = os.path.join( source_dir, 'song.html' )
    md_file   = os.path.join( source_dir, 'song.md' )

    output = None
    meta = {}

    if song in index:
        meta = index[ song ]
    else:
        print( f'key { song } missing in index.json. Skipping!' ) 
        continue

    if os.path.isfile( html_file ):
        with open( html_file, 'r' ) as f:
            output = f.read()

    elif os.path.isfile( md_file ):
        with open( md_file, 'r' ) as f:
            output = f.read()
            output = markdown.markdown( output )

    if output is not None:

        article_attributes = ""

        if '&32;' in output:
            print( f'Typo: &32; instead of &#32; in { song }' )
            output = output.replace( "&32;", "&#32;" )

        if '&#32;' in output:
            # Koska halutaan sisällön rivittyvän ennustettavasti ja oletetaan sisältö muotoiltavan white-space'lla, niin voidaan korvata kaikki säkeiden välilyönnit &nbsp;:lla. Tällöin jäljelle myös jäävät HTML-entiteeteillä ohjatut välilyönnit, jotka on manuaalisesti asetettu
            article_attributes += ' class="fixed-size"'
        
        output = output.replace( " ", "&nbsp;" )

        # ---------
        
        meta_file = os.path.join( source_dir, 'meta.json' )
     
        if os.path.isfile( meta_file ):
            with open( meta_file, 'r' ) as f:
                meta.update( json.loads( f.read() ))
        
        # ---------

        heading = ""
        subheading = ""
        
        if 'title' in meta and meta['title'] is not None:
            heading = meta['title']

        if 'author' in meta and meta['author'] is not None:
            heading = f'{ meta["author"] }{ "" if len(heading) == 0 else ": " }{ heading }'           

        if 'num' in meta and meta['num'] is not None:
            heading = f'{ meta["num"] }. { heading }'
        
        if 'links' in meta:
            pass
        
        if 'subheading' in meta and meta['subheading'] is not None:
            subheading = meta['subheading']

        # ----------

        output = f'<section>{ output }</section>'

        if len( heading ) > 0:
            heading = f'<h1>{ heading }</h1>'

        if len( subheading ) > 0:
            if len( heading) > 0:
                heading += f'<h2>{ subheading }</h2>'
            else:
                heading = f'<h2>{ subheading }</h2>'

        if len( heading ) > 0:
            output = f'<header>{ heading }</header>{ output }'

        output = f'<article{ article_attributes }>{output}</article>'

        out_file = os.path.join( OUTPUT_DIR, song + '.html' )
        with open( out_file, "w" ) as out_file:
            out_file.write( output )


        # ----------

        meta['song_file'] = song + '.html'
        index[ song ] = meta

        ## Konvertoitiin index.json meta.json'eiksi ###########
        #meta_file = os.path.join( source_dir, 'meta.json' )
        #with open( meta_file, "w" ) as f:
        #    nmeta = meta.copy();
        #    if "author" not in nmeta: nmeta['author'] = None
        #    if "num" in nmeta: del nmeta["num"]
        #    if "song_file" in nmeta: del nmeta["song_file"]
        #    if "disabled" in nmeta: del nmeta["disabled"]
        #    json.dump( nmeta, f, indent=4, sort_keys=False )
        #######################################################

# -------------

index_file = os.path.join( OUTPUT_DIR, 'index.json' )

with open( index_file, "w") as index_file:
    json.dump( index, index_file, indent=4, sort_keys=False )

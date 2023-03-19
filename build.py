#!/bin/python3

import json, markdown, os

SOURCE_DIR = "./src/";
OUTPUT_DIR = "./dist/";

markdown.markdown('#Hi')

songs = os.listdir( SOURCE_DIR );

os.popen( 'mkdir -p ' + OUTPUT_DIR );

index_file = open( os.path.join( SOURCE_DIR, 'index.json' ))
index = json.loads( index_file.read());
index_file.close()

for song in songs:

    source_dir = os.path.join( SOURCE_DIR, song )      

    html_file = os.path.join( source_dir, 'song.html' )
    md_file   = os.path.join( source_dir, 'song.md' )

    output = None
    meta = {}

    if song in index:
        meta = index[ song ];

    if os.path.isfile( html_file ):
        file = open( html_file, 'r' )
        output = file.read()
        file.close();

    elif os.path.isfile( md_file ):
        file = open( md_file, 'r' )
        output = file.read()
        file.close();
        output = markdown.markdown( output )

    if output is not None:

        heading = ""
        subheading = ""

        # ---------

        meta_file = os.path.join( source_dir, 'meta.json' )
     
        if os.path.isfile( meta_file ):
            file = open( meta_file, 'r' )
            meta.update( json.loads( file.read() ))
            file.close();

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

        output = f'<article>{output}</article>'

        out_file = os.path.join( OUTPUT_DIR, song + '.html' )
        with open( out_file, "w" ) as out_file:
            out_file.write( output )


        # ----------

        meta['song_file'] = song + '.html';
        index[ song ] = meta;

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

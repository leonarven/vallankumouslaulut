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
    meta = None;

    if song in index:
        meta = index[ song ];

    if os.path.isfile( html_file ):
        file = open( html_file, 'r' )
        output = file.read()

    elif os.path.isfile( md_file ):
        file = open( md_file, 'r' )
        output = file.read()
        output = markdown.markdown( output )

    if output is not None:

        heading = ""
        subheading = ""

        if meta is not None:

            if 'title' in meta and meta['title'] is not None:
                heading = meta['title']
 
            if 'author' in meta and meta['author'] is not None:
                heading = f'{ meta["author"] }{ "" if len(heading) == 0 else ": " }{ heading }'           

            if 'num' in meta and meta['num'] is not None:
                heading = f'{ meta["num"] }. { heading }'
            
            if 'links' in meta:
                pass

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
        out_file = open( out_file, 'w' )
        out_file.write( output )
        out_file.close()

        # ---------

        meta_file = os.path.join( source_dir, 'meta.json' )
     
        if os.path.isfile( meta_file ):
            file = open( meta_file, 'r' )
            nmeta = json.loads( file.read() )

            if meta is None:
                meta = nmeta
            
            else:
                meta.update( nmeta );

            index[ song ] = meta;

index_file = os.path.join( OUTPUT_DIR, 'index.json' )

with open( index_file, "w") as index_file:
    json.dump( index, index_file, indent=4, sort_keys=False )

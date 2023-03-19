
# Vaatimukset
python3

# Käyttö
`python3 build.py`

# Muokkaus
`./src/` sisältää `song.key`n perusteella nimetyt kansiot lauluille. Kansiossa on laulun sanat tiedostossa `song.*` sekä mahdollisesti `meta.json`, jossa määritellään laulun tiedot.

Ensisijaisesti käytetään tiedostoa `song.html`, mutta jos tällaista ei hakemistosta löydy, etsitään tiedostoa `song.md`, joka konvertoidaan html'ksi.

## Esimerkki `meta.json`
Kaikki tiedot ovat vapaaehtoisia, koska laulukirjan sisällön määrittelyssä ne voidaan asettaa (sekä ylikirjoittaa.)
```json
{
  "title": "Laulelemme",
  "author": "Laulu- ja soitinyhtye Äänekkäät",
  "subheading": "(Sävel. )",
  "links": { ... }
}
```
TODO: schema.json 

## Nuotinnos (TODO)
(Jotakuinkin näin, dev.huom.)
```html
<b class="c c-Am"></b>Una mattina mi son svegliato,
O bella, ciao! Bella, ciao!
Bella, <b class="c c-Am7"></b>ciao, ciao, ciao!
Una mat<b class="c c-Dm"></b>tina mi son sveg<b class="c c-Am"></b>liato
e ho tro<b class="c c-E7"></b>vato l'inva<b class="c c-Am"></b>sor.
```

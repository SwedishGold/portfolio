"""Contracts for the one approved, user-initiated museum recording."""
from pathlib import Path
from html.parser import HTMLParser
import copy, hashlib, json, unittest
from test_portfolio import BUILD, ROOT

VIDEO='assets/museum-language-demo.mp4'
POSTER='assets/museum-language-demo-poster.jpg'
VIDEO_SHA='0dc27b2f7c09dd707331b3559a3df92932a3bd219de1f6ff770390f2245477c3'
POSTER_SHA='a06133a6ca5f413d7e89006b88c7f1081118ff0768a07e712f62300e64208bce'
class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class MuseumMediaTests(unittest.TestCase):
    def setUp(self):
        self.cases=json.loads((ROOT/'cases.json').read_text())
        self.museum=next(c for c in self.cases if c['id']=='museum')
        self.outputs=BUILD.build_outputs(self.cases)
        self.html=self.outputs['index.html']
    def test_only_museum_has_a_source_bound_demo(self):
        self.assertEqual([c['id'] for c in self.cases if c.get('demo')],['museum'])
        demo=self.museum['demo']
        self.assertEqual((demo['video'],demo['poster']),(VIDEO,POSTER))
        self.assertIn('Umeå universitet',demo['caption'])
        self.assertIn('förproducerat',demo['caption'])
        self.assertIn('recording',demo['english'])
    def test_approved_media_bytes_are_present(self):
        self.assertEqual(hashlib.sha256((ROOT/VIDEO).read_bytes()).hexdigest(),VIDEO_SHA)
        self.assertEqual(hashlib.sha256((ROOT/POSTER).read_bytes()).hexdigest(),POSTER_SHA)
    def test_native_player_has_no_autoplay_loop_or_preload(self):
        tags=Tags(self.html).tags
        videos=[a for t,a in tags if t=='video']
        self.assertEqual(len(videos),1)
        player=videos[0]
        self.assertEqual(player['id'],'museum-video')
        self.assertEqual(player['poster'],POSTER)
        self.assertEqual(player['preload'],'none')
        for flag in ['controls','playsinline']:self.assertIn(flag,player)
        for flag in ['autoplay','loop','muted']:self.assertNotIn(flag,player)
        sources=[a for t,a in tags if t=='source']
        self.assertEqual(sources,[{'src':VIDEO,'type':'video/mp4'}])
        self.assertIn('museum-film',[a.get('id') for t,a in tags])
        self.assertIn(VIDEO,[a.get('href') for t,a in tags if t=='a'])
        self.assertFalse([t for t,a in tags if t in ['script','iframe']])
    def test_readme_and_case_link_to_real_player_and_thumbnail(self):
        for name,poster in [('README.md',POSTER),('cases/museum.md','../'+POSTER)]:
            text=self.outputs[name]
            self.assertIn(poster,text)
            self.assertIn('https://swedishgold.github.io/portfolio/#museum-film',text)
        self.assertIn(self.museum['demo']['english'],self.outputs['cases/museum.md'])
    def test_demo_paths_cannot_load_external_or_private_resources(self):
        demo={'video':VIDEO,'poster':POSTER,'title':'Demo','caption':'Recorded test','english':'Recorded test'}
        for bad in ['https://example.com/film.mp4','//example.com/film.mp4','../private.mp4','assets/../../secret.mp4','javascript:alert(1)','assets/film.mp4?token=secret']:
            with self.subTest(path=bad):
                cases=copy.deepcopy(self.cases);c=next(c for c in cases if c['id']=='museum')
                c['demo']={**demo,'video':bad}
                with self.assertRaises(ValueError):BUILD.build_outputs(cases)
    def test_demo_copy_is_escaped(self):
        cases=copy.deepcopy(self.cases);c=next(c for c in cases if c['id']=='museum')
        c['demo']={'video':VIDEO,'poster':POSTER,'title':'<script>bad</script>','caption':'<iframe>bad</iframe>','english':'safe'}
        out=BUILD.build_outputs(cases)['index.html']
        self.assertIn('&lt;script&gt;bad&lt;/script&gt;',out)
        self.assertFalse([t for t,a in Tags(out).tags if t in ['script','iframe']])

if __name__=='__main__':unittest.main()

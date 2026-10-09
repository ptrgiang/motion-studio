#!/usr/bin/env python3
"""Serve a local review studio. Read-only server; export notes and explicitly import them with review.py."""
import argparse,json,mimetypes,re
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import unquote,urlsplit
from review import identity,read,run_path,confined
ASSETS=Path(__file__).resolve().parent.parent/'assets'

def config(project,run_id):
    root=Path(project).resolve();out=run_path(root,run_id);m=read(out/'manifest.json');binding=identity(root,run_id)
    spec=read(root/'spec.json');engine=m['engine'];entry='src/promo.html' if engine=='dom' else 'src/canvas-starter.html' if engine=='canvas' else None
    return {'version':'1.4.0','spec':spec,'engine':engine,'entry':('/'+entry if entry else None),'binding':binding,'films':{e['format']:'/out/'+run_id+'/'+e['film'] for e in m['exports']},'audio':('/out/'+run_id+'/audio/mix.wav' if spec['audio_mode']=='designed' else None)}

def make_server(project,run_id,port=0):
    root=Path(project).resolve();config(root,run_id)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            try:
                url=unquote(urlsplit(self.path).path)
                if url=='/__motion/config':
                    b=json.dumps(config(root,run_id)).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b);return
                if url in ('/','/__motion/preview.mjs'):
                    p=ASSETS/('preview.html' if url=='/' else 'preview.mjs')
                else:
                    relative=url.lstrip('/');parts=Path(relative).parts
                    if not parts or not (parts[0] in ('src','assets') or relative.startswith('out/'+run_id+'/') or relative=='spec.json'):raise ValueError('Path not served')
                    if any(part.startswith('.') or part=='..' for part in parts):raise ValueError('Path not served')
                    p=confined(root,relative)
                    if p.suffix.lower() not in ('.html','.mjs','.js','.css','.json','.png','.jpg','.jpeg','.webp','.svg','.ttf','.otf','.woff','.woff2','.mp4','.wav'):raise ValueError('File type not served')
                if not p.is_file():self.send_error(404);return
                size=p.stat().st_size;start,end=0,size-1;status=200
                if self.headers.get('Range'):
                    match=re.fullmatch(r'bytes=(\d+)-(\d*)',self.headers['Range'])
                    if not match:self.send_error(416);return
                    start=int(match[1]);end=min(int(match[2]) if match[2] else end,end)
                    if start> end:self.send_error(416);return
                    status=206
                self.send_response(status);self.send_header('Content-Type','text/javascript' if p.suffix=='.mjs' else mimetypes.guess_type(p.name)[0] or 'application/octet-stream');self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-store')
                if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
                self.end_headers()
                with p.open('rb') as f:
                    f.seek(start);remaining=end-start+1
                    while remaining:
                        b=f.read(min(65536,remaining))
                        if not b:break
                        self.wfile.write(b);remaining-=len(b)
            except (ValueError,KeyError,OSError,TypeError) as e:self.send_error(409,str(e))
        def do_POST(self):self.send_error(405,'Read-only studio; export notes for explicit import')
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--run-id',required=True);p.add_argument('--port',type=int,default=0);a=p.parse_args()
    try:
        server=make_server(a.project,a.run_id,a.port);print(f'Preview: http://127.0.0.1:{server.server_port}',flush=True)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
        finally:server.server_close()
    except (ValueError,OSError,KeyError) as e:p.exit(1,str(e)+'\n')

// Local deterministic production runtime. No connection to the user's browser session.
import {createRequire} from 'node:module';
import {readFile,realpath,stat} from 'node:fs/promises';
import {createServer} from 'node:http';
import path from 'node:path';
export function runtime(project){return createRequire(path.join(project,'package.json'))('playwright');}
export async function serve(project){
 const root=await realpath(project);const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.svg':'image/svg+xml','.ttf':'font/ttf','.woff2':'font/woff2','.wav':'audio/wav'};
 const server=createServer(async(req,res)=>{try{
  const relative=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/+/, '');
  const requested=path.resolve(root,relative||'index.html');const actual=await realpath(requested);
  if(actual!==root&&!actual.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
  if(!(await stat(actual)).isFile()){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',mime[path.extname(actual)]||'application/octet-stream');res.end(await readFile(actual));
 }catch{res.writeHead(404);res.end();}});
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
 return {origin:`http://127.0.0.1:${server.address().port}`,close:()=>new Promise(resolve=>server.close(resolve))};
}
export function argumentsOf(argv){const opts={};for(let i=0;i<argv.length;i+=2){if(!argv[i].startsWith('--')||!argv[i+1])throw Error('Arguments must be --key value pairs');opts[argv[i].slice(2)]=argv[i+1];}return opts;}
export function inside(project,relative){if(typeof relative!=='string'||!relative||path.isAbsolute(relative))throw Error('Expected project-relative path');const p=path.resolve(project,relative);if(!p.startsWith(project+path.sep))throw Error('Path outside project');return p;}
export async function ready(page,fonts=[]){
 await page.evaluate(async fonts=>{
  await document.fonts.ready;
  for(const f of fonts){if(!await document.fonts.load(f,'Aa').then(x=>x.length))throw Error('Font not loaded: '+f);}
  await Promise.all([...document.images].map(im=>im.decode()));
 },fonts);
}
export async function offline(context,origin){await context.route('**/*',route=>{
 const url=route.request().url();if(url.startsWith(origin+'/')||url.startsWith('data:')||url.startsWith('blob:'))return route.continue();return route.abort('blockedbyclient');
});}

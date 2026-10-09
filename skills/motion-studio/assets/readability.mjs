// Heuristic diagnostics. No OCR, semantic judgment, automatic creative pass or music analysis.
export function inspectLayout(doc,format,frame,policy={}){
 const phoneWidth=policy.phone_width??360,minText=policy.min_text_px??12,minControl=policy.min_ui_control_px??18;const scale=phoneWidth/format.width;
 const visible=node=>{for(let n=node;n&&n.nodeType===1;n=n.parentElement){const s=doc.defaultView.getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)<.5)return false;}return true;};
 const rect=r=>({x:r.x,y:r.y,width:r.width,height:r.height});
 const texts=[...doc.querySelectorAll('[data-read]')].filter(visible).map(node=>{const range=doc.createRange();range.selectNodeContents(node);const size=parseFloat(doc.defaultView.getComputedStyle(node).fontSize);return {id:node.dataset.read,text:node.textContent.trim(),font_px:size,phone_px:size*scale,rects:[...range.getClientRects()].filter(r=>r.width&&r.height).map(rect)};}).filter(t=>t.text);
 const regions=[...doc.querySelectorAll('[data-region]')].filter(visible).map(node=>({id:node.dataset.region,rects:[rect(node.getBoundingClientRect())]}));const warnings=[];
 for(const t of texts)if(t.phone_px<minText)warnings.push({kind:'small_text',id:t.id,phone_px:t.phone_px,minimum:minText});
 const items=[...texts,...regions];
 for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){let area=0;for(const a of items[i].rects)for(const b of items[j].rects)area+=Math.max(0,Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x))*Math.max(0,Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y));if(area>4)warnings.push({kind:'overlap',ids:[items[i].id,items[j].id],area});}
 const controls=[...doc.querySelectorAll('[data-ui-control-px]')].filter(visible).map(n=>({id:n.dataset.uiControl,phone_px:Number(n.dataset.uiControlPx)*scale}));
 for(const c of controls)if(c.phone_px<minControl)warnings.push({kind:'small_ui_control',...c,minimum:minControl});
 return {frame,texts,controls,warnings};
}
export function readingHolds(spec){const wps=spec.readability?.words_per_second??3;return spec.shots.map(s=>{const words=s.copy.trim().split(/\s+/u).filter(Boolean).length;const transitionEnd=Math.max(s.start,...(s.transitions||[]).map(t=>t.end));const hold=Math.max(0,s.end-transitionEnd)/spec.fps;const recommended=words/wps+.3;return {shot:s.id,words,hold_seconds:hold,recommended_seconds:recommended,warning:hold<recommended};});}
export function validatePolicy(policy={}){for(const k of ['phone_width','min_text_px','min_ui_control_px','words_per_second'])if(policy[k]!==undefined&&(!Number.isFinite(policy[k])||policy[k]<=0))throw Error('Positive finite readability policy required: '+k);}

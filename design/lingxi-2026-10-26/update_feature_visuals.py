from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'site.html'
try:
 s=p.read_text()
 start=s.index('.pcard{');end=s.index('.filt{',start)
 css='''/* Lingxi feature panels: product UI first; reference hierarchy, original brand staging. */
.pcard{display:grid;grid-template-columns:minmax(220px,1fr) minmax(0,1.65fr);border:1px solid #d9d5ce;border-radius:10px;overflow:hidden;background:#fffefa;margin-bottom:48px;scroll-margin-top:90px}
.pcard .tx{grid-column:1;grid-row:1;padding:30px 28px;display:flex;flex-direction:column;align-items:flex-start}
.pcard .tag{display:inline-block;font:500 12px/18px var(--sans);color:#605d52;border:1px solid #d9d5ce;padding:3px 7px;margin-bottom:18px}
.pcard h3{font:500 26px/1.25 var(--sans);letter-spacing:-.02em;margin:0 0 16px;color:var(--brown)}
.pcard p{font:400 16px/1.6 var(--sans);color:var(--brown);margin:0 0 24px}
.pcard .link{font:600 16px/1.4 var(--sans);margin-top:auto;display:inline-flex;gap:8px;text-decoration:underline;text-underline-offset:5px}
.pcard .vis{grid-column:2;grid-row:1;position:relative;min-width:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:18px;padding:34px 24px 22px;isolation:isolate;background:#b8c2df}
.pcard .vis::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(150deg,rgba(85,109,179,.22),transparent 55%,rgba(246,164,92,.44)),repeating-linear-gradient(90deg,transparent 0 89px,rgba(39,50,84,.11) 90px 91px)}
.pcard:nth-of-type(3n) .vis{background:#d2d5e5}
.pcard:nth-of-type(4n) .vis{background:#c2cccf}
.pcard .ui-preview{display:block;width:min(100%,353px);border:1px solid rgba(40,50,75,.14);border-radius:8px;overflow:hidden;background:white;box-shadow:0 14px 30px rgba(35,43,72,.14);transition:transform .2s ease}
.pcard .ui-preview:hover{transform:translateY(-3px)}
.pcard .ui-preview:focus-visible{outline:3px solid #dd4a09;outline-offset:5px}
.pcard .vis img{position:static;width:100%;height:auto;object-fit:contain;display:block}
.pcard .ui-caption{font:400 12px/1.5 var(--sans);color:#35405b;text-align:center;margin:0;max-width:none}
.pcard .ui-caption a{text-decoration:underline;text-underline-offset:3px}
.pcard.featured{display:flex;flex-direction:column}
.pcard.featured .vis{padding:40px 36px 24px;min-height:560px;display:grid;grid-template-columns:1fr 1fr;gap:24px}
.pcard.featured .ui-preview{justify-self:end;width:min(100%,353px)}
.pcard.featured .ui-caption{grid-column:1/-1}
.pcard.featured .tx{padding:30px 32px 34px}
.pcard .ui-steps{font:400 16px/1.6 var(--sans);max-width:270px;color:#26344f}
.pcard .ui-steps small{display:block;font-size:12px;margin-bottom:18px}
.pcard .ui-steps h4{font:500 28px/1.35 var(--sans);margin:0 0 25px}
.pcard .ui-steps span{display:inline-block;padding:7px 12px;background:rgba(255,255,255,.78);border:1px solid rgba(52,62,91,.15);border-radius:30px;margin:0 4px 8px 0;font-size:14px}
.pcard .ui-steps p{font-size:14px;color:#35405b;margin-top:20px}
@media(min-width:901px) and (max-width:1250px){.prod{grid-template-columns:178px minmax(0,1fr);column-gap:40px}.pcard{grid-template-columns:minmax(190px,1fr) minmax(0,1.4fr)}.pcard .tx{padding:25px 22px}}
@media(max-width:900px){.prod{grid-template-columns:1fr;column-gap:0;padding-bottom:70px}.pnav{position:static;display:flex;flex-direction:row;flex-wrap:wrap;gap:2px;margin-bottom:32px}.pnav b{margin:14px 0 2px;width:100%}.pnav a{padding:9px 12px}.pgroup{margin-bottom:26px}.pgroup:not(:first-child){margin-top:28px}}
@media(max-width:620px){.prod{padding-left:18px;padding-right:18px}.pcard{display:flex;flex-direction:column}.pcard .tx{order:0;padding:24px 22px}.pcard .vis{order:1;padding:24px 14px 18px;min-height:0}.pcard h3{font-size:24px}.pcard.featured .vis{display:flex;min-height:0;padding:24px 14px 18px}.pcard.featured .tx{padding:24px 22px}.pcard .ui-steps{display:none}.pcard .ui-caption{font-size:12px}.pcard .ui-preview{max-width:353px}.pcard .link{font-size:15px}.pcard{margin-bottom:30px}}
@media(prefers-reduced-motion:reduce){.pcard .ui-preview{transition:none}.pcard .ui-preview:hover{transform:none}}
'''
 s=s[:start]+css+s[end:]
 s=s.replace('它写的都标「AI 生成」，它记的你都能删。右边是每一项在 App 里的样子。','它写的都标「AI 生成」，它记的你都能删。下面用产品界面，看看每一步怎么用。')
 routes={'ideal':'me/ideal','report':'me/ideal','voice':'onboarding/5','memory':'me/memory','chat':'lx/chat','analyze':'lx/analyze','helper':'chat/lin','game':'chat/lin','pair':'me/tests/pair'}
 alts={'ideal':'理想型照片与上传、让灵犀画入口','report':'理想型分析与见面去处的原型界面','voice':'三段语音介绍的第一段与话题提示','memory':'灵犀记忆的来源及改删操作','chat':'和灵犀聊的四个提问入口','analyze':'聊天截图上传与分析方向选择','helper':'帮聊拟稿及待用户发送的输入框','game':'聊天中的石头剪刀布选择','pair':'合盘原型的六维图与仅供参考说明'}
 for key,route in routes.items():
  old=f'<div class="vis"><img src="art/web/prod/illu-{key}.jpg" alt=""></div>'
  assert s.count(old)==1,(key,s.count(old))
  steps=''
  if key=='ideal':steps='<div class="ui-steps"><small>从你喜欢的样子开始</small><h4>传一张照片，<br>看推荐理由。</h4><span>清冷</span><span>短发</span><span>冷色衣着</span><span>安静</span><p>照片特点 · AI 生成 · 仅供参考</p></div>'
  new=f'<div class="vis"><a class="ui-preview" href="app.html#{route}" target="_blank" rel="noopener" aria-label="打开{alts[key]}交互原型"><img src="art/web/prod/ui-2026-10-26/{key}.webp" alt="{alts[key]}，原型示例" loading="lazy" decoding="async"></a>{steps}<p class="ui-caption">交互原型 · 示例内容　<a href="app.html#{route}" target="_blank" rel="noopener">打开体验 ↗</a></p></div>'
  s=s.replace(old,new)
 s=s.replace('class="pcard ap" id="p-ideal"','class="pcard ap featured" id="p-ideal"')
 p.write_text(s)
 print('Updated nine product visuals, reference-based hierarchy, mobile layout.')
except Exception as e:raise SystemExit('Feature update failed: '+str(e))

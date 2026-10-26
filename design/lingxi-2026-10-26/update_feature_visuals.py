"""Rebuild all nine marketing previews using existing prototype content; no raster UI."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'

def icon(name):
    return f'<img class="lxui-icon" src="art/ink/{name}.svg" alt="">'

def action(text, route, secondary=False):
    return f'<a class="lxui-action{" secondary" if secondary else ""}" href="app.html#{route}">{text}{ARROW}</a>'

def shell(key, title, body, route):
    return f'''<div class="lxui lxui-{key}" aria-label="{title}界面示例">
    <div class="lxui-top"><strong>{title}</strong><span>界面示例</span></div>
    <div class="lxui-content">{body}</div></div>
    <p class="ui-caption">交互原型 · 示例内容 <a href="app.html#{route}">打开原型 {ARROW}</a></p>'''

bodies = {
'ideal':('我的理想型', f'''<div class="lxui-photo"><img src="art/people/ideal.webp" alt="原型中的理想型示例照片"><span>你喜欢的样子</span></div>
<h4>从一张照片开始。</h4><p>传一张理想型照片，<br>让灵犀了解你喜欢的样子。</p>
<div class="lxui-traits"><span>短发</span><span>冷色衣着</span></div>
<div class="lxui-foot">{action('到原型中上传照片','me/ideal')}{action('体验「让灵犀画」','me/ideal',True)}</div>''', 'me/ideal'),
'report':('理想型报告', f'''<div class="lxui-report-intro">{icon('act-eye')}<h4>先看理由，<br>再决定要不要认识。</h4></div>
<p>照片里是短发、冷色衣着。性格还要通过资料和相处了解。</p>
<div class="lxui-source">依据 · 你上传的理想型照片</div>
<div class="lxui-rule"></div><h5>见面去处</h5>
<dl class="lxui-details"><div><dt>时间</dt><dd>周六下午 · 周日上午</dd></div><div><dt>线索</dt><dd>摄影展 · 靠窗的咖啡馆 · 书店一角</dd></div></dl>
<p class="lxui-note">参考你的偏好，仅供参考。</p>{action('在原型中看完整报告','me/ideal')}''', 'me/ideal'),
'voice':('讲讲你', f'''<div class="lxui-segments" aria-label="三段自我介绍"><span class="selected">周末</span><span>过去的关系</span><span>理想中的人</span></div>
<div class="lxui-voice-prompt"><span>第 1 段 / 共 3 段</span><h4>周末你<br>喜欢做什么？</h4><p>聊两三分钟，灵犀记下你在意的事。每条都能改、能删。</p></div>
<div class="lxui-mic">{icon('act-mic')}</div><div class="lxui-suggestions"><span>看展、看电影</span><span>约朋友吃饭</span><span>在家待着</span></div>
{action('到原型中讲讲你','onboarding/5')}''', 'onboarding/5'),
'memory':('灵犀记得', f'''<h4>记得的每一条，<br>你都能做主。</h4><div class="lxui-memory-list">
<div><span class="lxui-kind">说话习惯</span><p>短句，少用语气词</p><small>来源 · 10-24 聊天 · 10-25 语音</small></div>
<div><span class="lxui-kind">你看重的事</span><p>周末要安静，看展多于聚会</p><small>来源 · 10-25 语音第 1 段</small></div></div>
<div class="lxui-permissions"><span>{icon('act-eye')}查看来源</span><span>{icon('act-settings')}可改可删</span></div>
{action('在原型中管理记忆','me/memory')}''', 'me/memory'),
'chat':('和灵犀聊', f'''<div class="lxui-greeting">{icon('act-star')}<div><h4>我是灵犀。</h4><p>可以聊推荐，也可以聊对话。</p></div></div>
<div class="lxui-questions">{''.join(f'<a href="app.html#lx/chat">{q}{ARROW}</a>' for q in ['我和林合不合？','今天该不该主动？','看看与林的对话','我适合什么样的人？'])}</div>
<p class="lxui-note">说说你最近在意的事。</p>{action('到原型中和灵犀聊','lx/chat')}''', 'lx/chat'),
'analyze':('聊天分析', f'''<h4>这一段对话，<br>一起看看。</h4><p>上传你有权使用的聊天截图。</p>
<a class="lxui-upload" href="app.html#lx/analyze">{icon('act-camera')}<strong>到原型中上传截图</strong><span>最多 3 张</span></a>
<h5>你想了解什么？</h5><div class="lxui-options"><span>对话含义</span><span>待了解的事</span><span>关系进展</span><span>怎么回复</span></div>
<p class="lxui-note">仅用于本次分析，用后删除，只给你看。</p>''', 'lx/analyze'),
'helper':('灵犀帮聊', f'''<div class="lxui-chatline"><img src="art/people/p01.webp" alt="原型人物林"><div><small>林 · 示例对话</small><p>哪个？</p></div></div>
<div class="lxui-draft"><div>{icon('act-wand')}<span>灵犀拟稿 · AI 生成</span></div><blockquote>是三影堂那个，这周六还在。你拍什么多？</blockquote></div>
<div class="lxui-source">依据 · 你 10-24 打卡「三影堂」<br>你的习惯 · 短句、不用「哈哈」</div>
<div class="lxui-rule"></div><p class="lxui-note">改好后，由你自己发。</p>{action('到原型中试试帮聊','chat/lin')}''', 'chat/lin'),
'game':('猜拳，赢的人先问', f'''<h4>不知道怎么开口，<br>先猜个拳。</h4><p>在聊天框里出手势。</p>
<div class="lxui-hands">{''.join(f'<div>{icon("game-"+name)}<span>{label}</span></div>' for name,label in [('rock','石头'),('scissors','剪刀'),('paper','布')])}</div>
<div class="lxui-rule"></div><p>赢了，从灵犀按你们俩资料出的问题里，挑一个问。</p>
{action('到原型中发起猜拳','chat/lin')}''', 'chat/lin'),
'pair':('你和林的合盘', f'''<div class="lxui-people"><div><img src="art/people/p21.webp" alt="原型中的你"><strong>你</strong><span>INFJ</span></div><span class="lxui-people-link">{icon('act-star')}</span><div><img src="art/people/p01.webp" alt="原型人物林"><strong>林</strong><span>ENFP</span></div></div>
<h4>慢慢了解。</h4><p>你们都提过喜欢安静，是否相处舒服还要聊聊看。</p>
<dl class="lxui-compare"><div><dt>星座</dt><dd>处女座 / 处女座</dd></div><div><dt>属相五行</dt><dd>土兔 / 金龙</dd></div><div><dt>恋爱风格</dt><dd>安全型 / Ta 未测</dd></div></dl>
<p class="lxui-note">AI 生成 · 仅供参考，不单独决定推荐。</p>{action('到原型中看完整合盘','me/tests/pair')}''', 'me/tests/pair'),
}

CSS = '''/* Lingxi feature UI v2: nine native, responsive product demonstrations. */
.pcard{display:grid;grid-template-columns:minmax(215px,.85fr) minmax(0,1.5fr);border:1px solid #dedcda;border-radius:12px;overflow:hidden;background:#fff;margin-bottom:48px;scroll-margin-top:90px}
.pcard .tx{grid-column:1;grid-row:1;padding:34px 28px;display:flex;flex-direction:column;align-items:flex-start}
.pcard .tag{display:inline-block;font:500 12px/18px var(--sans);color:#625b55;margin-bottom:16px;padding:0;border:0}
.pcard h3{font:500 27px/1.3 var(--sans);letter-spacing:-.02em;margin:0 0 16px;color:var(--brown)}
.pcard p{font:400 16px/1.75 var(--sans);color:var(--brown);margin:0 0 24px}
.pcard .link{font:600 15px/1.5 var(--sans);margin-top:auto;display:inline-flex;gap:8px;text-decoration:underline;text-underline-offset:5px}
.pcard .vis{grid-column:2;grid-row:1;position:relative;min-width:0;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:20px;padding:40px 28px 24px;background:#c5cce3}
.pcard:nth-of-type(3n) .vis{background:#d8d6e6}.pcard:nth-of-type(4n) .vis{background:#d8e0de}.pcard:nth-of-type(5n) .vis{background:#ead7c9}
.pcard .ui-caption{display:flex;justify-content:center;align-items:center;gap:12px;flex-wrap:wrap;font:400 12px/1.6 var(--sans);color:#3d465b;margin:0;text-align:center}
.pcard .ui-caption a{display:inline-flex;gap:4px;align-items:center;text-decoration:underline;text-underline-offset:4px}.pcard .ui-caption svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.5}
.pcard.featured{display:flex;flex-direction:column}.pcard.featured .vis{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:28px;padding:44px 40px 26px}.pcard.featured .lxui{justify-self:end}.pcard.featured .ui-caption{grid-column:1/-1}.pcard.featured .tx{padding:30px 34px}
.pcard .ui-steps{max-width:260px;color:#26344f}.pcard .ui-steps h4{font:500 30px/1.45 var(--sans);margin:0 0 26px}.pcard .ui-steps p{font-size:14px;line-height:1.8;color:#3c4760;margin:24px 0 0}.pcard .ui-steps span{display:inline-block;padding:7px 10px;border:1px solid #626e9040;border-radius:5px;font-size:14px;margin:0 5px 8px 0}
/* Shared native UI scale, scoped to feature previews. */
.lxui{--ui-ink:#25324b;--ui-muted:#58647a;--ui-line:#e1e5ee;--ui-tint:#f1f3f9;width:100%;max-width:440px;min-width:0;background:#fff;border:1px solid #d3d9e5;border-radius:16px;box-shadow:0 16px 38px #26395817;color:var(--ui-ink);font:400 15px/1.65 var(--sans);text-align:left;overflow:hidden}
.lxui *{box-sizing:border-box;min-width:0}.lxui ::selection{background:#f6ceb9;color:#25324b}
.lxui-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:20px 26px;border-bottom:1px solid var(--ui-line)}.lxui-top strong{font-weight:600;font-size:16px;line-height:1.5}.lxui-top>span{color:var(--ui-muted);font-size:12px;white-space:nowrap}
.lxui-content{padding:28px}.lxui h4{font:600 24px/1.45 var(--sans);letter-spacing:-.01em;margin:0 0 12px;color:var(--ui-ink)}.lxui h5{font:600 15px/1.5 var(--sans);margin:0 0 14px;color:var(--ui-ink)}
.pcard .lxui p{font:400 15px/1.75 var(--sans);color:var(--ui-muted);margin:0 0 20px}.lxui small{font-size:12px;line-height:1.65;color:var(--ui-muted)}
.lxui a{text-decoration:none}.lxui a:focus-visible{outline:3px solid #c7470b;outline-offset:3px}.lxui a:hover{filter:brightness(.96)}
.lxui-action{display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;padding:13px 16px;min-height:48px;background:#263750;border:1px solid #263750;border-radius:8px;color:#fff;font-size:14px;font-weight:500;line-height:1.5}.lxui-action.secondary{background:#f1f3f8;color:#263750;border-color:#e1e5ee}.lxui-action svg,.lxui-questions svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.5;flex:none}
.lxui-foot{display:grid;gap:10px;margin-top:24px}.lxui .lxui-icon{position:static;display:block;width:22px;height:22px;object-fit:contain;flex:none}
.lxui-photo{position:relative;margin:0 0 24px;border-radius:9px;overflow:hidden}.lxui-photo>img{display:block;width:100%;height:auto;aspect-ratio:5/4;object-fit:cover;object-position:center 30%}.lxui-photo>span{position:absolute;left:12px;bottom:12px;padding:6px 10px;border-radius:5px;background:white;color:#25324b;font-size:12px}
.lxui-traits{display:flex;flex-wrap:wrap;gap:8px}.lxui-traits span{padding:5px 10px;background:var(--ui-tint);border-radius:5px;font-size:13px}
.lxui-rule{height:1px;background:var(--ui-line);margin:24px 0}.lxui-source{font-size:12px;line-height:1.8;color:var(--ui-muted)}
.lxui-report-intro{display:flex;align-items:flex-start;gap:14px}.lxui-report-intro .lxui-icon{margin-top:6px}.lxui-details{margin:0 0 20px}.lxui-details>div{display:grid;grid-template-columns:44px minmax(0,1fr);gap:14px;padding:12px 0;border-bottom:1px solid var(--ui-line)}.lxui-details dt{color:var(--ui-muted);font-size:13px}.lxui-details dd{margin:0;font-size:15px}
.pcard .lxui p.lxui-note{font-size:12px;line-height:1.7;margin:16px 0;color:var(--ui-muted)}
.lxui-segments{display:flex;gap:4px;padding:4px;background:var(--ui-tint);border-radius:7px}.lxui-segments>span{flex:1;text-align:center;font-size:12px;padding:7px 3px;line-height:1.5;color:var(--ui-muted)}.lxui-segments .selected{background:#fff;border-radius:4px;color:var(--ui-ink);font-weight:600}
.lxui-voice-prompt{margin-top:34px}.lxui-voice-prompt>span{font-size:12px;color:var(--ui-muted)}.lxui-voice-prompt h4{font-size:28px;margin-top:12px}.lxui-mic{display:flex;align-items:center;justify-content:center;width:70px;height:70px;border:1px solid #e6bea8;border-radius:50%;background:#fbe7db;margin:28px auto}.lxui-mic .lxui-icon{width:28px;height:28px}
.lxui-suggestions{display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-bottom:26px}.lxui-suggestions span{padding:5px 8px;border:1px solid var(--ui-line);border-radius:5px;font-size:12px}
.lxui-memory-list>div{padding:20px 0;border-bottom:1px solid var(--ui-line)}.lxui-kind{font-size:12px;color:var(--ui-muted)}.pcard .lxui-memory-list p{font-size:16px;font-weight:500;margin:6px 0 8px;color:var(--ui-ink)}
.lxui-permissions{display:flex;gap:20px;margin:24px 0;font-size:12px;color:var(--ui-muted)}.lxui-permissions>span{display:flex;gap:7px;align-items:center}.lxui-permissions .lxui-icon{width:17px;height:17px}
.lxui-greeting{display:flex;gap:14px;margin-bottom:12px}.lxui-greeting>.lxui-icon{width:30px;height:30px;margin-top:2px}.lxui-greeting h4{font-size:23px}.lxui-questions{margin:8px 0 24px;border-top:1px solid var(--ui-line)}.lxui-questions>a{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:17px 0;border-bottom:1px solid var(--ui-line);font-size:15px;color:var(--ui-ink)}
.lxui-upload{display:flex;align-items:center;justify-content:center;flex-direction:column;gap:12px;border:1px dashed #98a6c1;border-radius:9px;background:var(--ui-tint);padding:28px 16px;color:var(--ui-ink);margin:24px 0}.lxui-upload .lxui-icon{width:30px;height:30px}.lxui-upload strong{font-size:15px;font-weight:500}.lxui-upload>span{font-size:12px;color:var(--ui-muted)}
.lxui-options{display:grid;grid-template-columns:1fr 1fr;gap:9px}.lxui-options span{font-size:13px;padding:9px 10px;border:1px solid var(--ui-line);border-radius:5px;color:var(--ui-ink)}
.lxui-chatline{display:flex;align-items:center;gap:12px;margin-bottom:26px}.lxui-chatline>img{width:42px;height:42px;object-fit:cover;border-radius:50%}.pcard .lxui-chatline p{font-size:16px;color:var(--ui-ink);margin:2px 0 0}.lxui-draft{padding:22px;background:#eff1f8;border-radius:9px;margin-bottom:18px}.lxui-draft>div{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--ui-muted)}.lxui-draft .lxui-icon{width:18px;height:18px}.lxui-draft blockquote{font-size:20px;line-height:1.7;letter-spacing:0;color:var(--ui-ink);padding:0;margin:16px 0 0;border:0}
.lxui-hands{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:36px 0}.lxui-hands>div{display:flex;flex-direction:column;align-items:center;gap:14px;background:var(--ui-tint);border-radius:8px;padding:20px 8px;font-size:13px}.lxui-hands .lxui-icon{width:46px;height:46px}
.lxui-people{display:flex;justify-content:center;align-items:center;gap:22px;margin:0 0 30px}.lxui-people>div{display:flex;flex-direction:column;align-items:center;gap:7px}.lxui-people img{width:64px;height:64px;border-radius:50%;object-fit:cover}.lxui-people strong{font-size:15px;font-weight:500}.lxui-people span{font-size:12px;color:var(--ui-muted)}.lxui-people .lxui-people-link{width:40px;border-bottom:1px solid #c7cfdf;padding-bottom:6px}.lxui-people-link .lxui-icon{width:22px;height:22px;margin:auto}
.lxui-compare{margin:24px 0}.lxui-compare>div{display:flex;justify-content:space-between;gap:15px;padding:12px 0;border-bottom:1px solid var(--ui-line)}.lxui-compare dt{font-size:13px;color:var(--ui-muted)}.lxui-compare dd{font-size:14px;margin:0;text-align:right}
@media(min-width:901px) and (max-width:1250px){.prod{grid-template-columns:155px minmax(0,1fr);column-gap:28px}.pcard{grid-template-columns:minmax(170px,.75fr) minmax(0,1.5fr)}.pcard .tx{padding:28px 22px}.pcard .vis{padding:28px 18px 22px}.pcard.featured .vis{padding:32px 24px 24px}.pcard .ui-steps h4{font-size:26px}}
@media(max-width:900px){.prod{grid-template-columns:1fr;column-gap:0;padding-bottom:70px}.pnav{position:static;display:flex;flex-direction:row;flex-wrap:wrap;gap:2px;margin-bottom:32px}.pnav b{margin:14px 0 2px;width:100%}.pnav a{padding:9px 12px}.pgroup{margin-bottom:26px}.pgroup:not(:first-child){margin-top:28px}}
@media(max-width:620px){.prod{padding-left:18px;padding-right:18px}.pcard{display:flex;flex-direction:column;margin-bottom:30px}.pcard .tx,.pcard.featured .tx{order:0;padding:26px 22px}.pcard .vis,.pcard.featured .vis{order:1;display:flex;padding:26px 14px 22px;gap:18px}.pcard h3{font-size:25px}.pcard .ui-steps{display:none}.lxui-top{padding:17px 20px}.lxui-content{padding:22px 20px}.lxui h4{font-size:23px}.lxui-voice-prompt h4{font-size:27px}.lxui-hands{gap:7px}.lxui-hands .lxui-icon{width:38px;height:38px}.lxui-hands>div{padding:18px 6px}.lxui-draft{padding:18px}.lxui-draft blockquote{font-size:19px}}
'''

try:
    path=ROOT/'site.html'
    s=path.read_text()
    # Replace only the existing feature-specific CSS. Retain the rest of the site.
    start=s.index('/* Lingxi feature')
    end=s.index('.filt{', start)
    s=s[:start]+CSS+s[end:]
    s=re.sub(r'/\* Crisp native feature UI:.*?(?=\.login-entry)', '', s, flags=re.S)
    s=re.sub(r'@media\(max-width:620px\)\{\.ideal-demo.*?\}\}', '', s)
    # Keep the existing text column and feature id, replace the entire visual column.
    for key,(title,body,route) in bodies.items():
        pattern=rf'(<div class="pcard[^"\n]*" id="p-{key}">)<div class="vis">.*?(?=<div class="tx">)'
        extra=''
        if key=='ideal':
            extra='<div class="ui-steps"><h4>传一张照片，<br>看推荐理由。</h4><span>短发</span><span>冷色衣着</span><p>照片特点 · AI 生成 · 仅供参考<br>性格还要通过资料和相处了解。</p></div>'
        markup=shell(key,title,body,route)
        if extra:
            markup=markup.replace('<p class="ui-caption">',extra+'<p class="ui-caption">')
        s,n=re.subn(pattern,lambda m:m[1]+'<div class="vis">'+markup+'</div>',s,flags=re.S)
        assert n==1, (key,n)
    assert 'ui-2026-10-26/' not in s
    assert s.count('class="lxui lxui-')==9
    path.write_text(s)
    print('Rebuilt all nine native feature previews. Existing copy, navigation, and login retained.')
except Exception as exc:
    raise SystemExit(f'Feature UI rebuild failed: {exc}') from exc

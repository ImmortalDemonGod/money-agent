/* Dev Card — shared render lib. Client-side, GitHub public API, zero backend/cost. Export-safe (no avatar image). */
(function(global){
  "use strict";
  var LANG_COLORS={JavaScript:"#f1e05a",TypeScript:"#3178c6",Python:"#3572A5",Go:"#00ADD8",Rust:"#dea584",
    Java:"#b07219",C:"#555555","C++":"#f34b7d","C#":"#178600",Ruby:"#701516",PHP:"#4F5D95",Swift:"#F05138",
    Kotlin:"#A97BFF",Shell:"#89e051",HTML:"#e34c26",CSS:"#563d7c",Vue:"#41b883",Dart:"#00B4AB",Elixir:"#6e4a7e",
    Haskell:"#5e5086",Scala:"#c22d40",Lua:"#000080",Zig:"#ec915c",Nix:"#7e7eff",OCaml:"#3be133",Clojure:"#db5855"};
  function langColor(l){ return LANG_COLORS[l] || "#8b949e"; }
  function hashHue(s){ var h=0; for(var i=0;i<s.length;i++){ h=(h*31+s.charCodeAt(i))>>>0; } return h%360; }
  function esc(s){ return String(s).replace(/[<>&'"]/g,function(c){return {'<':'&lt;','>':'&gt;','&':'&amp;',"'":'&apos;','"':'&quot;'}[c];}); }

  function gh(path){
    return fetch("https://api.github.com"+path,{headers:{"Accept":"application/vnd.github+json"}}).then(function(r){
      if(r.status===403) throw new Error("GitHub rate limit hit (60/hour). Try again shortly.");
      if(r.status===404) throw new Error("No GitHub user by that name.");
      if(!r.ok) throw new Error("GitHub error "+r.status);
      return r.json();
    });
  }

  // returns a Promise of a stats object
  function fetchStats(username){
    username=username.replace(/^@/,"").trim();
    return Promise.all([gh("/users/"+encodeURIComponent(username)), gh("/users/"+encodeURIComponent(username)+"/repos?per_page=100&sort=pushed")])
    .then(function(res){
      var u=res[0], repos=res[1]||[];
      var stars=0, langs={}, top=null;
      repos.forEach(function(r){
        stars+=r.stargazers_count||0;
        if(r.language) langs[r.language]=(langs[r.language]||0)+1;
        if(!top || (r.stargazers_count||0)>(top.stargazers_count||0)) top=r;
      });
      var topLangs=Object.keys(langs).sort(function(a,b){return langs[b]-langs[a];}).slice(0,4);
      var years=Math.max(0, (new Date() - new Date(u.created_at))/ (365.25*24*3600*1000));
      var tier = u.followers>=10000||stars>=20000 ? "Legendary" : u.followers>=1000||stars>=3000 ? "Epic"
               : u.followers>=100||stars>=300 ? "Rare" : u.followers>=10 ? "Uncommon" : "Common";
      return {login:u.login, name:u.name||u.login, followers:u.followers, repos:u.public_repos,
        stars:stars, topLangs:topLangs, topRepo: top?{name:top.name,stars:top.stargazers_count||0}:null,
        years:Math.round(years*10)/10, tier:tier, hue:hashHue(u.login)};
    });
  }

  function fmt(n){ return n>=1000 ? (Math.round(n/100)/10)+"k" : String(n); }

  function buildSVG(s, opts){
    opts=opts||{};
    var hue=s.hue, W=520, H=300;
    var c1="hsl("+hue+",70%,52%)", c2="hsl("+((hue+40)%360)+",70%,42%)", ink="#0d1117", card="#161b22", sub="#8b949e", fg="#e6edf3";
    var out=[];
    out.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'">');
    out.push('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="'+c1+'"/><stop offset="1" stop-color="'+c2+'"/></linearGradient></defs>');
    out.push('<rect width="'+W+'" height="'+H+'" rx="16" fill="'+ink+'"/>');
    out.push('<rect x="6" y="6" width="'+(W-12)+'" height="'+(H-12)+'" rx="12" fill="'+card+'" stroke="url(#g)" stroke-width="2"/>');
    // tier ribbon
    out.push('<rect x="'+(W-136)+'" y="20" width="116" height="26" rx="13" fill="url(#g)"/>');
    out.push('<text x="'+(W-78)+'" y="38" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="700" fill="#0d1117">'+esc(s.tier)+'</text>');
    // name / login
    out.push('<text x="28" y="46" font-family="Helvetica,Arial,sans-serif" font-size="26" font-weight="800" fill="'+fg+'">'+esc(s.name)+'</text>');
    out.push('<text x="28" y="70" font-family="Helvetica,Arial,sans-serif" font-size="15" fill="'+sub+'">@'+esc(s.login)+' &#183; '+s.years+' yrs on GitHub</text>');
    // stats row
    var stats=[["Followers",fmt(s.followers)],["Stars",fmt(s.stars)],["Repos",fmt(s.repos)]];
    stats.forEach(function(st,i){
      var x=28+i*164;
      out.push('<text x="'+x+'" y="128" font-family="Helvetica,Arial,sans-serif" font-size="30" font-weight="800" fill="url(#g)">'+st[1]+'</text>');
      out.push('<text x="'+x+'" y="148" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="'+sub+'" letter-spacing="1">'+st[0].toUpperCase()+'</text>');
    });
    // languages
    out.push('<text x="28" y="186" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="'+sub+'" letter-spacing="1">TOP LANGUAGES</text>');
    var lx=28;
    s.topLangs.forEach(function(l){
      var w=l.length*8.2+26;
      out.push('<rect x="'+lx+'" y="196" width="'+w+'" height="24" rx="12" fill="#0d1117" stroke="'+langColor(l)+'" stroke-width="1.5"/>');
      out.push('<circle cx="'+(lx+14)+'" cy="208" r="5" fill="'+langColor(l)+'"/>');
      out.push('<text x="'+(lx+24)+'" y="212" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="'+fg+'">'+esc(l)+'</text>');
      lx+=w+10;
    });
    // top repo
    if(s.topRepo){
      out.push('<text x="28" y="252" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="'+sub+'">Top repo: <tspan fill="'+fg+'" font-weight="700">'+esc(s.topRepo.name)+'</tspan> &#9733; '+fmt(s.topRepo.stars)+'</text>');
    }
    // footer / watermark
    var foot=opts.paid ? "" : "devcard.surge.sh";
    out.push('<text x="'+(W-28)+'" y="'+(H-18)+'" text-anchor="end" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="'+sub+'">'+esc(foot)+'</text>');
    out.push('</svg>');
    return {markup:out.join(""), W:W, H:H};
  }

  function svgToPng(markup,W,H,scale,cb){
    var img=new Image();
    img.onload=function(){ var cv=document.createElement("canvas"); cv.width=W*scale; cv.height=H*scale;
      var ctx=cv.getContext("2d"); ctx.drawImage(img,0,0,cv.width,cv.height);
      try{ cb(cv.toDataURL("image/png")); }catch(e){ cb(null); } };
    img.onerror=function(){ cb(null); };
    img.src="data:image/svg+xml;base64,"+btoa(unescape(encodeURIComponent(markup)));
  }
  function download(url,name){ var a=document.createElement("a"); a.href=url; a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){a.remove();},0); }

  function downloadPng(stats, scale, paid, name){
    var b=buildSVG(stats,{paid:paid}); svgToPng(b.markup,b.W,b.H,scale||2,function(u){ if(!u){alert("Could not render.");return;} download(u,name||"dev-card.png"); });
  }
  function readmeSnippet(stats){
    return "![My Dev Card](https://devcard.surge.sh/card.png?u="+encodeURIComponent(stats.login)+")\n\n_Made with devcard.surge.sh_";
  }

  global.DevCard={fetchStats:fetchStats, buildSVG:buildSVG, svgToPng:svgToPng, downloadPng:downloadPng, download:download, readmeSnippet:readmeSnippet};
})(window);

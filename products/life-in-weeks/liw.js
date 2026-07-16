/* Life in Weeks — shared render library. Pure client-side, zero network, zero per-use cost. */
(function(global){
  "use strict";

  var WEEKS_PER_YEAR = 52;
  var PALETTES = {
    ink:   {bg:"#f4f1ea", past:"#1c1c1c", future:"#d8d2c6", now:"#c2410c", text:"#1c1c1c"},
    dusk:  {bg:"#0f1226", past:"#c7d2fe", future:"#2a2f52", now:"#f472b6", text:"#e6e8f5"},
    ember: {bg:"#1a120b", past:"#f59e0b", future:"#3a2a1a", now:"#ef4444", text:"#f5ecdf"}
  };
  var MILE_COLORS = ["#0ea5e9","#16a34a","#a855f7","#eab308","#ec4899"];

  function escapeXml(s){
    return String(s).replace(/[<>&'"]/g, function(ch){
      return {'<':'&lt;','>':'&gt;','&':'&amp;',"'":'&apos;','"':'&quot;'}[ch];
    });
  }

  function weeksBetween(a, b){ return Math.floor((b - a) / (7*24*3600*1000)); }

  // state: {name, dob:'YYYY-MM-DD', lifeYears, palette, milestones:[{date,label,color}]}
  function buildSVG(state, opts){
    opts = opts || {};
    var p = PALETTES[state.palette] || PALETTES.ink;
    var years = state.lifeYears || 90;
    var cols = WEEKS_PER_YEAR, rows = years;

    var pad = 40, top = state.name ? 96 : 70;
    var cell = 9, gap = 2.4;
    var gw = cols*cell + (cols-1)*gap;
    var W = gw + pad*2;
    var H = top + rows*cell + (rows-1)*gap + pad + 30;

    var born = new Date(state.dob + "T00:00:00");
    var now = opts.now ? new Date(opts.now) : new Date();
    var lived = Math.max(0, weeksBetween(born, now));
    var totalWeeks = years*WEEKS_PER_YEAR;

    var mileByWeek = {};
    (state.milestones||[]).forEach(function(mi){
      var md = new Date(mi.date + "T00:00:00");
      var wk = weeksBetween(born, md);
      if(wk>=0 && wk<totalWeeks) mileByWeek[wk] = mi.color;
    });

    var s = [];
    s.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'">');
    s.push('<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="'+p.bg+'"/>');
    s.push('<text x="'+(W/2)+'" y="38" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif" font-size="26" fill="'+p.text+'">Life in Weeks</text>');
    if(state.name){
      s.push('<text x="'+(W/2)+'" y="'+(top-30)+'" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="15" fill="'+p.text+'" opacity="0.75">'+escapeXml(state.name)+'</text>');
    }
    s.push('<text x="'+(W/2)+'" y="'+(state.name?top-12:56)+'" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="'+p.text+'" opacity="0.5">Each row is a year &#183; each dot is one week</text>');

    for(var r=0;r<rows;r++){
      for(var c=0;c<cols;c++){
        var idx = r*cols + c;
        var x = pad + c*(cell+gap);
        var y = top + r*(cell+gap);
        var fill;
        if(mileByWeek[idx] !== undefined) fill = mileByWeek[idx];
        else if(idx < lived) fill = p.past;
        else if(idx === lived) fill = p.now;
        else fill = p.future;
        s.push('<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+cell+'" height="'+cell+'" rx="1.4" fill="'+fill+'"/>');
      }
    }
    var foot = opts.paid ? "" : "life-in-weeks.surge.sh";
    s.push('<text x="'+(W/2)+'" y="'+(H-14)+'" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="'+p.text+'" opacity="0.4">'+escapeXml(foot)+'</text>');
    s.push('</svg>');
    return {markup:s.join(""), W:W, H:H, lived:lived, total:totalWeeks};
  }

  // render SVG markup -> PNG dataURL at a pixel scale
  function svgToPng(markup, W, H, scale, cb){
    var img = new Image();
    img.onload = function(){
      var canvas = document.createElement("canvas");
      canvas.width = Math.round(W*scale); canvas.height = Math.round(H*scale);
      var ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      try { cb(canvas.toDataURL("image/png")); } catch(e){ cb(null); }
    };
    img.onerror = function(){ cb(null); };
    img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(markup)));
  }

  // free PNG (2x, watermarked) -> triggers download
  function downloadPng(state){
    var b = buildSVG(state, {paid:false});
    svgToPng(b.markup, b.W, b.H, 2, function(url){
      if(!url){ alert("Could not render the image in this browser."); return; }
      var a = document.createElement("a");
      a.href = url; a.download = "life-in-weeks.png"; a.click();
    });
  }

  function triggerDownload(dataUrl, filename){
    var a = document.createElement("a");
    a.href = dataUrl; a.download = filename; document.body.appendChild(a); a.click();
    setTimeout(function(){ a.remove(); }, 0);
  }

  function makePdf(url, b, state){
    var jsPDF = global.jspdf.jsPDF;
    var pageW = 18, pageH = 24, margin = 1;
    var doc = new jsPDF({unit:"in", format:[pageW, pageH], orientation:"portrait"});
    var p = PALETTES[state.palette] || PALETTES.ink;
    doc.setFillColor(p.bg);
    doc.rect(0, 0, pageW, pageH, "F");
    var availW = pageW - 2*margin, availH = pageH - 2*margin;
    var ar = b.W / b.H;
    var drawW = availW, drawH = drawW / ar;
    if(drawH > availH){ drawH = availH; drawW = drawH * ar; }
    var ox = (pageW - drawW)/2, oy = (pageH - drawH)/2;
    doc.addImage(url, "PNG", ox, oy, drawW, drawH, undefined, "FAST");
    return doc;
  }

  // paid delivery: try a print-ready PDF at progressively safer resolutions; if the device cannot
  // build the PDF at all (mobile canvas limits), fall back to a high-res PNG so a payer is NEVER
  // left without a print file. done(err, format) — format is "pdf" or "png" on success.
  function downloadPdf(state, done){
    var b = buildSVG(state, {paid:true});
    var haveJsPdf = !!(global.jspdf && global.jspdf.jsPDF);
    // px-per-svg-unit scales to attempt, high->low (≈300dpi over a 22in edge, then safer)
    var ideal = (22 * 300) / b.H;
    var scales = [Math.min(ideal, 7), 5, 3.5, 2.5].filter(function(v,i,a){ return a.indexOf(v)===i; });

    function tryPdf(i){
      if(!haveJsPdf || i >= scales.length){ return pngFallback(); }
      svgToPng(b.markup, b.W, b.H, scales[i], function(url){
        if(!url){ return tryPdf(i+1); }
        try{
          var doc = makePdf(url, b, state);
          doc.save("life-in-weeks-poster.pdf");
          if(done) done(null, "pdf");
        }catch(e){ tryPdf(i+1); }
      });
    }
    function pngFallback(){
      // a print-resolution PNG (still a valid file for any print shop)
      svgToPng(b.markup, b.W, b.H, 3, function(url){
        if(!url){ if(done) done(new Error("render-failed")); return; }
        triggerDownload(url, "life-in-weeks-poster.png");
        if(done) done(null, "png");
      });
    }
    tryPdf(0);
  }

  global.LIW = {
    WEEKS_PER_YEAR: WEEKS_PER_YEAR,
    PALETTES: PALETTES,
    MILE_COLORS: MILE_COLORS,
    escapeXml: escapeXml,
    buildSVG: buildSVG,
    svgToPng: svgToPng,
    downloadPng: downloadPng,
    downloadPdf: downloadPdf
  };
})(window);

export default {
 async fetch(request, env) {
 const json=(data,status=200)=>Response.json(data,{status,headers:{"Cache-Control":"no-store","X-Content-Type-Options":"nosniff"}});
 try {
 const domain=env.ACCESS_TEAM_DOMAIN.trim().replace(/^https?:\/\//,"").replace(/\/+$/,"");
 const issuer=`https://${domain}`;
 const token=request.headers.get("Cf-Access-Jwt-Assertion");
 if(!token||!env.ACCESS_AUD)return json({error:"Unauthorized"},401);
 const parts=token.split(".");if(parts.length!==3)return json({error:"Unauthorized"},401);
 const decode=s=>Uint8Array.from(atob(s.replace(/-/g,"+").replace(/_/g,"/").padEnd(Math.ceil(s.length/4)*4,"=")),c=>c.charCodeAt(0));
 const parse=s=>JSON.parse(new TextDecoder().decode(decode(s)));
 const header=parse(parts[0]),claims=parse(parts[1]),now=Math.floor(Date.now()/1000);
 if(header.alg!=="RS256"||claims.iss!==issuer||!Array.isArray(claims.aud)||!claims.aud.includes(env.ACCESS_AUD.trim())||!Number.isFinite(claims.exp)||claims.exp<=now||(claims.nbf!==undefined&&(!Number.isFinite(claims.nbf)||claims.nbf>now)))return json({error:"Unauthorized"},401);
 const certs=await fetch(`${issuer}/cdn-cgi/access/certs`);if(!certs.ok)return json({error:"Authentication unavailable"},503);
 const {keys}=await certs.json();const jwk=keys.find(k=>k.kid===header.kid);if(!jwk)return json({error:"Unauthorized"},401);
 const key=await crypto.subtle.importKey("jwk",jwk,{name:"RSASSA-PKCS1-v1_5",hash:"SHA-256"},false,["verify"]);
 const valid=await crypto.subtle.verify("RSASSA-PKCS1-v1_5",key,decode(parts[2]),new TextEncoder().encode(`${parts[0]}.${parts[1]}`));if(!valid)return json({error:"Unauthorized"},401);
 const url=new URL(request.url);if(url.hostname!=="vegassidekick.com"||url.pathname!=="/hub/api/test")return json({error:"Not found"},404);
 if(request.method!=="GET")return json({error:"Method not allowed"},405);
 const result=await env.DB.prepare("SELECT 1 AS connected").first();return json({app:"Vegas Sidekick Hub",authentication:"verified",database:result?.connected===1?"connected":"unavailable"});
 }catch{return json({error:"Request failed"},500);}
 }
};

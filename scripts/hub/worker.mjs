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
 const url=new URL(request.url);if(url.hostname!=="vegassidekick.com"||url.protocol!=="https:")return json({error:"Not found"},404);
 if(typeof claims.email!=="string"||!claims.email||typeof claims.sub!=="string"||!claims.sub)return json({error:"Unauthorized"},401);
 if(url.pathname!=="/hub/api/test")return await taskRequest(request,env.DB,claims.sub,json);
 if(request.method!=="GET")return json({error:"Method not allowed"},405);
 const result=await env.DB.prepare("SELECT 1 AS connected").first();return json({app:"Vegas Sidekick Hub",authentication:"verified",database:result?.connected===1?"connected":"unavailable"});
 }catch{return json({error:"Request failed"},500);}
 }
};

const departments=new Set(["command","tasks","shows","index","actions","analytics","marketing","partnerships"]);
const statuses=new Set(["backlog","todo","in_progress","awaiting","verification","completed"]);
const fields=["title","description","notes","department","priority","status","due_on","verification","project_id","parent_task_id"];
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
class InputError extends Error {}
function validate(input,old) {
 if(!input||typeof input!=="object"||Array.isArray(input))throw new InputError("Expected object");
 if(Object.keys(input).some(k=>!fields.includes(k)&&!(old&&k==="revision")))throw new InputError("Unsupported field");
 const t={...(old||{description:"",notes:"",priority:3,status:"todo",due_on:null,verification:null,project_id:null,parent_task_id:null}),...input};
 if(typeof t.title!=="string"||!t.title.trim()||t.title.trim().length>200)throw new InputError("Title must contain 1–200 characters");
 t.title=t.title.trim();
 if(!departments.has(t.department)||!statuses.has(t.status)||!Number.isInteger(t.priority)||t.priority<1||t.priority>4)throw new InputError("Invalid department, priority or status");
 for(const k of ["description","notes","verification"])if(!(k==="verification"&&t[k]===null)&&(typeof t[k]!=="string"||t[k].length>10000))throw new InputError("Invalid "+k);
 if(t.due_on!==null){if(typeof t.due_on!=="string"||!/^\d{4}-\d{2}-\d{2}$/.test(t.due_on))throw new InputError("Invalid due date");const d=new Date(t.due_on+"T00:00:00Z");if(!Number.isFinite(+d)||d.toISOString().slice(0,10)!==t.due_on)throw new InputError("Invalid due date");}
 for(const k of ["project_id","parent_task_id"])if(t[k]!==null&&(typeof t[k]!=="string"||!uuid.test(t[k])))throw new InputError("Invalid "+k);
 return t;
}
async function body(request){
 if(request.headers.get("Origin")!=="https://vegassidekick.com")throw new InputError("Same-origin request required");
 if(request.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase()!=="application/json")throw new InputError("JSON required");
 const reader=request.body?.getReader();if(!reader)throw new InputError("Body required");
 let size=0;const decoder=new TextDecoder();let raw="";
 while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>100000){await reader.cancel();throw new InputError("Body too large");}raw+=decoder.decode(value,{stream:true});}
 raw+=decoder.decode();try{return JSON.parse(raw);}catch{throw new InputError("Invalid JSON");}
}
export async function taskRequest(request,db,actor,json){
 const url=new URL(request.url),path=url.pathname,method=request.method;
 const match=path.match(/^\/hub\/api\/tasks\/([^/]+)(\/activity)?$/);
 if(path==="/hub/api/projects"||path.startsWith("/hub/api/projects/"))return projectRequest(request,db,actor,json);
 if(path!=="/hub/api/tasks"&&!match)return json({error:"Not found"},404);
 if(match&&!uuid.test(match[1]))return json({error:"Not found"},404);
 const q=(sql,...args)=>db.prepare(sql).bind(...args);
 try{
 if(method==="GET"){
 if(path==="/hub/api/tasks"){
 const limit=Number(url.searchParams.get("limit")||100),offset=Number(url.searchParams.get("offset")||0);
 if(!Number.isInteger(limit)||limit<1||limit>200||!Number.isSafeInteger(offset)||offset<0)return json({error:"Invalid pagination"},400);
 const rows=await q("SELECT * FROM tasks WHERE archived_at IS NULL ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?",limit,offset).all();
 return json({tasks:rows.results,limit,offset});
 }
 const task=await q("SELECT * FROM tasks WHERE id=? AND archived_at IS NULL",match[1]).first();
 if(!task)return json({error:"Not found"},404);
 if(match[2]){const rows=await q("SELECT * FROM activity WHERE task_id=? ORDER BY created_at DESC,id DESC LIMIT 200",task.id).all();return json({activity:rows.results});}
 return json({task});
 }
 if(method==="POST"&&path==="/hub/api/tasks"){
 const t=validate(await body(request)),id=crypto.randomUUID(),now=new Date().toISOString();
 await checkHierarchy(q,t);
 const completed=t.status==="completed";
 await db.batch([
 q("INSERT INTO tasks(id,title,description,notes,department,priority,status,due_on,verification,completed_at,completed_by,created_at,updated_at,project_id,parent_task_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",id,t.title,t.description,t.notes,t.department,t.priority,t.status,t.due_on,t.verification,completed?now:null,completed?actor:null,now,now,t.project_id,t.parent_task_id),
 q("INSERT INTO activity(id,task_id,project_id,department,event_type,actor_type,actor_id,importance,detail_json,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",crypto.randomUUID(),id,t.project_id,t.department,"created","manual",actor,t.priority,JSON.stringify({status:t.status,revision:1,project_id:t.project_id,parent_task_id:t.parent_task_id,completed_at:completed?now:null,verification:t.verification}),now)
 ]);
 return json({task:await q("SELECT * FROM tasks WHERE id=?",id).first()},201);
 }
 if(method==="PATCH"&&match&&!match[2]){
 const input=await body(request);
 if(!input||!Number.isSafeInteger(input.revision)||input.revision<1)return json({error:"Revision required"},400);
 const old=await q("SELECT * FROM tasks WHERE id=? AND archived_at IS NULL",match[1]).first();
 if(!old)return json({error:"Not found"},404);
 if(old.revision!==input.revision)return json({error:"Task changed; reload before editing"},409);
 const t=validate(input,old),now=new Date().toISOString();
 await checkHierarchy(q,t,old);
 const changed=fields.filter(k=>t[k]!==old[k]);
 if(!changed.length)return json({task:old});
 const completing=t.status==="completed"&&old.status!=="completed",reopening=t.status!=="completed"&&old.status==="completed";
 const completedAt=t.status==="completed"?(old.completed_at||now):null,completedBy=t.status==="completed"?(old.completed_by||actor):null;
 const event=completing?"completed":reopening?"reopened":"updated";
 const detail=JSON.stringify({revision:old.revision+1,changes:Object.fromEntries(changed.map(k=>[k,{before:old[k],after:t[k]}])),completed_at:completedAt,previous_completed_at:old.completed_at,verification:t.verification});
 const results=await db.batch([
 q("INSERT INTO activity(id,task_id,project_id,department,event_type,actor_type,actor_id,importance,detail_json,created_at) SELECT ?,id,?,?,?,?,?,?,?,? FROM tasks WHERE id=? AND revision=? AND archived_at IS NULL",crypto.randomUUID(),t.project_id,t.department,event,"manual",actor,t.priority,detail,now,old.id,old.revision),
 q("UPDATE tasks SET title=?,description=?,notes=?,department=?,priority=?,status=?,due_on=?,verification=?,completed_at=?,completed_by=?,updated_at=?,project_id=?,parent_task_id=?,revision=revision+1 WHERE id=? AND revision=? AND archived_at IS NULL",t.title,t.description,t.notes,t.department,t.priority,t.status,t.due_on,t.verification,completedAt,completedBy,now,t.project_id,t.parent_task_id,old.id,old.revision)
 ]);
 if(results[1].meta.changes!==1)return json({error:"Task changed; reload before editing"},409);
 return json({task:{...old,...Object.fromEntries(fields.map(k=>[k,t[k]])),completed_at:completedAt,completed_by:completedBy,updated_at:now,revision:old.revision+1}});
 }
 return json({error:"Method not allowed"},405);
 }catch(e){if(e instanceof InputError)return json({error:e.message},400);if(/Invalid parent task or project|Cannot invalidate child tasks/.test(String(e)))return json({error:"Task hierarchy changed; refresh before editing"},409);return json({error:"Request failed"},500);}
}

async function checkHierarchy(q,t,old){
 if(t.project_id&&!await q("SELECT id FROM projects WHERE id=? AND archived_at IS NULL",t.project_id).first())throw new InputError("Project not found");
 if(t.parent_task_id){
 const p=await q("SELECT id,project_id,parent_task_id FROM tasks WHERE id=? AND archived_at IS NULL",t.parent_task_id).first();
 if(!p||p.id===old?.id||p.parent_task_id||p.project_id!==t.project_id)throw new InputError("Choose a top-level task in the same project");
 }
 if(old&&(old.project_id!==t.project_id||t.parent_task_id!==null)&&await q("SELECT id FROM tasks WHERE parent_task_id=? LIMIT 1",old.id).first())throw new InputError("Move or detach subtasks first");
}
async function projectRequest(request,db,actor,json){
 const path=new URL(request.url).pathname,method=request.method;
 const q=(sql,...args)=>db.prepare(sql).bind(...args);
 try{
 if(method==="GET"&&path==="/hub/api/projects"){
 const url=new URL(request.url),limit=Number(url.searchParams.get("limit")||100),offset=Number(url.searchParams.get("offset")||0);
 if(!Number.isInteger(limit)||limit<1||limit>200||!Number.isSafeInteger(offset)||offset<0)return json({error:"Invalid pagination"},400);
 const rows=await q("SELECT * FROM projects WHERE archived_at IS NULL ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?",limit,offset).all();
 return json({projects:rows.results,limit,offset});
 }
 if(method==="POST"&&path==="/hub/api/projects"){
 const t=await body(request);
 if(!t||typeof t!=="object"||Array.isArray(t)||Object.keys(t).some(k=>!["title","description","department"].includes(k))||typeof t.title!=="string"||!t.title.trim()||t.title.trim().length>200||!departments.has(t.department)||typeof (t.description??"")!=="string"||(t.description??"").length>10000)throw new InputError("Invalid project details");
 const id=crypto.randomUUID(),now=new Date().toISOString();
 await db.batch([q("INSERT INTO projects(id,title,description,department,created_at,updated_at) VALUES(?,?,?,?,?,?)",id,t.title.trim(),t.description??"",t.department,now,now),q("INSERT INTO activity(id,project_id,department,event_type,actor_type,actor_id,detail_json,created_at) VALUES(?,?,?,?,?,?,?,?)",crypto.randomUUID(),id,t.department,"project_created","manual",actor,JSON.stringify({title:t.title.trim()}),now)]);
 return json({project:await q("SELECT * FROM projects WHERE id=?",id).first()},201);
 }
 return json({error:"Method not allowed"},405);
 }catch(e){if(e instanceof InputError)return json({error:e.message},400);return json({error:"Request failed"},500);}
}

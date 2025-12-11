export interface Agent {
  agent_id: string,
  os: string,
  os_version: string,
  arch: string,
  python_version: string,
  agent_version: string,
  first_seen: string,
  last_seen: string,
  last_heartbeat:string,
  meta: {}
}

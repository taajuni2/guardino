import * as events from "node:events";

export type ISODateTimeString = string;
export interface Event {
  id: string;
  ts: ISODateTimeString;
  agent_id: string;
  event_type: string;
  severity?: string | null;
  summary?: string | null;
  paths?: string[] | null;
  meta?: Record<string, any> | null;
  raw?: Record<string, any> | null;
}


export interface AgentLifecycle  extends Event{
}



export interface EventsGrouped {
  lifecycle: AgentLifecycle[];
  events: Event[];
}

export type UnifiedEvent = Event | AgentLifecycle;

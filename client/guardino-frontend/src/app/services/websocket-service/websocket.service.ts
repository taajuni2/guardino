import { Injectable, NgZone } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import {environment} from "../../../environment/environment";
import {Agent} from "../../../entities/Agent";
import {Event,UnifiedEvent, AgentLifecycle} from "../../../entities/Events";
import {WsMessage} from "../../../entities/Websocket";

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private ws?: WebSocket;
  private reconnectInterval = 3000;

  private agentSubject = new Subject<Agent>();
  private eventSubject = new Subject<Event>();

  agents$ = this.agentSubject.asObservable();
  events$ = this.eventSubject.asObservable();

  constructor(private zone: NgZone) { }

  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

    const wsUrl = environment.wsUrl;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log("[Websocket] Connected!", wsUrl);
    }

    this.ws.onmessage = (event: WsMessage) => {
      const message = JSON.parse(event.data);

      this.zone.run(() => {
        switch (message.type) {
          case 'agent_register':
            console.log("agent_register received in websocket.service")
            this.agentSubject.next(message as Agent);
            break;
          case 'event_new':
            this.eventSubject.next(message as Event);
            break;
          case 'agent_heartbeat':
            console.log("agent_heartbeat received in websocket.service")
            this.eventSubject.next(message as Event);
        }
      })
    }

    this.ws.onclose = () => {
      console.warn("[Websocket] Disconnected! Reconnecting...");
      setTimeout(() => this.connect(), this.reconnectInterval);
    }

    this.ws.onerror = (err) => {
      console.error("[Websocket] Error", err);
      this.ws?.close();
    }
  }
}

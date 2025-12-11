import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../../environment/environment";
import { BehaviorSubject, Observable } from "rxjs";
import { Agent } from "../../../entities/Agent";
import {WebsocketService} from "../websocket-service/websocket.service";

@Injectable({
  providedIn: 'root'
})
export class AgentService {

  private agentsSubject = new BehaviorSubject<Agent[]>([]);
  agents$ = this.agentsSubject.asObservable();

  constructor(
    private http: HttpClient,
    private websocketService: WebsocketService
  ) {
    // Initiale Ladung der Agents
    this.loadAgentsFromApi();

    // Live-Updates aus dem WebSocket
    this.websocketService.agents$.subscribe(agent => {
      this.upsertAgent(agent);
    });
  }

  // Falls du irgendwo explizit reloaden willst
  refreshAgents(): void {
    this.loadAgentsFromApi();
  }

  // Wenn eine Component nur "einmal" den aktuellen Stand braucht
  getAgentsOnce(): Observable<Agent[]> {
    return this.agents$; // optional .pipe(take(1))
  }

  // Snapshot synchron (z.B. für schnelle Berechnungen)
  getAgentsSnapshot(): Agent[] {
    return this.agentsSubject.value;
  }

  // -------- intern --------

  private loadAgentsFromApi(): void {
    this.http.get<Agent[]>(`${environment.apiUrl}/agents/all`)
      .subscribe(agents => {
        // z.B. neueste zuerst nach last_seen
        const sorted = [...agents].sort((a, b) =>
          (b.last_seen || '').localeCompare(a.last_seen || '')
        );
        this.agentsSubject.next(sorted);
      });
  }

  private upsertAgent(agent: Agent): void {
    const current = this.agentsSubject.value;
    const idx = current.findIndex(a => a.agent_id === agent.agent_id);

    let updated: Agent[];

    if (idx === -1) {
      // neuer Agent → oben einfügen
      updated = [agent, ...current];
    } else {
      // bestehenden Agent aktualisieren
      updated = [...current];
      updated[idx] = agent;
    }

    // optional nach last_seen sortieren (neueste oben)
    updated.sort((a, b) =>
      (b.last_seen || '').localeCompare(a.last_seen || '')
    );

    this.agentsSubject.next(updated);
  }
}

import { Component, OnInit } from '@angular/core';
import {AgentService} from "../../services/agent-service/agent.service";
import {Agent} from "../../../entities/Agent";
import {SimpleChanges} from "@angular/core";
import {WebsocketService} from "../../services/websocket-service/websocket.service";

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})

export class DashboardPageComponent implements OnInit {
  public agents: Agent[] = [];
  public inactiveAgents: Agent[] = [];
  public inactiveCount = 0;
  public activeCount = 0;

  constructor(private agentService: AgentService, private websocketService: WebsocketService) { }




  ngOnInit() {
    this.agentService.agents$.subscribe(agents => {
      this.agents = agents;

      this.inactiveAgents = agents.filter(a =>
        this.isAgentInactive(a.last_seen)
      );
      this.inactiveCount = this.inactiveAgents.length;
      this.activeCount = this.agents.length - this.inactiveCount;
    });
  }
  isAgentInactive(lastSeen: string | null | undefined): boolean {
    if (!lastSeen) return true;
    const last = new Date(lastSeen).getTime();
    const now = Date.now();
    const diffMs = now - last;
    return diffMs > 5 * 60 * 1000; // > 5 Minuten
  }

}

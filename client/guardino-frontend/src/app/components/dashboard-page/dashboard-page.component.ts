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
  public totalAgents: Agent[] = [];
  public totalAgentsCount: number = 0;
  public inactiveAgents : Agent[] = [];
  public inactiveCount:  number = 0;
  activeAgents = 0;
  threatsDetected = 0;
  constructor(private agentService: AgentService, private websocketService: WebsocketService) { }




  ngOnInit() {
    this.websocketService.connect();
    this.agentService.getAgents().subscribe(agents => {
      this.inactiveAgents = agents.filter(a =>
        this.isAgentInactive(a.last_seen)
      );
      this.activeAgents = this.totalAgentsCount - this.inactiveCount;
      this.inactiveCount = this.inactiveAgents.length;
    })
    this.websocketService.agents$.subscribe(agents => {
      console.log("[Websocket] Agents received", agents);
      this.totalAgents.push(agents);
      this.totalAgentsCount++
    })
  }
  private isAgentInactive(lastSeen: string, minutes: number = 5): boolean {
    if (!lastSeen) return true;

    const last = new Date(lastSeen).getTime();
    const now = Date.now();

    return (now - last) > minutes * 60 * 1000;
  }

}

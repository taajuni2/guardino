import { Component, OnInit } from '@angular/core';
import {AgentService} from "../../services/agent-service/agent.service";
import {Agent} from "../../../entities/Agent";

@Component({
  selector: 'app-dashboard-page',
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.scss'
})

export class DashboardPageComponent implements  OnInit {
  public totalAgents: number = 0;
  public inactiveAgents : Agent[] = [];
  public inactiveCount:  number = 0;
  constructor(private agentService: AgentService) { }


  activeAgents = 0;
  threatsDetected = 0;

  ngOnInit() {
    this.agentService.getAgents().subscribe(agents => {
      this.totalAgents = agents.length;
      console.log(agents)
      this.inactiveAgents = agents.filter(a =>
        this.isAgentInactive(a.last_seen)
      );
      this.activeAgents = this.totalAgents - this.inactiveCount;
      this.inactiveCount = this.inactiveAgents.length;

      console.log("Inactive agents:", this.inactiveAgents);
    })
  }
  private isAgentInactive(lastSeen: string, minutes: number = 5): boolean {
    if (!lastSeen) return true;

    const last = new Date(lastSeen).getTime();
    const now = Date.now();

    return (now - last) > minutes * 60 * 1000;
  }


}

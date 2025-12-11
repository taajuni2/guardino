import { Component, OnInit} from '@angular/core';
import {AgentService} from "../../../../services/agent-service/agent.service";
import {Agent} from "../../../../../entities/Agent";
import {EventService} from "../../../../services/event-service/event.service";

@Component({
  selector: 'app-agent-stats-card',
  templateUrl: './agent-stats-card.component.html',
  styleUrl: './agent-stats-card.component.scss'
})
export class AgentStatsCardComponent implements  OnInit {
  constructor(private agentService: AgentService, private eventService: EventService) { }
  totalAgents = 0;
  onlineAgents = 0;
  offlineAgents = 0;

  totalThreats = 0;

  ngOnInit() {
    this.agentService.agents$.subscribe(agents => {
      this.totalAgents = agents.length;

      this.onlineAgents = agents.filter(a => !this.agentService.isAgentInactive(a.last_seen)).length;
      this.offlineAgents = agents.filter(a =>  this.agentService.isAgentInactive(a.last_seen)).length;
    });

    this.eventService.threatsByAgent$.subscribe(threatMap => {
      this.totalThreats = Object.values(threatMap).reduce((a, b) => a + b, 0);
    });
  }



}

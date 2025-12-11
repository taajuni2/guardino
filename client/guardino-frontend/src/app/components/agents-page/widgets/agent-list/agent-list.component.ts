import {Component, OnInit} from '@angular/core';
import {AgentService} from "../../../../services/agent-service/agent.service";
import {EventService} from "../../../../services/event-service/event.service";
import {Agent} from "../../../../../entities/Agent";

@Component({
  selector: 'app-agent-list', templateUrl: './agent-list.component.html', styleUrl: './agent-list.component.scss'
})
export class AgentListComponent implements OnInit {
  agents: Agent[] = [];
  totalAgents = 0;
  onlineAgents = 0;
  offlineAgents = 0;
  threatsLast24h = 0;
  threatsByAgent: Record<string, number> = {};

  constructor(private agentService: AgentService, private eventService: EventService) {
  }

  ngOnInit() {
    this.agentService.agents$.subscribe(agents => {
      this.agents = agents;
      this.totalAgents = this.agents.length;

      const inactive = agents.filter(a => this.agentService.isAgentInactive(a.last_seen));
      this.offlineAgents = inactive.length;
      this.onlineAgents = this.totalAgents - this.offlineAgents;
    })

    this.eventService.threatsByAgent$.subscribe(map => {
      this.threatsByAgent = map;
    });
  }

  getThreats(agentId: string): number {
    return this.threatsByAgent[agentId] ?? 0;
  }


  getStatus(agent: Agent): 'online' | 'offline' | 'warning' {
    if (this.agentService.isAgentInactive(agent.last_seen)) return 'offline';
    if (this.getThreats(agent.agent_id) > 0) return 'warning';
    return 'online';
  }

}

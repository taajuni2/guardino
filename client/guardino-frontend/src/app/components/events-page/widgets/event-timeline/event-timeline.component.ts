import {Component} from '@angular/core';

interface EventItem {
  id: string;
  title: string;
  severity: 'info' | 'critical' | 'warning';
  agent: string;
  agentName: string;
  description?: string;
  timestamp: string;
  meta?: string;
}

@Component({
  selector: 'app-event-timeline',
  templateUrl: './event-timeline.component.html',
  styleUrl: './event-timeline.component.scss'
})
export class EventTimelineComponent {
  events: EventItem[] = [
    {
      id: '1',
      title: 'Regular heartbeat received',
      severity: 'info',
      agent: 'DESK-001',
      agentName: 'Marketing-PC-01',
      description: 'Agent status: Online, CPU: 45%, Memory: 67%, Disk: 23%',
      timestamp: '2024-10-06 14:32:15'
    },
    {
      id: '2',
      title: 'Suspicious file encryption activity detected',
      severity: 'critical',
      agent: 'SRV-005',
      agentName: 'FileServer-Main',
      description: 'Multiple files being encrypted in rapid succession. Pattern matches known ransomware behavior.',
      timestamp: '2024-10-06 14:30:42'
    },
    {
      id: '3',
      title: 'Full system scan completed',
      severity: 'info',
      agent: 'DESK-045',
      agentName: 'Dev-Workstation-03',
      description: 'Scanned 245,678 files. No threats detected. Scan duration: 1h 23m',
      timestamp: '2024-10-06 14:28:33'
    }
  ];

  selectedSeverity = 'all';
  selectedType = 'all';
}
